from numpy import tri


class ArtesianConfig:
    """ 
     The Artesian.SDK instance can be configured using API-Key authentification
      
        Attributes:
            baseUrl:
              should be https://arkive.artesian.cloud/{tenantName}/,
              the link that can be found in Artesian UI when selecting a curve to extract
              
            apiKey:
              can be extract from the UI once logged-in. It is suggested to insert a description and check the "Never Expires" choice.
              The token can be used only once.
      """
    def __init__(self, baseUrl: str, apiKey: str) -> None:
        """
         Inits Artesian Config with overrides.
             
             Args:
                baseUrl: A str ussed to control the environment to connect to.
                  https://arkive.artesian.cloud/{tenantName}/

                apiKey: A str that is the bearer token obtained from the API-Key Configuration.
        """

        self.baseUrl = baseUrl
        self.apiKey = apiKey    


        