from datetime import datetime
import Artesian
from Artesian.ArtesianConfig import ArtesianConfig
from Artesian.MarketData._Dto.DerivedTransformQueryValidation import (
    DerivedTransformQueryValidation,
)
from Artesian.MarketData._Dto.TimeSerieData import TimeSerieData
from Artesian.MarketData._Enum.MarketDataType import MarketDataType

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

mkdservice = Artesian.MarketData.MarketDataService(cfg)

# Validate a transform query against in-memory sample time-series data.
derivedTransformQueryValidation = DerivedTransformQueryValidation(
    data=TimeSerieData(
        type=MarketDataType.ActualTimeSerie,
        timezone="UTC",
        rows={
            datetime(2020, 1, 1, 0): 10.0,
            datetime(2020, 1, 1, 1): 11.0,
        },
    ),
    transform="SELECT Time, Value + 1 AS Value FROM $table"
)

result = mkdservice.derivedTransformQueryValidation(derivedTransformQueryValidation)

assert result.valid, (
    f"Derived transform query is not valid: "
    f"{result.error.message if result.error else 'unknown error'}"
)

assert result.data.rows is not None, "Expected transformed rows in response"
assert result.data.rows[datetime(2020, 1, 1, 0)] == 11.0
assert result.data.rows[datetime(2020, 1, 1, 1)] == 12.0

print(result)
