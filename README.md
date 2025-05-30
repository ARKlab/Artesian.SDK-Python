# Artesian.SDK

This Library provides read access to the Artesian API

## Getting Started

### Installation

You can install the package directly from [pip](https://pypi.org/project/artesian-sdk/).

```Python
pip install artesian-sdk
```

Alternatively, to install this package go to the [release page](https://github.com/ARKlab/Artesian.SDK-Python/releases) .

### How to use

The Artesian.SDK instance can be configured using API-Key authentication

```Python
from Artesian import ArtesianConfig

cfg = ArtesianConfig("https://arkive.artesian.cloud/{tenantName}/", "{api-key}")
```

## BREAKING CHANGES: Upgrade v2->v3

The following breaking changes has been introduced in v3 respect to v2.

### Python Version >=3.8

Python >=3.8 is **required**.
Python 3.7 is not supported due missing 'typing' features.

### SubPackaging

With Artesian-SDK v3 we introduced SubPkg to split the different part of the library. The new SubPkg are:

- Artesian.Query: contains all classes for querying Artesian data.
- Artesian.GMEPublicOffers: contains all classes for querying GME Public Offers
- **(NEW)** Artesian.MarketData: contains all classes to interact with the MarketData registry of Artesian. Register a new MarketData, change its Tags, etc. See documentation below.

To upgrade is enough to prefix the QueryService with 'Query.' or import it from Artesian.Query.

Were was used:

```Python
from Artesian import *

cfg = ArtesianConfig("https://arkive.artesian.cloud/{tenantName}/", "{api-key}")
qs = QueryService(cfg)
```

now you have to:

```Python
from Artesian import ArtesianConfig
from Artesian.Query import QueryService

cfg = ArtesianConfig("https://arkive.artesian.cloud/{tenantName}/", "{api-key}")
qs = QueryService(cfg)
```

### Enum entries Casing

To align the casing of the entries of the Enum, we adopted PascalCase to align it with the Artesian API.

Where before was used

```Python
  .inGranularity(Granularity.HOUR) \
```

now is

```Python
  .inGranularity(Granularity.Hour) \
```

## MarketData QueryService

Using the ArtesianConfig `cfg` we create an instance of the QueryService which is used to create Actual, Versioned and Market Assessment time series queries

### Actual Time Series Extraction

```Python
from Artesian import ArtesianConfig, Granularity
from Artesian.Query import QueryService, RelativeInterval

cfg = ArtesianConfig("https://arkive.artesian.cloud/{tenantName}/", "{api-key}")

qs = QueryService(cfg)
data = qs.createActual() \
    .forMarketData([100011484,100011472,100011477,100011490,100011468,100011462,100011453]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Hour) \
    .execute()

print(data)

```

To construct an Actual Time Series Extraction the following must be provided.

<table>
  <tr><th>Actual Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Time Granularity</td><td>Specify the granularity type</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Versioned Time Series Extraction

```Python
from Artesian import ArtesianConfig, Granularity
from Artesian.Query import QueryService, RelativeInterval

qs = QueryService(cfg)
q = qs.createVersioned() \
    .forMarketData([100042422,100042283,100042285,100042281,100042287,100042291,100042289]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Hour)

print(q)

ret = q.forMUV().execute()
print(ret)
ret = q.forLastNVersions(2).execute()
print(ret)
ret = q.forLastOfDays("2019-03-12","2019-03-16").execute()
print(ret)
ret = q.forLastOfDays("P0Y0M-2D","P0Y0M2D").execute()
print(ret)
ret = q.forLastOfDays("P0Y0M-2D").execute()
print(ret)
ret = q.forLastOfMonths("2019-03-12","2019-03-16").execute()
print(ret)
ret = q.forLastOfMonths("P0Y-1M0D","P0Y1M0D").execute()
print(ret)
ret = q.forLastOfMonths("P0Y-1M0D").execute()
print(ret)
ret = q.forVersion("2019-03-12T14:30:00").execute()
print(ret)
ret = q.forMostRecent("2019-03-12","2019-03-16").execute()
print(ret)
ret = q.forMostRecent("2019-03-12T12:30:05","2019-03-16T18:42:30").execute()
print(ret)
ret = q.forMostRecent("P0Y0M-2D","P0Y0M2D").execute()
print(ret)
ret = q.forMostRecent("P0Y0M-2D").execute()
print(ret)
ret = q.forMostRecent("2019-03-12","2019-03-16").execute()
print(ret)
ret = q.forMostRecent("P0Y-1M0D","P0Y1M0D").execute()
print(ret)
ret = q.forMostRecent("P0Y-1M0D").execute()
print(ret)
```

To construct a Versioned Time Series Extraction the following must be provided.

<table>
  <tr><th>Versioned Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Time Granularity</td><td>Specify the granularity type</td></tr>
  <tr><td>Versioned Time Extraction Window</td><td>Versioned extraction time window</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Market Assessment Time Series Extraction

```Python
from Artesian import ArtesianConfig
from Artesian.Query import QueryService, RelativeInterval

qs = QueryService(cfg)
data = qs.createMarketAssessment() \
    .forMarketData([100000032,100000043]) \
    .forProducts(["D+1","Feb-18"]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .execute()

print(data)
```

To construct a Market Assessment Time Series Extraction the following must be provided.

<table>
  <tr><th>Mas Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Product</td><td>Provide a product or set of products</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried </td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Bid Ask Time Series Extraction

```Python
from Artesian import ArtesianConfig
from Artesian.Query import QueryService, RelativeInterval

qs = QueryService(cfg)
data = qs.createBidAsk() \
    .forMarketData([100000032,100000043]) \
    .forProducts(["D+1","Feb-18"]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .execute()

print(data)
```

To construct a Bid Ask Time Series Extraction the following must be provided.

<table>
  <tr><th>Mas Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Product</td><td>Provide a product or set of products</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried </td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Auction Time Series Extraction

```Python
from Artesian import ArtesianConfig
from Artesian.Query import QueryService, RelativeInterval

qs = QueryService(cfg)
data = qs.createAuction() \
    .forMarketData([100011484,100011472,100011477,100011490,100011468,100011462,100011453]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .execute()

print(data)
```

To construct an Auction Time Series Extraction the following must be provided.

<table>
  <tr><th>Auction Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Extraction Windows

Extraction window types for queries.

Date Range

```Python
 .inAbsoluteDateRange("2018-08-01", "2018-08-10")
```

Relative Interval

```Python
 .inRelativeInterval(RelativeInterval.RollingWeek)
```

Period

```Python
 .inRelativePeriod("P5D")
```

Period Range

```Python
 .inRelativePeriodRange("P-3D", "P10D")
```

### Filler Strategy

All extraction types (Actual,Versioned, Market Assessment and BidAsk) have an optional filler strategy.

```python
var versionedSeries = qs
  .createVersioned() \
  .forMarketData([100000001]) \
  .forLastNVersions(1) \
  .inGranularity(Granularity.Day) \
  .inAbsoluteDateRange(new Date("2018-1-1"), new Date("2018-1-10")) \
  .withFillLatestValue("P5D") \
  .execute()
```

Use 'Null' to fill the missing timepoint with 'None' values.

```python
 .withFillNull()
```

Use 'None' to not fill at all: timepoints are not returned if not present.

```python
 .withFillNone()
```

Custom Value can be provided for each MarketDataType.

Custom Value for Actual extraction type.

```python
.withFillCustomValue(123)
```

Custom Value for BidAsk extraction type.

```python
.withFillCustomValue(
  bestBidPrice = 15.0,
  bestAskPrice = 20.0,
  bestBidQuantity = 30.0,
  bestAskQuantity = 40.0,
  lastPrice = 50.0,
  lastQuantity = 60.0)
```

Custom Value for Market Assessment extraction type.

```python
.withFillCustomValue(
settlement = 10.0,
open = 20.0,
close = 30.0,
high = 40.0,
low = 50.0,
volumePaid = 60.0,
volueGiven = 70.0,
volume = 80.0)
```

Custom Value for Versioned extraction type.

```python
.withFillCustomValue(123)
```

Latest Value to propagate the latest value, not older than a certain threshold only if there is a value at the end of the period.

```python
 .withFillLatestValue("P5D")
```

```python
 .withFillLatestValue("P5D", "False")
```

Latest Value to propagate the latest value, not older than a certain threshold even if there's no value at the end.

```python
 .withFillLatestValue("P5D", "True")
```

### Query written Versions or Products

Using MarketDataService is possible to query all the Versions and all the Products curves which has been written in a MarketData.

```Python
from Artesian.MarketData import MarketDataService

mds = MarketDataService(cfg)

```

To list MarketData curves

```Python
page = 1
pageSize = 100
res = mds.readCurveRange(100042422, page, pageSize, versionFrom="2016-12-20" , versionTo="2019-03-12")
```

### Search the MarketData collection with faceted results

Using MarketDataService is possible to query and search the MarketData collection with faceted results. Supports paging, filtering and free text.

```Python
from Artesian.MarketData import MarketDataService

mds = MarketDataService(cfg)

```

To list MarketData curves

```Python
page = 1
pageSize = 100
searchText = "Riconsegnato_"
filters = {"ProviderName": ["SNAM", "France"]}
sorts=["MarketDataId asc"]
doNotLoadAdditionalInfo=True
res = mds.searchFacet(page, pageSize, searchText, filters, sorts, doNotLoadAdditionalInfo)
```

## GME Public Offer

Artesian support Query over GME Public Offers which comes in a custom and dedicated format.

### Extract GME Public Offer

```Python
from Artesian.GMEPublicOffers import GMEPublicOfferService, Market, Purpose, Status, Zone, Scope, UnitType, GenerationType, BAType

qs = GMEPublicOfferService(cfg)

data = qs.createQuery() \
    .forDate("2020-04-01") \
    .forMarket([Market.MGP]) \
    .forStatus(Status.ACC) \
    .forPurpose(Purpose.BID) \
    .forZone([Zone.NORD]) \
    .withPagination(1,100) \
    .execute()

print(data)
```

To construct a GME Public Offer Extraction the following must be provided.

<table>
  <tr><th>GME Public Offer Query</th><th>Description</th></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
  <tr><td>Market</td><td>Provide a market or set of markets to query</td></tr>
   <tr><td>Status</td><td>Provide a status or set of statuses to query</td></tr>
    <tr><td>Purpose</td><td>Provide a purpose or set of purposes to query</td></tr>
     <tr><td>Zone</td><td>Provide a zone to query</td></tr>
     
</table>

### Unit of Measure Conversion Functionality

### Overview

The unit of measure conversion functionality allows users to request a conversion of units for Market Data that was registered using a different unit. This feature is supported only for Actual and Versioned Time Series.
Supported units are defined in the CommonUnitOfMeasure object and conform to ISO/IEC 80000 (i.e., `kW`, `MW`, `kWh`, `MWh`, `m`, `km`, `day`, `min`, `h`, `s`, `mo`, `yr`).

Note: Duration-based units are interpreted with the following fixed assumptions:
`1 day = 24 hours`
`1 mo = 30 days`
`1 yr = 365 days`

Additional supported units include **currency codes** in 3-letter format as per ISO 4217:2015 (e.g., `EUR`, `USD`, `JPY`). These are not part of CommonUnitOfMeasure and must be specified as regular strings.
Units of measure can also be **composite**, using the {a}/{b} syntax, where both {a} and {b} are either units from CommonUnitOfMeasure or ISO 4217 currency codes.

### Conversion Logic

Unit conversion is based on the assumption that each unit of measure can be decomposed into a **"BaseDimension"**, which represents a polynomial of base SI units (`m`, `s`, `kg`, etc.) and currencies (`EUR`, `USD`, etc.).
A unit of measure is represented as a value in BaseDimension UnitOdMeasure.
Example:
10 `Wh` = 10 `kg·m²·s⁻³`
Conversion is allowed when the BaseDimensions **match exactly**, i.e., the same set of base units raised to the same exponents.
In Artesian, units that differ **only** in the **time dimension** are also potentially convertible, as the time dimension can be inferred from the data’s time interval.

### Example: Power to Energy Conversion

Converting `W` to `Wh`:
• `W` → BaseDimension: `k·m²·s⁻³`
• `Wh` → BaseDimension: `kg·m²·s⁻²`
• `1 h = 3600 s`
**Conversion Steps:**
10 W = 10 kg·m²/s³
1 h = 3600 s
10 kg·m²/s³ × 3600 s = 36000 kg·m²/s² = 10 Wh

### MarketData Registration with UnitOfMeasure

The UnitOfMeasure is defined during registration:

```Python
mkd = MarketData.MarketDataEntityInput(
      providerName = "TestProviderName",
      marketDataName = "TestMarketDataName",
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.ActualTimeSerie,
      originalTimezone="CET",
      aggregationRule=AggregationRule.SumAndDivide,
    UnitOfMeasure = CommonUnitOfMeasure.kW
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)
```

### UnitOfMeasure Conversion and Aggregation Rule Override

In the QueryService, there are two supported methods related to unit of measure handling during extraction:

1. UnitOfMeasure Conversion
2. Aggregation Rule Override

### UnitOfMeasure Conversion

To convert a UnitOfMeasure during data extraction, use the `.inUnitOfMeasure()` method. This function converts the data from the unit defined at MarketData registration to the target unit you specify in the query.

```Python
qs = QueryService(cfg)
data = qs.createActual() \
    .forMarketData([100011484]) \
    .inAbsoluteDateRange("2024-01-01","2024-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Day) \
    .inUnitOfMeasure(CommonUnitOfMeasure.MW) \
    .execute()
```

By default, the aggregation rule used during extraction is the one defined at registration. However, you can override it if needed. The conversion is always applied before aggregation.

### Aggregation Rule Override

AggregationRule can be overrided using the `.withAggregationRule()` method in QueryService.

```Python
qs = QueryService(cfg)
data = qs.createActual() \
    .forMarketData([100011484]) \
    .inAbsoluteDateRange("2024-01-01","2024-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Day) \
    .withAggregationRule(AggregationRule.AverageAndReplicate) \
    .execute()
```

Sometimes, especially when converting from a **consumption unit** (e.g., `MWh`) to a **power unit** (e.g., `MW`), the registered aggregation rule (e.g., `SumAndDivide`) may not make sense for the new unit.

If you **don’t override the aggregation rule**, the conversion may produce **invalid or misleading results**.

### Example: Convert power (`MW`) to energy (`MWh`):

```Python
data = qs.createActual() \
    .forMarketData([100011484]) \
    .inAbsoluteDateRange("2024-01-01","2024-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Day) \
    .inUnitOfMeasure(CommonUnitOfMeasure.MWh) \
    .withAggregationRule(AggregationRule.AverageAndReplicate) \
    .execute()
```

### Composite Unit Example: `MWh/day`

```Python
data = qs.createActual() \
    .forMarketData([100011484]) \
    .inAbsoluteDateRange("2024-01-01","2024-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Day) \
    .inUnitOfMeasure(CommonUnitOfMeasure.MWh / CommonUnitOfMeasure.day) \
    .withAggregationRule(AggregationRule.AverageAndReplicate) \
    .execute()
```

### CheckConversion: Validate Unit Compatibility

Use the `CheckConversion` method to verify whether a list of input units can be converted into a specifified target unit:

```Python
from Artesian import ArtesianConfig, MarketData
from Artesian.MarketData import CommonUnitOfMeasure

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

inputUnitsOfMeasure = [CommonUnitOfMeasure.kW, CommonUnitOfMeasure.kWh, "EUR/MWh"]
targetUnitOfMeasure = CommonUnitOfMeasure.MW

checkConversionResult = mkservice.checkConversion(inputUnitsOfMeasure , targetUnitOfMeasure)
```

**Returned Object: CheckConversionResult**

1. TargetUnitOfMeasure: "`kW`"
2. ConvertibleInputUnitsOfMeasure: [ "`MW`", "`kW/s`" ]
3. NotConvertibleInputUnitsOfMeasure: [ "`s`" ]

### Extraction Options

Extraction options for GME Public Offer queries.

#### Date

```Python
 .forDate("2020-04-01")
```

#### Purpose

```Python
 .forPurpose(Purpose.BID)
```

#### Status

```Python
 .forStatus(Status.ACC)
```

#### Operator

```Python
 .forOperator(["Operator_1", "Operator_2"])
```

#### Unit

```Python
 .forUnit(["UP_1", "UP_2"])
```

#### Market

```Python
 .forMarket([Market.MGP])
```

#### Scope

```Python
 .forScope([Scope.ACC, Scope.RS])
```

#### BAType

```Python
 .forBAType([BAType.NETT, BAType.NERV])
```

#### Zone

```Python
 .forZone([Zone.NORD])
```

#### UnitType

```Python
 .forUnitType([UnitType.UCV, UnitType.UPV])
```

#### Generation Type

```Python
 .forGenerationType(GenerationType.GAS)
```

#### Pagination

```Python
 .withPagination(1,10)
```

#### UnitOfMeasure (for Actual and Versioned Time Series)

```Python
 .inUnitOfMeasure(CommonUnitOfMeasure.kWh)
```

#### AggregationRule (for Actual and Versioned Time Series)

```Python
 .withAggregationRule(AggregationRule.SumAndDivide)
```

## Write Data in Artesian

Using the MarketDataService is possible to register MarketData and write curves into it using the UpsertData method.

Depending on the Type of the MarketData, the UpsertData should be composed as per example below.

### Write Data in an Actual Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from Artesian.MarketData import AggregationRule
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.name,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.ActualTimeSerie,
      originalTimezone="CET",
      aggregationRule=AggregationRule.AverageAndReplicate,
      tags={
        'TestSDKPython': ['PythonValue2']
      },
      derivedCfg=DerivedCfg(
                version=1,
                derivedAlgorithm=DerivedAlgorithm.Coalesce,
                orderedReferencedMarketDataIds=[10000, 10001, 10002],
            ),
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)

data = MarketData.UpsertData(mkdid, 'CET',
  rows=
  {
      datetime(2020,1,1): 42.0,
      datetime(2020,1,2): 43.0,
  },
  downloadedAt=datetime(2020,1,3).replace(tzinfo=tz.UTC)
  )

mkservice.upsertData(data)
```

Upsert has optional switches that can be applied
```
mkservice.upsertData(data, deferCommandExecution, deferDataGeneration, keepNulls, upsertMode)
```
The switch details are,

deferCommandExecution (true/false) choose between syncronoys and asyncronous command execution, default is false.
deferDataGeneration (true/false) choose between syncronoys and asyncronous precomputed data generation, default is true.
keepNulls (true/false) if true then nulls are written in the curve replacing any data present for the instant, default is false.
upsertMode (Merge/Replace) for ActualTimeSeries the two modes are equivalent. Leaving Null/None/Empty is equivalent to Merge.


DerivedCfg can be of algorithm type: Coalesce, Sum, Muv.

Updating the DerivedCfg can be performed with `updateDerivedConfiguration` on MarketDataService. A validation will be done on the existing DerivedCfg of the MarketData, that should be not null and with same type as the one used for the update.

```csharp
derivedCfgUpdate = DerivedCfg(
    version=1,
    derivedAlgorithm=DerivedAlgorithm.Coalesce,
    orderedReferencedMarketDataIds=[10002, 10001, 10000],
)

marketDataUpdated = mkdservice.updateDerivedConfiguration(
                        registeredDerived.marketDataId,
                        derivedCfgUpdate,
                        False)
```

In case we want to write an hourly (or lower) time series the timezone for the upsert data must be UTC:

```Python
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.name,
      originalGranularity=Granularity.Hour,
      type=MarketData.MarketDataType.ActualTimeSerie,
      originalTimezone="CET",
      aggregationRule=AggregationRule.AverageAndReplicate,
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)

