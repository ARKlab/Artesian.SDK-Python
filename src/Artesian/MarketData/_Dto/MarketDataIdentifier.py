from dataclasses import dataclass


@dataclass
class MarketDataIdentifier:
    """
    Class for the Market Data Identifier.

    Attributes:
        provider: the Market Data Identifier by provider
        name: the Market Data Identifier by name
    """

    provider: str
    name: str
