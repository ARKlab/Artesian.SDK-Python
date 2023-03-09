from enum import Enum


class GenerationType(Enum):
    UNKNOWN = 1
    OTHER = 2
    AUTOGENERATION = 3
    BIOMASS = 4
    COAL = 5
    WIND = 6
    PV = 7
    GAS = 8
    GASOIL = 9
    THERMAL = 10
    HYDRO = 11
    MIXED = 12
    OIL = 13