data = MarketData.UpsertData(mkdid, 'UTC',
  rows=
  {
      datetime(2020,1,1,5,0,0): 42.0,
      datetime(2020,1,2,6,0,0): 43.0,
      datetime(2020,1,2,7,0,0): 44.0,
      datetime(2020,1,2,8,0,0): 45.0,
      datetime(2020,1,2,9,0,0): 46.0,
  },
  downloadedAt=datetime(2020,1,3).replace(tzinfo=tz.UTC)
  )

mkservice.upsertData(data)

```

### Write Data in a Versioned Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from Artesian.MarketData import AggregationRule
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.name,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.VersionedTimeSerie,
      originalTimezone="CET",
      aggregationRule=AggregationRule.AverageAndReplicate,
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)

data = MarketData.UpsertData(mkdid, 'CET',
  rows=
  {
      datetime(2020,1,1): 42.0,
      datetime(2020,1,2): 43.0,
  },
  version= datetime(2020,1,3,12,0),
  downloadedAt=datetime(2020,1,3).replace(tzinfo=tz.UTC)
  )

mkservice.upsertData(data)

```

Upsert has optional switches that can be applied
```
mkservice.upsertData(data, deferCommandExecution, deferDataGeneration, keepNulls, upsertMode)
```
The switch details are,

