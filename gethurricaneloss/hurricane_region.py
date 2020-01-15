from typing import List
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class HurricaneRegion:
    """
    HurricaneRegion - Representation for data needed to describe a region's hurricane susceptibility.
    """
    name: str
    event_rate: int     # landfall rate
    loss_mean: float
    loss_stddev: float

    def __repr__(self):
        return " <Region: {}, Rate: {}, Mean {}, StdDev {}> ".format(self.name, self.event_rate, self.loss_mean, self.loss_stddev)


HurricaneRegions = List[HurricaneRegion]
