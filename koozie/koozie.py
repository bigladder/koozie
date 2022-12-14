import importlib.resources as pkg_resources
import pint

# Edit constants template to stop using h to represent planck_constant
# See https://github.com/hgrecco/pint/issues/719#issuecomment-998872301
# ---------------------------------------------------------------------
constants_template = pkg_resources.read_text(pint, 'constants_en.txt').replace("= h  ", "     ").replace(" h ", " planck_constant ")

# Edit units template to use h to represent hour instead of planck_constant
units_template = pkg_resources.read_text(pint, 'default_en.txt').replace("@import constants_en.txt", "").replace(" h ", " planck_constant ").replace("hour = 60 * minute = hr", "hour = 60 * minute = h = hr")

# Join templates as iterable object
full_template = constants_template.split("\n") + units_template.split("\n")

# Set up UnitRegistry with abbreviated scientific format
ureg = pint.UnitRegistry(full_template)
ureg.default_format = "~P"  # short pretty
# ---------------------------------------------------------------------

# Add new definitions / aliases
ureg.define('cubic_feet_per_minute = cu_ft / min = cfm')
ureg.define('in_H2O = inch_H2O_39F')
ureg.define('ton_ref = ton_of_refrigeration')

# Public functions
def fr_u(value, from_units):
  '''Convert a value from given units to base SI units'''
  return ureg.Quantity(value, from_units).to_base_units().magnitude

def to_u(value, to_units):
  '''Convert from base SI units to any other units'''
  base_units = ureg.Quantity(value, to_units).to_base_units().units
  return ureg.Quantity(value, base_units).to(to_units).magnitude

def convert(value, from_units, to_units):
  '''Convert from any units to another units of the same dimension'''
  return ureg.Quantity(value, from_units).to(to_units).magnitude