deferCommandExecution (true/false) choose between syncronoys and asyncronous command execution, default is false.
deferDataGeneration (true/false) choose between syncronoys and asyncronous precomputed data generation, default is true.
keepNulls (true/false) if true then nulls are written in the curve replacing any data present for the instant, default is false.
upsertMode (Merge/Replace) for VersionedTimeSeries the merge writes in to the curve replacing existing data for an existing instant, replace writes the payload removing any previous data for the version. Leaving Null/None/Empty is equivalent to Merge.

| DATETIME | EXISTING | PAYLOAD | MERGE | REPALACE |
|---|---|---|---|---|
| VERSION NAME | 2025-01-01 | 2025-01-01 | 2025-01-01 | 2025-01-01 |
| 2025-01-01 |        |        |        |        |
| 2025-01-02 | 999.99 | 222.22 | 222.22 | 222.22 |
| 2025-01-03 | 999.99 | 222.22 | 222.22 | 222.22 |
| 2025-01-04 | 999.99 | 222.22 | 222.22 | 222.22 |
| 2025-01-05 | 999.99 | 222.22 | 222.22 | 222.22 |
| 2025-01-06 | 999.99 | 222.22 | 222.22 | 222.22 |
| 2025-01-07 | 999.99 | 222.22 | 222.22 | 222.22 |
| 2025-01-08 |        | 222.22 | 222.22 | 222.22 |
| 2025-01-09 |        |        |        |        |
| 2025-01-10 |        |        |        |        |
| 2025-01-11 | 999.99 |        | 999.99 |        |
| 2025-01-12 | 999.99 |        | 999.99 |        |
| 2025-01-13 | 999.99 |        | 999.99 |        |
| 2025-01-14 |        |        |        |        |
| 2025-01-15 |        |        |        |        |


