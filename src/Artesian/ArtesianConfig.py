from __future__ import annotations


class ArtesianConfig:
    """
    The Artesian.SDK instance can be configured using API-Key authentification

    Attributes:
       baseUrl:
         should be https://arkive.artesian.cloud/{tenantName}/,
         the link that can be found in Artesian UI when selecting a curve to extract

       apiKey:
          the key to use to authenticate
          can be created from the Artesian UI.
    """

    def __init__(self: ArtesianConfig, baseUrl: str, apiKey: str) -> None:
        """
        Inits Artesian Config with overrides.

          Args:
            baseUrl: A str ussed to control the environment to connect to.
              https://arkive.artesian.cloud/{tenantName}/

            apiKey: A str that is the API-Key.
        """
        self.baseUrl = baseUrl
        self.apiKey = apiKey
