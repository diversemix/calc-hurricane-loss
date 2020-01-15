from .calculator import gethurricaneloss
from .hurricane_region import HurricaneRegion
import numpy


def main():
    """
    The main function for the 'gethurricaneloss' application.

    Responsibility - to unpack any command line arguments and pass them on to the calculator.
    """
    regions = [
        HurricaneRegion('florida', 10, 1.5, 0.6),
        HurricaneRegion('gulf', 10, 1.5, 0.6),
    ]

    numpy.random.poisson(5)
    print("result=", gethurricaneloss(1, regions))


if __name__ == '__main__':
    main()
