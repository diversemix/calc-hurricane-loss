# calc-hurricane-loss
Uses a Monte-Carlo simulation to calculate hurricane loss

## Description

This application calculates the total loss caused by hurricanes, given the two regions:
- Florida
- Gulf States

The problem was broken down into a generic `loss-framework` which can model regions and their respective event models.
Then this was used to build upon for this specific case for hurricanes.
However, it should be relatively easy to extend for more regions or different event models.

## Usage

```{bash}
gethurricaneloss [options] florida_landfall_rate florida_mean florida_stddev gulf_landfall_rate gulf_mean gulf_stddev 
```

Calculates the average annual hurricane loss in $Billions for a simple hurricane model.
The model is parameterized by:

- `florida_landfall_rate` – The annual rate of landfalling hurricanes in Florida.
- `florida_mean`, `florida_stddev` – The LogNormal parameters that describe the economic loss of a landfalling hurricane in Florida.
- `gulf_landfall_rate` - The annual rate of landfalling hurricanes in the Gulf states.
- `gulf_mean`, `gulf_stddev` - The LogNormal parameters that describe the economic loss of a landfalling hurricane in the Gulf stats.

options:
- `--version` - Reports the version then exits.
- `-n`, `--num_monte_carlo_samples` - Number of samples (i.e. simulation years) to run, (defaults to 100)
- `-v/-i`, `--verbose/--info` - This switches logging between verbose or just info output (default)
- `-m/-s`, `--multicpu/--singlecpu` - This switches the calculation to be done on a single cpu (default) or all available. 

## Development Usage

:warning: **NOTE** - To develop this locally you will need python3.7 as application uses [dataclasses](https://docs.python.org/3/library/dataclasses.html) 

All the necessary commands needed for development, build and test are encapsulated in the `Makefile`.
To perform a complete reinstall and test, from within the root folder of the project just type:

```{bash}
make
```

If this give you problems there is also a docker container that does the complete build and test cycle, this can be run with:

```{bash}
make docker
```

Here are a complete set of make commands that can be used:

```{bash}
make all
make requirements:
make install
make clean:
make venv:
make docker
make lint:
make test
make test-all
make test-dist
make test-tox
make test-sdist
make test-bdist-wheel
make uninstall-gethurricaneloss
```

## Design Thinking

- First commit was to get a skeleton for the application to be developed in.

  - This included the use of `pytest` and `pytest-cov` for testing as well as a noddy test.
  - Configure use of `tox` and `setup.py` - this was by-and-large copied from [httpie](https://github.com/jakubroztocil/httpie) as a good solid python command line application to learn from.
  - The addition of a `Makefile`, I tend to use make files for all my projects and again, saw that `httpie` followed this best-practice too.

- Made use of [typing](https://docs.python.org/3/library/typing.html) and this is statically checked with [mypy](https://mypy.readthedocs.io/en/latest/). This means that lots of the validation is done at compile time (`make lint`)

- Used [click](https://click.palletsprojects.com/en/7.x/) for handling the command line as its a lot slicker than `argparse`

- There is a generic `loss-framework` that specifies the following:

  - `BatchArgument` : This is used as the argument list for each spawned process.
  - `BatchedCalculator` : This calculator is used when utilizing all available CPUs
  - `Calculator` : This calculator is used with using a single core.
  - `EventModel` : Specifies the distrubtion functions for a particular event.
  - `EventRegion` : Specifies a region and the stats associated with that event.
  - `LossResult` : This is the result of any calculation performed.

## Issues

- Test Coverage - This seems to be generating some warnings I cannot remove
- I don't think its an issue but not had chance to check: https://stackoverflow.com/questions/27098529/numpy-float64-vs-python-float
- Sensible standard deviations - though looking around the internet this does not seem straight forward. Perhaps we could warn if the stddev > 2 ?
- There are more tests that I would like to get in place. But I'd like to ask more questions first.
