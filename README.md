# calc-hurricane-loss
Uses a Monte-Carlo simulation to calculate hurricane loss

## Description

```{text}
Total loss = 0
For each simulation year
    Simulation loss = 0
    Sample number of Florida events.
    For each Florida event
        Sample a Florida loss and add it to the simulation loss.
    Sample number of Gulf events.
    For each Gulf event
        Sample a Gulf loss and add it to the simulation loss
    Add the simulation loss to the total loss

Mean loss = total loss / number of simulation years
```

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

- `-n`, `--num_monte_carlo_samples` - Number of samples (i.e. simulation years) to run, (defaults to ???)

## Development Usage

All the necessary commands needed for development, build and test are encapsulated in the `Makefile`.
To perform a complete reinstall and test, from within the root folder of the project just type:

```{bash}
make
```

## Design Thinking

- First commit was to get a skeleton for the application to be developed in.

  - This included the use of `pytest` and `pytest-cov` for testinsg as well as a noddy test.
  - Configure use of `tox` and `setup.py` - this was by-and-large copied from (httpie)[https://github.com/jakubroztocil/httpie] as a good solid python command line application to learn from.
  - The addition of a `Makefile`, I tend to use make files for all my projects and again, saw that `httpie` followed this best-practice too.

## Todo

- config
- multiprocessor
- command line args