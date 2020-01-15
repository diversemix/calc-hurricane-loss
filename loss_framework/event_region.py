from typing import List
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class EventRegion:
    """
    EventRegion - Representation for data needed to describe a region's occurances of an event.
    """
    name: str
    event_rate: int     # landfall rate
    loss_mean: float
    loss_stddev: float

    def __repr__(self) -> str:
        return " <Region: {}, Rate: {}, Mean {}, StdDev {}> ".format(self.name, self.event_rate, self.loss_mean, self.loss_stddev)


EventRegions = List[EventRegion]
