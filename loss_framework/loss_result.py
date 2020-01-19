from dataclasses import dataclass


@dataclass
class LossResult:
    """
    LossResult - Responsible for keeping the current result coherent (mathamatically).
    """
    num_years: int = 0
    total_loss: float = 0

    def add_annual_loss(self, loss: float) -> None:
        self.num_years += 1
        self.total_loss += loss

    def __str__(self) -> str:
        if self.num_years:
            return "Mean loss = {:.3f} per year calculated over {} years.".format(self.total_loss / self.num_years, self.num_years)
        else:
            return "No result"
