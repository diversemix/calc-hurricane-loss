from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, order=True)
class EventModel:
    """
    EventModel - Representation for data needed to describe a region's susceptibility to an event.
    """
    fn_event_model: Any
    fn_loss_model: Any