### Write Data in a Market Assessment Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.name,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.MarketAssessment,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)

marketAssessment = MarketData.UpsertData(MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME'), 'CET',
  marketAssessment=
  {
      datetime(2020,1,1):
      {
         "Feb-20": MarketData.MarketAssessmentValue(open=10.0, close=11.0),
         "Mar-20": MarketData.MarketAssessmentValue(open=20.0, close=21.0)
      },
          datetime(2020,1,2):
          {
              "Feb-20": MarketData.MarketAssessmentValue(open=11.0, close=12.0),
              "Mar-20": MarketData.MarketAssessmentValue(open=21.0, close=22.0)
          }
  },
  downloadedAt=datetime(2020,1,3).replace(tzinfo=tz.UTC)
  )

mkservice.upsertData(marketAssessment)

```

Upsert has optional switches that can be applied
```
mkservice.upsertData(data, deferCommandExecution, deferDataGeneration, keepNulls, upsertMode)
```
The switch details are,

deferCommandExecution (true/false) choose between syncronoys and asyncronous command execution, default is false.
deferDataGeneration (true/false) choose between syncronoys and asyncronous precomputed data generation, default is true.
keepNulls (true/false) if true then nulls are written in the curve replacing any data present for the instant, default is false.
upsertMode (Merge/Replace) for MarketAssessment merge adds the new products to the existing and overwrites existing with the new ones while replace replaces all the existing products with the new ones. Leaving Null/None/Empty is equivalent to Merge.


### Write Data in a Bid Ask Time Series

```Python
from Artesian import ArtesianConfig,Granularity,MarketData
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.name,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.BidAsk,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)

