[![Release](https://img.shields.io/pypi/v/koozie.svg)](https://pypi.python.org/pypi/koozie)

[![Test](https://github.com/bigladder/koozie/actions/workflows/test.yaml/badge.svg)](https://github.com/bigladder/koozie/actions/workflows/test.yaml)

koozie
======

*koozie* is a light-weight wrapper around [*pint*](https://pint.readthedocs.io/en/stable/) for unit conversions. The intent is to provide much of the functionality without worrying about the setup. It uses quantities internally, but its functions only return floats. This approach reflects the opinion that all calculations should be performed in Standard base SI units, and any conversions can happen via pre- or post-processing for usability. This minimizes additional operations in performance critical code.

*koozie* also defines a few convenient aliases for different units. See the [source code](https://github.com/bigladder/koozie/blob/master/koozie/koozie.py) for details. A list of other available units is defined in [pint's default units definition file](https://github.com/hgrecco/pint/blob/master/pint/default_en.txt).

There are three public functions in *koozie*:

- `fr_u(value, from_units)`: Convert a value from given units to base SI units
- `to_u(value, to_units)`: Convert a value from base SI units to given units
- `convert(value, from_units, to_units)`: Convert from any units to another units of the same dimension

Example usage can be found in the [test file](https://github.com/bigladder/koozie/blob/master/test/test_koozie.py).

*koozie* also provides a command line utility for unit conversions:

```
Usage: koozie [OPTIONS] VALUE FROM_UNITS [TO_UNITS]

  koozie: Convert VALUE from FROM_UNITS to TO_UNITS.

  If TO_UNITS is not specified, VALUE will be converted from FROM_UNITS into
  base SI units.

Options:
  -v, --version    Show the version and exit.
  -l, --list TEXT  Print a list of available units by dimension (e.g.,
                   "power"). Default: list all units.
  -h, --help       Show this message and exit.
```

Example usage:

```
$ koozie 1 inch meter
> 0.0254 m

$ koozie 0 degC degF
> 31.999999999999936 °F

$ koozie 0 degC
> 273.15 K

$ koozie -l flow
> [length] ** 3 / [time] ([volumetric_flow_rate])
  -----------------------------------------------
    - cubic_feet_per_minute (cfm)
    - gallons_per_minute (gpm)

```
