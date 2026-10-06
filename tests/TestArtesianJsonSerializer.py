import unittest
from dataclasses import dataclass, field, fields
from datetime import UTC, date, datetime, timedelta, timezone

import msgspec
from dateutil import tz

from Artesian._ClientsExecutor.ArtesianJsonSerializer import (
    KEY_VALUE_ARRAY,
    WIRE_METADATA_KEY,
    artesianJsonDecode,
    artesianJsonDeserialize,
    artesianJsonEncode,
    artesianJsonSerialize,
    keyValueArrayField,
)
from Artesian.MarketData import MarketDataType, UpsertData
from Artesian.MarketData._Dto.TimeSerieData import TimeSerieData

NAIVE = datetime(2020, 1, 1, 1)  # noqa: DTZ001 - Artesian rows are naive local times


@dataclass
class _Sample:
    firstName: str
    kind: MarketDataType
    optional: int | None = None
    rows: dict[datetime, float | None] | None = keyValueArrayField()
    nested: dict[str, dict[str, int]] | None = keyValueArrayField()
    plain: dict[str, int | None] | None = None
    _hidden: int = field(default=0)


@dataclass
class _Inner:
    plain: dict[str, int]


@dataclass
class _Outer:
    marked: list[_Inner] | None = keyValueArrayField()
    unmarked: list[_Inner] | None = None


class TestArtesianJsonSerializer(unittest.TestCase):
    def test_marker_propagates_through_nested_dataclasses(self) -> None:
        inner = _Inner({"a": 1})
        self.assertEqual(
            artesianJsonSerialize(_Outer(marked=[inner], unmarked=[inner])),
            {"Marked": [{"Plain": [{"Key": "a", "Value": 1}]}], "Unmarked": [{"Plain": {"a": 1}}]},
        )

    def test_non_finite_floats_are_rejected(self) -> None:
        class Float64(float):
            pass

        for value in (float("nan"), float("inf"), float("-inf"), Float64("nan")):
            for payload in (
                _Sample("x", MarketDataType.ActualTimeSerie, rows={NAIVE: value}),
                {"k": value},
                [value],
            ):
                with self.subTest(value=value, payload=type(payload).__name__), self.assertRaises(ValueError):
                    artesianJsonEncode(payload)

    def test_wire_conventions(self) -> None:
        sample = _Sample(
            "x",
            MarketDataType.VersionedTimeSerie,
            rows={NAIVE: None},
            nested={"a": {"b": 1}},
            plain={"k": None},
            _hidden=5,
        )
        self.assertEqual(
            artesianJsonSerialize(sample),
            {
                "FirstName": "x",
                "Kind": "VersionedTimeSerie",
                "Rows": [{"Key": "2020-01-01T01:00:00", "Value": None}],
                "Nested": [{"Key": "a", "Value": [{"Key": "b", "Value": 1}]}],
                "Plain": {"k": None},
            },
        )

    def test_datetime_formats(self) -> None:
        cases = [
            (NAIVE, "2020-01-01T01:00:00"),
            (datetime(2020, 1, 1, tzinfo=tz.UTC), "2020-01-01T00:00:00Z"),
            (datetime(2020, 1, 1, 0, 0, 0, 5, tzinfo=UTC), "2020-01-01T00:00:00.000005Z"),
            (datetime(2020, 1, 1, tzinfo=timezone(timedelta(hours=2))), "2020-01-01T00:00:00+02:00"),
            (date(2020, 1, 1), "2020-01-01"),
        ]
        for value, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(artesianJsonSerialize(value), expected)
                self.assertEqual(artesianJsonEncode(value), f'"{expected}"'.encode())

    def test_builtin_subclasses(self) -> None:
        class Timestamp(datetime):
            pass

        class Float64(float):
            pass

        sample = _Sample("x", MarketDataType.ActualTimeSerie, rows={Timestamp(2020, 1, 1, 1): Float64(2.0)})
        expected = b'{"FirstName":"x","Kind":"ActualTimeSerie","Rows":[{"Key":"2020-01-01T01:00:00","Value":2.0}]}'
        self.assertEqual(artesianJsonEncode(sample), expected)

    def test_marker_uses_shared_metadata(self) -> None:
        marked = {f.name for f in fields(UpsertData) if f.metadata.get(WIRE_METADATA_KEY) == KEY_VALUE_ARRAY}
        self.assertEqual(marked, {"rows", "marketAssessment", "bidAsk", "auctionRows"})

    def test_decode_accepts_both_dict_shapes(self) -> None:
        expected = TimeSerieData(MarketDataType.ActualTimeSerie, rows={NAIVE: 1.0, datetime(2020, 1, 2): None})  # noqa: DTZ001
        bodies = [
            (
                b'{"Type":"ActualTimeSerie","Rows":[{"Key":"2020-01-01T01:00:00","Value":1.0},'
                b'{"Key":"2020-01-02T00:00:00","Value":null}],"Unknown":1}'
            ),
            b'{"Type":"ActualTimeSerie","Rows":{"2020-01-01T01:00:00":1.0,"2020-01-02T00:00:00":null}}',
        ]
        for body in bodies:
            with self.subTest(body=body):
                self.assertEqual(artesianJsonDecode(body, TimeSerieData), expected)

    def test_decode_nested_and_plain_dicts(self) -> None:
        body = b'{"FirstName":"x","Kind":"MarketAssessment","Optional":3,"Nested":{"a":[{"Key":"b","Value":1}]},"Plain":[{"Key":"k","Value":2}]}'
        expected = _Sample("x", MarketDataType.MarketAssessment, 3, nested={"a": {"b": 1}}, plain={"k": 2})
        self.assertEqual(artesianJsonDecode(body, _Sample), expected)
        self.assertEqual(artesianJsonDeserialize(artesianJsonSerialize(expected), _Sample), expected)

    def test_decode_rejects_unknown_enum_name(self) -> None:
        with self.assertRaises(msgspec.ValidationError):
            artesianJsonDecode(b'{"FirstName":"x","Kind":"Nope"}', _Sample)

    def test_decode_dotnet_seven_digit_fraction(self) -> None:
        value = artesianJsonDecode(
            b'{"Type":"ActualTimeSerie","Version":"2020-01-01T00:00:00.1234567Z"}', TimeSerieData
        )
        self.assertEqual(
            value, TimeSerieData(MarketDataType.ActualTimeSerie, version=datetime(2020, 1, 1, 0, 0, 0, 123457, UTC))
        )

    def test_decode_untyped(self) -> None:
        self.assertEqual(
            artesianJsonDecode(b'[{"T":"2020-01-01T00:00:00Z","D":1}]'), [{"T": "2020-01-01T00:00:00Z", "D": 1}]
        )
