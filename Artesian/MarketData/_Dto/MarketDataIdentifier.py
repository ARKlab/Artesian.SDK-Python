from dataclasses import dataclass

@dataclass
class MarketDataIdentifier:
    provider:str
    name:str