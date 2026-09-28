"""Artesian JSON wire format on top of msgspec.

DTOs stay plain dataclasses. On the wire:
- keys are PascalCase, private (``_x``) fields are dropped and ``None`` fields are omitted;
- enums travel by name; datetimes are RFC 3339 (naive stays naive, UTC gets ``Z``);
- a dict is sent as ``[{"Key": k, "Value": v}]`` only when its field is marked with
  :func:`keyValueArrayField` (the marker applies to every dict nested inside that field),
  otherwise as a JSON object. When decoding, any dict accepts both shapes.

Decoding compiles each target type once into a mirror ``msgspec.Struct`` so parsing and
validation run in C; a cached converter then rebuilds the dataclasses.
"""

import types
from collections.abc import Callable
from dataclasses import field, fields, is_dataclass
from datetime import date, datetime
from enum import Enum
from functools import cache
from typing import Any, Literal, Union, get_args, get_origin, get_type_hints

import msgspec

WIRE_METADATA_KEY = "artesian_wire"
KEY_VALUE_ARRAY = "key_value_array"


def keyValueArrayField() -> None:
    """A ``None``-defaulted dataclass field whose dicts are sent as Key/Value arrays."""
    return field(default=None, metadata={WIRE_METADATA_KEY: KEY_VALUE_ARRAY})


def _pascal(name: str) -> str:
    return name[0].upper() + name[1:]


# ---------------------------------------------------------------- encode

_PASSTHROUGH = frozenset({str, int, float, bool, type(None), datetime, date})


class _KeyValue(msgspec.Struct):
    Key: Any
    Value: Any


@cache
def _encodePlan(cls: type) -> tuple[tuple[str, str, bool], ...]:
    return tuple(
        (f.name, _pascal(f.name), f.metadata.get(WIRE_METADATA_KEY) == KEY_VALUE_ARRAY)
        for f in fields(cls)
        if not f.name.startswith("_")
    )


