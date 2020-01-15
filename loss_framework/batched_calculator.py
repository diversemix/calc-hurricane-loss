import multiprocessing
import logging
from dataclasses import dataclass
from typing import List
from .loss_result import LossResult
from .calculator import Calculator


@dataclass
class BatchArgument:
    size: int
    calc: Calculator


def get_batch_result(args: BatchArgument) -> LossResult:
    return args.calc.get_loss(args.size)


class BatchedCalculator:
    """
    BatchedCalculator - Batches up the loss calculation over a number of Processes
    """
    def __init__(self, log: logging.Logger, calc: Calculator):
        self.calc = calc
        self.log = log

    def get_loss(self, num_monte_carlo_samples: int) -> LossResult:
        batches = self.get_batches(num_monte_carlo_samples)
        self.log.debug('Found {} CPUs. Using batches {} '.format(len(batches), batches))

        args = [BatchArgument(b, self.calc) for b in batches]

        with multiprocessing.Pool(len(batches)) as pool:
            results = pool.map(get_batch_result, args)

        total_loss = sum([r.total_loss for r in results if r])
        total_years = sum([r.num_years for r in results if r])
        return LossResult(total_years, total_loss)

    def get_batches(self, num_monte_carlo_samples: int) -> List[int]:
        cpu_count = multiprocessing.cpu_count()
        batch_size = int(num_monte_carlo_samples / cpu_count)
        batches = [batch_size for _ in range(cpu_count - 1)]
        last_size = num_monte_carlo_samples - (batch_size * (cpu_count - 1))
        batches.append(last_size)
        return batches
