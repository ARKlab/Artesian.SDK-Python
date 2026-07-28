from Artesian import ArtesianConfig
from Artesian.MarketData import *

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = MarketDataService(cfg)

res = mkdservice.searchFacet(
    1,
    1,
    "Riconsegnato_",
    filters={"ProviderName": ["SNAM", "France"]},
    sorts=["MarketDataId asc"],
    doNotLoadAdditionalInfo=False,
)

print(res.results)

res1 = mkdservice.searchFacet(1, 1, "Riconsegnato_")

print(res1.results)

res2 = mkdservice.searchFacet(1, 1, "Riconsegnato_", doNotLoadAdditionalInfo=True)

print(res2.results)

print("Test completed")