bidAsk = MarketData.UpsertData(MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME'), 'CET',
  bidAsk={
      datetime(2020,1,1):
      {
          "Feb-20":MarketData.BidAskValue(bestBidPrice=15.0, lastQuantity=14.0),
          "Mar-20":MarketData.BidAskValue(bestBidPrice=25.0, lastQuantity=24.0)
      },
      datetime(2020,1,2):
      {
          "Feb-20":MarketData.BidAskValue(bestBidPrice=15.0, lastQuantity=14.0),
          "Mar-20":MarketData.BidAskValue(bestBidPrice=25.0, lastQuantity=24.0)
      }

  },
  downloadedAt=datetime(2020,1,3).replace(tzinfo=tz.UTC)
  )

mkservice.upsertData(bidAsk)
```

Upsert has optional switches that can be applied
```
mkservice.upsertData(data, deferCommandExecution, deferDataGeneration, keepNulls, upsertMode)
```
The switch details are,

deferCommandExecution (true/false) choose between syncronoys and asyncronous command execution, default is false.
deferDataGeneration (true/false) choose between syncronoys and asyncronous precomputed data generation, default is true.
keepNulls (true/false) if true then nulls are written in the curve replacing any data present for the instant, default is false.
upsertMode (Merge/Replace) for BidAsk merge adds the new products to the existing and overwrites existing with the new ones while replace replaces all the existing products with the new ones. Leaving Null/None/Empty is equivalent to Merge.


### Write Data in an Auction Time Series

```Python
from Artesian import ArtesianConfig,Granularity,MarketData
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.name,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.Auction,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

