import logging
import multiprocessing as mp
from typing import List
from loss_framework import Calculator, BatchedCalculator, EventModel, EventRegion, LossResult


def dummy_event_model(rate: int) -> int:
    return 0


def dummy_loss_model(mean: int, stddev: int, events: int) -> List[int]:
    return [0]


def test_construct() -> None:
    log = logging.getLogger()
    c = Calculator(log,
                   EventModel(dummy_event_model, dummy_loss_model),
                   [EventRegion('blank', 0, 0, 0)])
    bc = BatchedCalculator(log, c)

    assert bc.get_loss(40) == LossResult(40, 0)


def test_get_batches() -> None:
    log = logging.getLogger()
    c = Calculator(log,
                   EventModel(dummy_event_model, dummy_loss_model),
                   [EventRegion('blank', 0, 0, 0)])
    bc = BatchedCalculator(log, c)
    batches = bc.get_batches(41)

    assert len(batches) == mp.cpu_count()
    assert sum(batches) == 41
