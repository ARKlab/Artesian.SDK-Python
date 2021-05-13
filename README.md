![image](http://www.ark-energy.eu/wp-content/uploads/ark-dark.png)
# Artesian.SDK

This Library provides read access to the Artesian API

## Getting Started
### Installation
You can install the package directly from [pip](https://pypi.org/project/artesian-sdk/).
```Python
pip install artesian-sdk
```
Alternatively, to install this package go to the [release page](https://github.com/ARKlab/Artesian.SDK-Python/releases)  .

## How to use
The Artesian.SDK instance can be configured using API-Key authentication
```Python
from Artesian import *

cfg = ArtesianConfig("https://fake-artesian-env/", "{api-key}")
```

## QueryService
Using the ArtesianConfig `cfg` we create an instance of the QueryService which is used to create Actual, Versioned and Market Assessment time series queries

### Actual Time Series
```Python
from Artesian import *

qs = QueryService(cfg);
data = qs.createActual() \
    .forMarketData([100011484,100011472,100011477,100011490,100011468,100011462,100011453]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.HOUR) \
    .execute()

```
To construct an Actual Time Series the following must be provided.
<table>
  <tr><th>Actual Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Time Granularity</td><td>Specify the granularity type</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Versioned Time Series
```Python
from Artesian import *

qs = QueryService(cfg);
q = qs.createVersioned() \
    .forMarketData([100042422,100042283,100042285,100042281,100042287,100042291,100042289]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.HOUR)


q.forMUV().execute()
q.forLastNVersions(2).execute()
q.forLastOfDays("2019-03-12","2019-03-16").execute()
q.forLastOfDays("P0Y0M-2D","P0Y0M2D").execute()
q.forLastOfDays("P0Y0M-2D").execute()
q.forLastOfMonths("2019-03-12","2019-03-16").execute()
q.forLastOfMonths("P0Y-1M0D","P0Y1M0D").execute()
q.forLastOfMonths("P0Y-1M0D").execute()
q.forVersion("2019-03-12T14:30:00").execute()
q.test1.forMostRecent("2019-03-12","2019-03-16").execute()
q.test1.forMostRecent("P0Y0M-2D","P0Y0M2D").execute()
q.test1.forMostRecent("P0Y0M-2D").execute()
q.test1.forMostRecent("2019-03-12","2019-03-16").execute()
q.test1.forMostRecent("P0Y-1M0D","P0Y1M0D").execute()
q.test1.forMostRecent("P0Y-1M0D").execute() 
```
To construct a Versioned Time Series the following must be provided.
<table>
  <tr><th>Versioned Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Time Granularity</td><td>Specify the granularity type</td></tr>
  <tr><td>Versioned Time Extraction Window</td><td>Versioned extraction time window</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Market Assessment Time Series
```Python
from Artesian import *

qs = QueryService(cfg);
data = qs.createMarketAssessment() \
    .forMarketData([100000032,100000043]) \
    .forProducts(["D+1","Feb-18"]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .execute()
```
To construct a Market Assessment Time Series the following must be provided.
<table>
  <tr><th>Mas Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Product</td><td>Provide a product or set of products</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried </td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Bid Ask Time Series
```Python
from Artesian import *

qs = QueryService(cfg);
data = qs.createBidAsk() \
    .forMarketData([100000032,100000043]) \
    .forProducts(["D+1","Feb-18"]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .execute()
```
To construct a Bid Ask Time Series the following must be provided.
<table>
  <tr><th>Mas Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Product</td><td>Provide a product or set of products</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried </td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Auction Time Series
```Python
from Artesian import *

qs = QueryService(cfg);
data = qs.createAuction() \
    .forMarketData([100011484,100011472,100011477,100011490,100011468,100011462,100011453]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .execute()

```
To construct an Auction Time Series the following must be provided.
<table>
  <tr><th>Auction Query</th><th>Description</th></tr>
  <tr><td>Market Data ID</td><td>Provide a market data id or set of market data id's to query</td></tr>
  <tr><td>Time Extraction Window</td><td>An extraction time window for data to be queried</td></tr>
</table>

[Go to Time Extraction window section](#artesian-sdk-extraction-windows)

### Artesian SDK Extraction Windows
Extraction window types  for queries.

Date Range
```Python
 .inAbsoluteDateRange("2018-08-01", "2018-08-10")
```
Relative Interval
```Python
 .inRelativeInterval(RelativeInterval.ROLLING_WEEK)
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

Null

```python
 .withFillNull()
```

None

```python
 .withFillNone()
```

Custom Value

```python
 //Timeseries
 .withFillCustomValue(123)
 // Market Assessment
 .withFillCustomValue(
    settlement = 123,
    open = 456,
    close = 789,
    high = 321,
    low = 654,
    volumePaid = 987,
    volueGiven = 213,
    volume = 435,
  )
```

Latest Value

```python
 .withFillLatestValue("P5D")
```


## MarketData Service

Using the ArtesianServiceConfig `cfg` we create an instance of the MarketDataService which is used to retrieve MarketData infos.

```Python
from Artesian import *

mds = MarketDataService(cfg);

```

To list MarketData curves
```Python
page = 1
pageSize = 100
res = mds.readCurveRange(100042422, page, pageSize, versionFrom="2016-12-20" , versionTo="2019-03-12")
```


## Links
* [Github](https://github.com/ARKlab/Artesian.SDK-Python)
* [Ark Energy](http://www.ark-energy.eu/)
* [Artesian Portal](https://portal.artesian.cloud)
