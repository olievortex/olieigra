"""Model for an Igra2 header record"""
from dataclasses import dataclass


@dataclass
class HeaderModel:
    """Model for an Igra2 header record"""
    id: str
    year: int
    month: int
    day: int
    hour: int
    reltime: int
    numlev: int
    p_src: str
    np_src: str
    lat: int
    lon: int