registered = mkservice.readMarketDataRegistryByName(mkdid.provider, mkdid.name)
if (registered is None):
  registered = mkservice.registerMarketData(mkd)

auctionRows = MarketData.UpsertData(MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME'), 'CET',
  auctionRows={
      datetime(2020,1,1): MarketData.AuctionBids(datetime(2020,1,1),
          bid=[
              MarketData.AuctionBidValue(11.0, 12.0),
              MarketData.AuctionBidValue(13.0, 14.0),
          ],
          offer=[
              MarketData.AuctionBidValue(21.0, 22.0),
              MarketData.AuctionBidValue(23.0, 24.0),
          ]
      )
  },
  downloadedAt=datetime(2020,1,3).replace(tzinfo=tz.UTC)
  )

  mkservice.upsertData(auctionRows)

```

Upsert has optional switches that can be applied
```
mkservice.upsertData(data, deferCommandExecution, deferDataGeneration, keepNulls, upsertMode)
```
The switch details are,

deferCommandExecution (true/false) choose between syncronoys and asyncronous command execution, default is false.
deferDataGeneration (true/false) choose between syncronoys and asyncronous precomputed data generation, default is true.
keepNulls (true/false) if true then nulls are written in the curve replacing any data present for the instant, default is false.
upsertMode (Merge/Replace) for Auction merge and replace are equivalent. Leaving Null/None/Empty is equivalent to Merge.


## Delete Data in Artesian

Using the MarketDataService is possible to delete MarketData and its curves.

### Delete MarketData in Artesian

Using the MarketDataService is possible to delete MarketData and its curves.

```Python

