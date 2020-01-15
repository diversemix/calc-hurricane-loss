import logging
import multiprocessing
import click
from typing import List
import numpy as np

from .hurricane_calculator import HurricaneCalculator
from .hurricane_region import HurricaneRegion
from .hurricane_model import HurricaneModel
from .loss_result import LossResult

SAMPLE_THRESHOLD = 20000


@click.command()
@click.option('-n', '--num_monte_carlo_samples', default=1, help='Number of simulation years.', type=int)
@click.option('-v/-i', '--verbose/--info', default=False, help='Enables debug logging.')
@click.argument('florida_landfall_rate', nargs=1, type=int)
@click.argument('florida_mean', nargs=1, type=float)
@click.argument('florida_stddev', nargs=1, type=float)
@click.argument('gulf_landfall_rate', nargs=1, type=int)
@click.argument('gulf_mean', nargs=1, type=float)
@click.argument('gulf_stddev', nargs=1, type=float)
def main(num_monte_carlo_samples, verbose,
         florida_landfall_rate, florida_mean, florida_stddev,
         gulf_landfall_rate, gulf_mean, gulf_stddev):
    """
    The main function for the 'gethurricaneloss' application.

    Responsibility - to unpack any command line arguments, consturct the regions and the model
    then construct an appropriate calculator to calculate the total loss.
    """
    regions = [
        HurricaneRegion('florida', florida_landfall_rate, florida_mean, florida_stddev),
        HurricaneRegion('gulf', gulf_landfall_rate, gulf_mean, gulf_stddev),
    ]

    model = HurricaneModel(np.random.poisson, np.random.lognormal)
    log = create_logger(logging.DEBUG if verbose else logging.INFO)

    log.debug("Hurricane Regions: {}".format(regions))
    log.debug("Hurricane Models: {}".format(model))

    c = HurricaneCalculator(log, model, regions)

    if num_monte_carlo_samples < SAMPLE_THRESHOLD:
        result = c.gethurricaneloss(num_monte_carlo_samples)
        log.info(result)
    else:
        log.info('Argument num_monte_carlo_samples exceeds the threshold for a simple calculation - this may take some time...')
        batches = get_batches(num_monte_carlo_samples)
        log.info('Found {} CPUs. Using batches {} '.format(len(batches), batches))

        args = [(b, c) for b in batches]

        with multiprocessing.Pool(len(batches)) as pool:
            results = pool.map(get_batch_result, args)

        total_loss = sum([r.total_loss for r in results])
        total_years = sum([r.num_years for r in results])
        total = LossResult(total_years, total_loss)
        log.info(total)


def get_batch_result(arg):
    batch_size = arg[0]
    calculator = arg[1]
    return calculator.gethurricaneloss(batch_size)


def create_logger(log_level: int) -> logging.Logger:
    log = logging.getLogger("gethurricaneloss")
    ch = logging.StreamHandler()
    log.addHandler(ch)
    log.setLevel(log_level)
    return log


def get_batches(num_monte_carlo_samples: int) -> List[int]:
    cpu_count = multiprocessing.cpu_count()
    batch_size = int(num_monte_carlo_samples / cpu_count)
    batches = [batch_size for _ in range(cpu_count - 1)]
    last_size = num_monte_carlo_samples - (batch_size * (cpu_count - 1))
    batches.append(last_size)
    return batches


if __name__ == '__main__':
    main()
