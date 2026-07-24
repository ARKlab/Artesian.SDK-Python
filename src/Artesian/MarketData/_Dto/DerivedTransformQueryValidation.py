from dataclasses import dataclass
from typing import Optional
from .TimeSerieData import TimeSerieData


@dataclass
class DerivedTransformQueryValidation:
    """
    Class Derived transform query validation.

    Attributes:
        data: The time series data used for the query validation
        transform: The Transform query to apply on the referenced timeseries.
                   The query is executed against the helper table `$table`.
                   For ActualTimeSerie the table exposes `Time` (datetime) and `Value` (double).
                   For VersionedTimeSerie it exposes `Version` (datetime), `Time` (datetime) and `Value` (double).
                   The transform query should return `Time` and `Value` columns in the response.
                   Query examples
                   SELECT Time + INTERVAL 1 DAY AS Time, Value FROM $table
                   SELECT Time, CASE WHEN EXTRACT(HOUR FROM (Time AT TIME ZONE 'UTC') AT TIME ZONE 'Europe/Rome')
                   < 10 THEN Value + 1 ELSE Value END AS Value FROM $table WHERE Time IS NOT NULL
                   SELECT Time, Value FROM $table WHERE Version IS NOT NULL AND((EXTRACT(hour FROM Version)
                   < 10 AND Time >= date_trunc('day', Version + interval '1 day')) OR(EXTRACT(hour FROM Version)
                   >= 10 AND Time >= date_trunc('day', Version + interval '2 day')))

    """

    data: TimeSerieData
    transform: Optional[str] = None

    def __post_init__(self: "DerivedTransformQueryValidation") -> None:
        if self.transform is None:
            raise ValueError("transform must be provided for query validation.")
