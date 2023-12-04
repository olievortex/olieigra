"""Model for an Igra2 body record"""
from dataclasses import dataclass


@dataclass
class BodyModel:
    """Model for an Igra2 body record"""
    type: str
    pres: int
    gph: float
    temp: float
    rh: float
    dpdp: float
    wdir: float
    wspd: float