def _toWire(obj: object, kv: bool) -> object:
    t = type(obj)
    if t in _PASSTHROUGH:
        return obj
    if isinstance(obj, Enum):
        return obj.name
    # msgspec only encodes exact builtins: coerce subclasses such as pandas.Timestamp or numpy.float64.
    if isinstance(obj, datetime):
        return datetime(
            obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond, obj.tzinfo, fold=obj.fold
        )
    if isinstance(obj, date):
        return date(obj.year, obj.month, obj.day)
    for base in (float, int, str):
        if isinstance(obj, base):
            return base(obj)
    if isinstance(obj, dict):
        if kv:
            return [
                _KeyValue(
                    k if type(k) in _PASSTHROUGH else _toWire(k, True),
                    v if type(v) in _PASSTHROUGH else _toWire(v, True),
                )
                for k, v in obj.items()
            ]
        return {_toWire(k, False): _toWire(v, False) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [x if type(x) in _PASSTHROUGH else _toWire(x, kv) for x in obj]
    if is_dataclass(obj) and not isinstance(obj, type):
        out: dict[str, object] = {}
        for name, wire, fieldKv in _encodePlan(t):
            v = getattr(obj, name)
            if v is not None:
                out[wire] = _toWire(v, fieldKv)
        return out
    return obj


_encoder = msgspec.json.Encoder()


def artesianJsonEncode(obj: object) -> bytes:
    """Encodes ``obj`` to Artesian JSON bytes."""
    return _encoder.encode(_toWire(obj, False))


def artesianJsonSerialize(obj: object) -> object:
    """Converts ``obj`` to the JSON-compatible builtins Artesian expects on the wire."""
    return msgspec.to_builtins(_toWire(obj, False))


# ---------------------------------------------------------------- decode

# Wire types are assembled at runtime; typed as Any so checkers accept dynamic subscripts.
_Literal: Any = Literal
_Union: Any = Union

_Converter = Callable[[Any], Any] | None  # None means the decoded value is already final


@cache
def _compile(tp: Any) -> tuple[Any, _Converter]:
    """Returns the msgspec wire type for ``tp`` and the converter back to ``tp``."""
    if isinstance(tp, type) and is_dataclass(tp):
        return _compileDataclass(tp)
    if isinstance(tp, type) and issubclass(tp, Enum):
        return _Literal[tuple(tp.__members__)], lambda v: tp[v]
    origin, args = get_origin(tp), get_args(tp)
    if origin in (Union, types.UnionType):
        return _compileUnion(args)
    if tp is dict or origin is dict:
        return _compileDict(*(args or (Any, Any)))
    if tp is list or origin is list:
        itemWire, itemConv = _compile(args[0] if args else Any)
        if itemConv is None:
            return list[itemWire], None
        return list[itemWire], lambda v: [itemConv(x) for x in v]
    return tp, None


def _compileUnion(args: tuple[Any, ...]) -> tuple[Any, _Converter]:
    compiled = [_compile(a) for a in args]
    wire = _Union[tuple(w for w, _ in compiled)]
    convs = [c for (_, c), a in zip(compiled, args, strict=True) if a is not type(None)]
    if all(c is None for c in convs):
        return wire, None
    # ponytail: only Optional[X] needs a branch-aware converter; Union[A, B] of convertible types is unsupported.
    if len(convs) != 1:
        raise TypeError(f"Unsupported union for Artesian deserialization: {args}")
    conv = convs[0]
    assert conv is not None
    return wire, lambda v: None if v is None else conv(v)


def _compileDict(keyTp: Any, valueTp: Any) -> tuple[Any, _Converter]:
    keyWire, keyConv = _compile(keyTp)
    valueWire, valueConv = _compile(valueTp)
    entry = msgspec.defstruct("KeyValue", [("Key", keyWire), ("Value", valueWire)])
    wire = Union[dict[keyWire, valueWire], list[entry]]  # noqa: UP007 - built dynamically
    if keyConv is None and valueConv is None:
        return wire, lambda v: v if type(v) is dict else {e.Key: e.Value for e in v}
    kc = keyConv or (lambda x: x)
    vc = valueConv or (lambda x: x)

    def conv(v: Any) -> dict:
        items = v.items() if type(v) is dict else ((e.Key, e.Value) for e in v)
        return {kc(k): vc(x) for k, x in items}

    return wire, conv


def _compileDataclass(cls: type) -> tuple[Any, _Converter]:
    hints = get_type_hints(cls)
    specs: list[tuple[str, Any, Any]] = []
    convs: list[tuple[str, _Converter]] = []
    for f in fields(cls):
        if f.name.startswith("_") or not f.init:
            continue
        wire, conv = _compile(hints[f.name])
        # Null is accepted for any field, as before; missing fields keep the dataclass default.
        specs.append((f.name, Union[wire, None, msgspec.UnsetType], msgspec.UNSET))  # noqa: UP007
        convs.append((f.name, conv))
    mirror = msgspec.defstruct(cls.__name__, specs, rename=_pascal)

    def toDataclass(m: Any) -> object:
        kwargs = {}
        for name, conv in convs:
            v = getattr(m, name)
            if v is not msgspec.UNSET:
                kwargs[name] = v if conv is None or v is None else conv(v)
        return cls(**kwargs)

    return mirror, toDataclass


@cache
def _decoder(cls: Any) -> msgspec.json.Decoder:
    return msgspec.json.Decoder(_compile(cls)[0])


_untypedDecoder = msgspec.json.Decoder()


def artesianJsonDecode(data: bytes, cls: type | None = None) -> object:
    """Decodes Artesian JSON bytes into ``cls``, or into builtins when ``cls`` is None."""
    if cls is None:
        return _untypedDecoder.decode(data)
    conv = _compile(cls)[1]
    value = _decoder(cls).decode(data)
    return value if conv is None else conv(value)


def artesianJsonDeserialize(obj: object, cls: type) -> object:
    """Converts JSON-compatible builtins (as produced by ``artesianJsonSerialize``) into ``cls``."""
    wire, conv = _compile(cls)
    value = msgspec.convert(obj, wire)
    return value if conv is None else conv(value)
