from datetime import datetime, timezone
from uuid import uuid4

import Artesian
from Artesian.Granularity import Granularity
from Artesian.MarketData import (
    AggregationRule,
    MarketDataEntityInput,
    MarketDataIdentifier,
    MarketDataType,
    OverrideKind,
    UpsertCurveDataOverride,
    UpsertData,
)


# Run only manually with a valid Artesian URI and API key.
cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

marketDataService = Artesian.MarketData.MarketDataService(cfg)
queryService = Artesian.Query.QueryService(cfg)

marketDataId = None
overrideId = None

try:
    providerName = "MarketDataOverrideSample"
    marketDataName = "Override_" + str(uuid4())
    marketDataIdentifier = MarketDataIdentifier(providerName, marketDataName)

    marketDataInput = MarketDataEntityInput(
        providerName=providerName,
        marketDataName=marketDataName,
        type=MarketDataType.ActualTimeSerie,
        originalGranularity=Granularity.Day,
        originalTimezone="UTC",
        aggregationRule=AggregationRule.Undefined,
    )

    marketData = marketDataService.readMarketDataRegistryByName(
        providerName,
        marketDataName,
    )
    if marketData is None:
        marketData = marketDataService.registerMarketData(marketDataInput)

    marketDataId = marketData.marketDataId
    assert marketDataId is not None

    marketDataService.upsertData(
        UpsertData(
            ID=marketDataIdentifier,
            timezone="UTC",
            downloadedAt=datetime(2025, 1, 14, tzinfo=timezone.utc),
            rows={
                datetime(2025, 1, 1): 10.0,
                datetime(2025, 1, 3): 10.0,
                datetime(2025, 1, 5): 10.0,
            },
            deferCommandExecution=False,
            deferDataGeneration=False,
        )
    )

    upsertCurveDataOverride = UpsertCurveDataOverride(
        ID=marketDataIdentifier,
        overrideId=None,
        timezone="UTC",
        downloadedAt=datetime.now(timezone.utc),
        rows={
            datetime(2025, 1, 1): 11.5,
            datetime(2025, 1, 2): 12.5,
        },
        kind=OverrideKind.Override,
        replaceExisting=True,
        comment="SDK Market Data override sample",
        deferCommandExecution=False,
        deferDataGeneration=False,
    )

    createdMetadata = marketDataService.upsertCurveDataOverride(upsertCurveDataOverride)

    assert createdMetadata
    assert createdMetadata[0].id is not None
    assert createdMetadata[0].kind == OverrideKind.Override
    overrideId = createdMetadata[0].id

    effectiveData = (
        queryService.createActual()
        .forMarketData([marketDataId])
        .inGranularity(Granularity.Day)
        .inAbsoluteDateRange("2025-01-01", "2025-01-03")
        .inTimeZone("UTC")
        .execute()
    )
    print("Effective TS data after override:", effectiveData)

    metadata = marketDataService.readOverrideMetadata(
        marketDataId,
        OverrideKind.Override,
        page=1,
        pageSize=10,
    )
    assert metadata.data

    marketDataService.deleteOverrideData(overrideId)

    deletedMetadata = marketDataService.readOverrideMetadata(
        marketDataId,
        OverrideKind.Override,
        page=1,
        pageSize=10,
    )
    assert all(entry.id != overrideId for entry in deletedMetadata.data), (
        "The override metadata should not be returned after deletion."
    )

    print("Market data override sample completed")
finally:
    if marketDataId is not None:
        try:
            marketDataService.deleteMarketData(marketDataId)
        except Exception as ex:
            print(
                f"Best-effort cleanup failed for market data id {marketDataId}: {ex}"
            )
