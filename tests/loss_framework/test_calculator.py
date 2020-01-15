import logging
from typing import List
from loss_framework import Calculator, EventModel, EventRegion, LossResult


def dummy_event_model(rate: int) -> int:
    return 0


def dummy_loss_model(mean: int, stddev: int, events: int) -> List[int]:
    return [0]


def test_construct() -> None:
    c = Calculator(logging.getLogger(),
                   EventModel(dummy_event_model, dummy_loss_model),
                   [EventRegion('blank', 0, 0, 0)])

    assert c.get_loss(1) == LossResult(1, 0)
