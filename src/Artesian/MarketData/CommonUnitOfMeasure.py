from dataclasses import dataclass


@dataclass(frozen=True)
class CommonUnitOfMeasure:
    kW = "kW"
    MW = "MW"
    kWh = "kWh"
    MWh = "MWh"
    m = "m"
    km = "km"
    day = "day"
    min = "min"
    h = "h"
    s = "s"
    mo = "mo"
    yr = "yr"
