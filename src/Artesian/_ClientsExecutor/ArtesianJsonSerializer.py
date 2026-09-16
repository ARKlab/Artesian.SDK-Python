from datetime import datetime
from platform import system
from dateutil import parser
import jsons
from typing import Any, Callable, Dict, Optional, get_args


__commonFmt = "%Y-%m-%dT%H:%M:%S.%f"
if system() == "Linux":
    __commonFmt = "%04Y-%m-%dT%H:%M:%S.%f"


def __artesianDatetimeSerializer(obj: datetime, **kwargs: Any) -> str:
    if obj.tzinfo is None:
        ret = obj.strftime(__commonFmt)
        return ret

    offset = obj.utcoffset()
    if offset is not None and offset.total_seconds() == 0:
        ret = obj.strftime(__commonFmt + "Z")
        return ret
    ret = obj.isoformat(timespec="seconds")
    return ret


def __artesianDatetimeDeserializer(obj: str, *args: Any, **kwargs: Any) -> datetime:
    return parser.isoparse(obj)


def __camelToPascal(k: str) -> str:
    return k[0].upper() + k[1:]


def __pascalToCamel(k: str) -> str:
    return k[0].lower() + k[1:]


def __is_valid_json_key(key: object) -> bool:
    return issubclass(type(key), (str, int, float, bool)) or key is None


def __artesianDictSerializer(
    obj: dict,
    *,
    key_transformer: Optional[Callable[[str], str]] = None,
    **kwargs: Any
) -> list:

    result = []
    append = result.append

    dt_ser = __artesianDatetimeSerializer
    nested_key_transformer = key_transformer or __camelToPascal
    items = obj.items

    for k, v in items():

        # ---- KEY ----
        if isinstance(k, datetime):
            k_out = dt_ser(k, **kwargs)
        elif isinstance(k, (str, int, float, bool)) or k is None:
            k_out = k
        else:
            k_out = str(k)

        # ---- VALUE ----
        if isinstance(v, datetime):
            v_out = dt_ser(v, **kwargs)
        elif isinstance(v, (str, int, float, bool)) or v is None:
            v_out = v
        else:
            v_out = jsons.dump(v, key_transformer=nested_key_transformer, **kwargs)

        append({"Key": k_out, "Value": v_out})

    return result


def __artesianDictDeserializer(
    obj: list, cls: type, *args: Any, **kwargs: Any
) -> object:
    key, value = get_args(cls)
    result: Dict[key, value] = {  # type: ignore
        jsons.load(item["Key"], key, *args, **kwargs): jsons.load(
            item["Value"], value, *args, **kwargs
        )
        for item in obj
    }

    return result


__artesianJsonSerializer = jsons.JsonSerializable.fork()

jsons.set_serializer(
    __artesianDictSerializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer
)
jsons.set_deserializer(
    __artesianDictDeserializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer
)

jsons.set_serializer(
    __artesianDatetimeSerializer,
    datetime,
    high_prio=True,
    fork_inst=__artesianJsonSerializer,
)
jsons.set_deserializer(
    __artesianDatetimeDeserializer,
    datetime,
    high_prio=True,
    fork_inst=__artesianJsonSerializer,
)


__artesianJsonKwArgs = {
    "strip_privates": True,
    "strip_nulls": True,
    # 'strict': True, disabled due to failure in untyped Dict (Tags)
    "use_enum_name": True,
    "fork_inst": __artesianJsonSerializer,
}


def artesianJsonSerialize(
    obj: object, cls: Optional[type] = None, **kwargs: Any
) -> object:
    """
    Sets the Artesian Json Serializer.

    Args:
      obj: string for the object for the serialization
      cls: type for the serialization
      kwargs: override the dump

    Returns:
      JsonSerializer.
    """
    kwargs_ = {**__artesianJsonKwArgs, **kwargs}
    return jsons.dump(obj, cls, key_transformer=__camelToPascal, **kwargs_)


def artesianJsonDeserialize(
    obj: object, cls: Optional[type] = None, **kwargs: Any
) -> object:
    """
    Sets the Artesian Json Deserializer.

    Args:
      obj: string for the object for the deserialization
      cls: type for the deserialization
      kwargs: override the load

    Returns:
      JsonDeserializer.
    """
    kwargs_ = {**__artesianJsonKwArgs, **kwargs, "strict": False}
    return jsons.load(obj, cls, key_transformer=__pascalToCamel, **kwargs_)