from Artesian import ArtesianConfig
from Artesian.MarketData import MarketDataService

cfg = ArtesianConfg()
mkservice = MarketDataService(cfg)

mkservice.deleteMarketData(100042422)

```

Depending on the Type of the MarketData, the DeletData should be composed as per example below. The timezone is optional: for DateSeries if provided must be equal to MarketData OriginalTimezone Default:MarketData OriginalTimezone. For TimeSeries Default:CET

### Delete Data in an Actual Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from Artesian.MarketData import AggregationRule
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
deleteData = MarketData.DeleteData(
    ID=mkdid,
    timezone='CET',
    rangeStart=datetime(2020, 1, 1, 6),
    rangeEnd=datetime(2020, 1, 1, 18),
)

mkdservice.deleteData(deleteData)
```

### Delete Data in an Versioned Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from Artesian.MarketData import AggregationRule
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
deleteData = MarketData.DeleteData(
    ID=mkdid,
    timezone='CET',
    rangeStart=datetime(2020, 1, 1, 0),
    rangeEnd=datetime(2020, 1, 7, 0),
    version=datetime(2020, 1, 1, 0)
)

mkdservice.deleteData(deleteData)
```

### Delte Data in a Market Assessment Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
deleteData = MarketData.DeleteData(
    ID= mkdid,
    timezone='CET',
    rangeStart=datetime(2020, 1, 1, 0),
    rangeEnd=datetime(2020, 1, 3, 0),
    product=["Feb-20"]
)

mkdservice.deleteData(deleteData)
```

