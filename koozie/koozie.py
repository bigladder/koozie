import importlib.resources as pkg_resources
import pint
from collections import OrderedDict

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

# Add new aliases
ureg.define('@alias inch_H2O_39F = in_H2O')
ureg.define('@alias ton_of_refrigeration = ton_ref')

# Add new derived dimensions
ureg.define('[thermal_resistance] = [area] * [temperature] / [power]')
ureg.define('[thermal_conductance] = [power] / ([area] * [temperature])')
ureg.define('[volumetric_flow_rate] = [length] ** 3 / [time]')

# Add new units
ureg.define('cubic_feet_per_minute = cu_ft / min = cfm')
ureg.define('gallons_per_minute = gallon / min = gpm')
ureg.define('thermal_resistance_SI = m**2*K/W = R_value_SI = R_SI')
ureg.define('thermal_resistance_IP = ft**2*degR*h/Btu = R_value_IP = R_IP')
ureg.define('thermal_conductance_SI = W/(m**2*K) = U_factor_SI = U_SI')
ureg.define('thermal_conductance_IP = Btu/(ft**2*degR*h) = U_factor_IP = U_IP')

# Private functions (used in CLI)
def fr_q(value, from_units):
  '''Convert a value from given units to a quantity in base SI units'''
  return ureg.Quantity(value, from_units).to_base_units()

def to_q(value, to_units):
  '''Convert a value from base SI units to a quantity in any other units'''
  base_units = ureg.Quantity(value, to_units).to_base_units().units
  return ureg.Quantity(value, base_units).to(to_units)

def convert_q(value, from_units, to_units):
  '''Convert a value from any units to a quantity in another units of the same dimension'''
  return ureg.Quantity(value, from_units).to(to_units)

# Public functions
def fr_u(value, from_units):
  '''Convert a value from given units to base SI units'''
  return fr_q(value, from_units).magnitude

def to_u(value, to_units):
  '''Convert a value from base SI units to any other units'''
  return to_q(value, to_units).magnitude

def convert(value, from_units, to_units):
  '''Convert a value from any units to another units of the same dimension'''
  return convert_q(value, from_units, to_units).magnitude

def sorting_function(x):
  return len(x[0])


def get_unit_list():
  unit_list = {}
  for u in ureg:
    if u in ureg: # Certain symbols do not show up
      if ureg[u].dimensionless:
        dimensionality = "[]"
      else:
        dimensionality = f"{ureg[u].dimensionality}"#.replace('[','').replace(']','').replace(' ** ','^')
      if dimensionality not in unit_list:
        unit_list[dimensionality] = {
          "aliases": [],
          "units": {}
        }
      unit = list(ureg[u]._units._d.keys())[0]
      if unit not in unit_list[dimensionality]["units"]:
        unit_list[dimensionality]["units"][unit] = []
      if u != unit:
        unit_list[dimensionality]["units"][unit].append(u)

  # Get dimension aliases
  for dim in ureg._dimensions:
    if dim in unit_list:
      continue
    else:
      dimensionality = f"{ureg.get_dimensionality(ureg._dimensions[dim].reference)}"
      #if dimensionality == "None":
      #  dimensionality = "[]"
      if dimensionality not in unit_list:
        unit_list[dimensionality] = {
          "aliases": [],
          "units": {}
        }
      unit_list[dimensionality]["aliases"].append(dim)
  return OrderedDict(sorted(unit_list.items(), key=sorting_function))

