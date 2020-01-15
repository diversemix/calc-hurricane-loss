import logging
import click
import numpy as np

from loss_framework import (
    Calculator,
    BatchedCalculator,
    EventRegion,
    EventModel,
    LossResult
)


@click.command()
@click.option('-n', '--num_monte_carlo_samples', default=1, help='Number of simulation years.', type=int)
@click.option('-v/-i', '--verbose/--info', default=False, help='Enables debug logging.')
@click.option('-m/-s', '--multicpu/--singlecpu', default=False, help='Enables use of multipe CPUs.')
@click.argument('florida_landfall_rate', nargs=1, type=int)
@click.argument('florida_mean', nargs=1, type=float)
@click.argument('florida_stddev', nargs=1, type=float)
@click.argument('gulf_landfall_rate', nargs=1, type=int)
@click.argument('gulf_mean', nargs=1, type=float)
@click.argument('gulf_stddev', nargs=1, type=float)
def main(num_monte_carlo_samples: int, verbose: bool, multicpu: bool,
         florida_landfall_rate: int, florida_mean: float, florida_stddev: float,
         gulf_landfall_rate: int, gulf_mean: float, gulf_stddev: float) -> int:
    """
    The main function for the 'gethurricaneloss' application.

    Responsibility - to unpack any command line arguments, consturct the regions and the model
    then pass them into the loss-framework's calculator to calculate the total loss.
    """
    result = gethurricaneloss(num_monte_carlo_samples, verbose, multicpu,
                              florida_landfall_rate, florida_mean, florida_stddev,
                              gulf_landfall_rate, gulf_mean, gulf_stddev)
    print(result)
    return 0


def gethurricaneloss(num_monte_carlo_samples: int, verbose: bool, multicpu: bool,
                     florida_landfall_rate: int, florida_mean: float, florida_stddev: float,
                     gulf_landfall_rate: int, gulf_mean: float, gulf_stddev: float) -> LossResult:

    regions = [
        EventRegion('florida', florida_landfall_rate, florida_mean, florida_stddev),
        EventRegion('gulf', gulf_landfall_rate, gulf_mean, gulf_stddev),
    ]

    model = EventModel(np.random.poisson, np.random.lognormal)
    log = create_logger(logging.DEBUG if verbose else logging.INFO)

    log.debug("Hurricane Regions: {}".format(regions))
    log.debug("Hurricane Models: {}".format(model))

    c = Calculator(log, model, regions)
    result = None
    if multicpu:
        bc = BatchedCalculator(log, c)
        result = bc.get_loss(num_monte_carlo_samples)
    else:
        result = c.get_loss(num_monte_carlo_samples)

    return result


def create_logger(log_level: int) -> logging.Logger:
    log = logging.getLogger("gethurricaneloss")
    ch = logging.StreamHandler()
    log.addHandler(ch)
    log.setLevel(log_level)
    return log


if __name__ == '__main__':
    main()
