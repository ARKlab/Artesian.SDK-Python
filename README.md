![image](https://www.ark-energy.eu/wp-content/uploads/ark-dark.png)
# Artesian.SDK

This Library provides read access to the Artesian API

## Getting Started
### Installation
You can install the package directly from [pip](https://pypi.org/project/artesian-sdk/).
```Python
pip install artesian-sdk
```
Alternatively, to install this package go to the [release page](https://github.com/ARKlab/Artesian.SDK-Python/releases)  .

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

## QueryService
Using the ArtesianConfig `cfg` we create an instance of the QueryService which is used to create Actual, Versioned and Market Assessment time series queries

### Actual Time Series
```Python
from Artesian import Granularity
from Artesian.Query import QueryService

qs = QueryService(cfg)
data = qs.createActual() \
    .forMarketData([100011484,100011472,100011477,100011490,100011468,100011462,100011453]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Hour) \
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
from Artesian import Granularity
from Artesian.Query import QueryService

qs = QueryService(cfg)
q = qs.createVersioned() \
    .forMarketData([100042422,100042283,100042285,100042281,100042287,100042291,100042289]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.Hour)


q.forMuv().execute()
q.forLastNVersions(2).execute()
q.forLastOfDays("2019-03-12","2019-03-16").execute()
q.forLastOfDays("P0Y0M-2D","P0Y0M2D").execute()
q.forLastOfDays("P0Y0M-2D").execute()
q.forLastOfMonths("2019-03-12","2019-03-16").execute()
q.forLastOfMonths("P0Y-1M0D","P0Y1M0D").execute()
q.forLastOfMonths("P0Y-1M0D").execute()
q.forVersion("2019-03-12T14:30:00").execute()
q.forMostRecent("2019-03-12","2019-03-16").execute()
q.forMostRecent("2019-03-12T12:30:05","2019-03-16T18:42:30").execute()
q.forMostRecent("P0Y0M-2D","P0Y0M2D").execute()
q.forMostRecent("P0Y0M-2D").execute()
q.forMostRecent("2019-03-12","2019-03-16").execute()
q.forMostRecent("P0Y-1M0D","P0Y1M0D").execute()
q.forMostRecent("P0Y-1M0D").execute() 
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

qs = Query.QueryService(cfg)
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
from Artesian.Query import QueryService

qs = QueryService(cfg)
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
from Artesian.Query import QueryService

qs = QueryService(cfg)
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

## Artesian SDK Extraction Windows
Extraction window types  for queries.

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

Latest Value to propagate the latest value, not older than a certain threshold.

```python
 .withFillLatestValue("P5D")
```

## Jupyter

Artesian SDK uses asyncio internally, this causes a conflict with Jupyter. You can work around this issue by add the following at the beginning of the notebook.

```python

!pip install nest_asyncio

import nest_asyncio
nest_asyncio.apply() 


```

[Issue #3397 with workaround](https://github.com/jupyter/notebook/issues/3397#issuecomment-419386811)

## Write Data in Artesian


Using the MarketDataService is possible to register MarketData and write curves into it using the UpsertData method.

Depending on the Type of the MarketData, the UpsertData should be composed as per example below.

### Write Data in a ActualTimeSerie

```Python
from Artesian import ArtesianConfig
from Artesian import ArtesianConfig,Granularity,MarketData
from dateutil import tz

cfg = ArtesianConfg()

mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.curveName,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.ActualTimeSerie,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

registered = mkservice.readMarketDataByName(mkdid.provider, mkdid.curveName)
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

### Write Data in a MarketAssessment

```Python
from Artesian import ArtesianConfig
from Artesian import ArtesianConfig,Granularity,MarketData
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.curveName,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.MarketAssessment,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

marketAssessment = MarketData.UpsertData(MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME'), 'CET', 
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

### Write Data in a BidAsk

```Python
from Artesian import ArtesianConfig
from Artesian import ArtesianConfig,Granularity,MarketData
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.curveName,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.BidAsk,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

bidAsk = MarketData.UpsertData(MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME'), 'CET', 
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

### Write Data in a Auction

```Python
from Artesian import ArtesianConfig
from Artesian import ArtesianConfig,Granularity,MarketData
from dateutil import tz

cfg = ArtesianConfg()
mkservice = MarketData.MarketDataService(cfg)

mkdid = MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME')
mkd = MarketData.MarketDataEntityInput(
      providerName = mkdid.provider,
      marketDataName = mkdid.curveName,
      originalGranularity=Granularity.Day,
      type=MarketData.MarketDataType.Auction,
      originalTimezone="CET",
      tags={
        'TestSDKPython': ['PythonValue2']
      }
  )

auctionRows = MarketData.UpsertData(MarketData.MarketDataIdentifier('PROVIDER', 'CURVENAME'), 'CET', 
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
## Delete Data in Artesian


Using the MarketDataService is possible to register MarketData and write curves into it using the UpsertData method.

Depending on the Type of the MarketData, the UpsertData should be composed as per example below.

```Python

from Artesian import ArtesianConfig
from Artesian.MarketData import MarketDataService

cfg = ArtesianConfg()
mkservice = MarketDataService(cfg)

mkservice.deleteMarketData(100042422)

```

## Query written Versions or Products

Using the ArtesianServiceConfig `cfg` we create an instance of the MarketDataService which is used to retrieve MarketData infos.

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


## Links
* [Github](https://github.com/ARKlab/Artesian.SDK-Python)
* [Ark Energy](http://www.ark-energy.eu/)
* [Artesian Portal](https://portal.artesian.cloud)