### Delte Data in a Bid Ask Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
deleteData = MarketData.DeleteData(
    ID= mkdid,
    timezone='CET',
    rangeStart=datetime(2020, 1, 1, 0),
    rangeEnd=datetime(2020, 1, 3, 0),
    product=["Feb-20"]
)

mkdservice.deleteData(deleteData)
```

### Delete Data in an Auction Time Series

```Python
from Artesian import ArtesianConfig, Granularity, MarketData
from Artesian.MarketData import AggregationRule
from datetime import datetime
from dateutil import tz

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'MARKETDATANAME')
deleteData = MarketData.DeleteData(
    ID=mkdid,
    timezone='CET',
    rangeStart=datetime(2020, 1, 1, 6),
    rangeEnd=datetime(2020, 1, 1, 18),
)

mkdservice.deleteData(deleteData)
```

## Jupyter Support

Artesian SDK uses asyncio internally, this causes a conflict with Jupyter. You can work around this issue by add the following at the beginning of the notebook.

```python

!pip install nest_asyncio

import nest_asyncio
nest_asyncio.apply()


```

[Issue #3397 with workaround](https://github.com/jupyter/notebook/issues/3397#issuecomment-419386811)

## Links

- [Github](https://github.com/ARKlab/Artesian.SDK-Python)
- [Ark Energy](http://www.ark-energy.eu/)
- [Artesian Portal](https://portal.artesian.cloud)
