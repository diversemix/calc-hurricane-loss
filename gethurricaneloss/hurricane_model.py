from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, order=True)
class HurricaneModel:
    """
    HurricaneModel - Representation for data needed to describe a region's hurricane susceptibility.
    """
    fn_event_model: Any
    fn_loss_model: Any
