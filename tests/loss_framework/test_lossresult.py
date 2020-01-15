from loss_framework import LossResult


def test_constructs() -> None:
    lr = LossResult(1, 2)

    assert lr.num_years == 1
    assert lr.total_loss == 2


def test_output() -> None:
    lr = LossResult(10, 200)

    assert str(lr) == "Mean loss = 20.000 per year calculated over 10 years.", str(lr)


def test_no_output() -> None:
    lr = LossResult()

    assert str(lr) == "No result", str(lr)


def test_can_add() -> None:
    lr = LossResult(10, 200)
    lr.add_annual_loss(300)
    assert lr.num_years == 11
    assert lr.total_loss == 500
