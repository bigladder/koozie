[![Test](https://github.com/bigladder/koozie/actions/workflows/test.yaml/badge.svg)](https://github.com/bigladder/koozie/actions/workflows/test.yaml)

koozie
======

*koozie* is a light-weight wrapper around [*pint*](https://pint.readthedocs.io/en/stable/). The intent is to provide much of the functionality without worrying about the setup. It uses quantities internally, but its functions only return floats. This approach reflects the opinion that all calculations should be performed in Standard base SI units, and any conversions can happen via pre- or post-processing for usability. This minimizes additional operations in performance critical code.

*koozie* also defines a few convenient aliases for different units. See the [source code](https://github.com/bigladder/koozie/blob/master/koozie/koozie.py) for details. A list of other available units is defined in [pint's default units definition file](https://github.com/hgrecco/pint/blob/master/pint/default_en.txt).

There are three public functions in *koozie*:

- `fr_u(value, from_units)`: Convert a value from given units to base SI units
- `to_u(value, to_units)`: Convert a value from base SI units to given units
- `convert(value, from_units, to_units)`: Convert from any units to another units of the same dimension

Example usage can be found in the [test file](https://github.com/bigladder/koozie/blob/master/test/test_koozie.py).
