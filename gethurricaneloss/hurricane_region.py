from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class HurricaneRegion:
    name: str
    landfall_rate: int
    mean: float
    stddev: float
