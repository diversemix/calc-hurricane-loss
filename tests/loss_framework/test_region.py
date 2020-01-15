from loss_framework import EventRegion


def test_constructs() -> None:
    hr = EventRegion('uk', 1, 2, 3)
    expected = " <Region: {}, Rate: {}, Mean {}, StdDev {}> ".format('uk', 1, 2, 3)

    assert str(hr) == expected, str(hr)
