from gethurricaneloss.__main__ import gethurricaneloss


def test_main_verbose_muli() -> None:
    result = gethurricaneloss(10, True, True,
                              10000, 1, 0,
                              10000, 1, 0)

    assert result.num_years == 10
    assert result.total_loss > 530000
    assert result.total_loss < 560000


def test_main_info_single() -> None:
    result = gethurricaneloss(10, False, False,
                              10000, 1, 0,
                              10000, 1, 0)

    assert result.num_years == 10
    assert result.total_loss > 530000
    assert result.total_loss < 560000
