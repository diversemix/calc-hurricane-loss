from .hurricane_region import HurricaneRegions
from .hurricane_model import HurricaneModel
from .loss_result import LossResult


class HurricaneCalculator:
    """
    The main calculator for the application.

    Responsibility - to store the hurricane data for regions for calculation of loss
    """

    def __init__(self, log, model: HurricaneModel, regions: HurricaneRegions):
        self.regions = regions
        self.model = model
        self.log = log

    def gethurricaneloss(self, n_years: int) -> LossResult:
        result = LossResult()

        for year in range(n_years):
            year_loss = 0
            for region in self.regions:
                events = self.model.fn_event_model(region.event_rate)
                loss = self.model.fn_loss_model(region.loss_mean, region.loss_stddev, events)
                year_loss += sum(loss)
                self.log.debug("{:10}: Year={}, Events={}, Loss={}".format(region.name, year, events, year_loss))
            result.add_annual_loss(year_loss)

        return result
