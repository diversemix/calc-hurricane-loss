import logging
from .loss_result import LossResult
from .event_model import EventModel
from .event_region import EventRegions


class Calculator:
    """
    The main calculator for the application.

    Responsibility - to store the hurricane data for regions for calculation of loss
    """

    def __init__(self, log: logging.Logger, model: EventModel, regions: EventRegions):
        self.regions = regions
        self.model = model
        self.log = log

    def get_loss(self, n_years: int) -> LossResult:
        result = LossResult()
        isLogging = self.log.isEnabledFor(logging.DEBUG)

        for year in range(n_years):
            year_loss = 0
            for region in self.regions:
                events = self.model.fn_event_model(region.event_rate)
                loss = self.model.fn_loss_model(region.loss_mean, region.loss_stddev, events)
                loss_total = sum(loss)
                year_loss += loss_total
                if isLogging:
                    self.log.debug("{:10}: Year={}, Events={}, Loss={}".format(region.name, year, events, loss_total))
            result.add_annual_loss(year_loss)

        return result
