"""koozie functions"""
import importlib.resources as pkg_resources
from collections import OrderedDict
from collections.abc import Iterable
from typing import List

import pint

# Edit constants template to stop using h to represent planck_constant
# See https://github.com/hgrecco/pint/issues/719#issuecomment-998872301
# ---------------------------------------------------------------------
constants_template = (
    pkg_resources.read_text(pint, "constants_en.txt")
    .replace("= h  ", "     ")
    .replace(" h ", " planck_constant ")
)

# Edit units template to use h to represent hour instead of planck_constant
units_template = (
    pkg_resources.read_text(pint, "default_en.txt")
    .replace("@import constants_en.txt", "")
    .replace(" h ", " planck_constant ")
    .replace("hour = 60 * minute = hr", "hour = 60 * minute = h = hr")
)

# Join templates as iterable object
full_template = constants_template.split("\n") + units_template.split("\n")

# Set up UnitRegistry with abbreviated scientific format
unit_registry = pint.UnitRegistry(full_template)
unit_registry.default_format = "~P"  # short pretty
# ---------------------------------------------------------------------

# Add new aliases
unit_registry.define("@alias inch_H2O_39F = in_H2O")
unit_registry.define("@alias ton_of_refrigeration = ton_ref")

# Add new derived dimensions
unit_registry.define("[thermal_resistance] = [area] * [temperature] / [power]")
unit_registry.define("[thermal_conductance] = [power] / ([area] * [temperature])")
unit_registry.define("[volumetric_flow_rate] = [length] ** 3 / [time]")

# Add new units
unit_registry.define("cubic_feet_per_minute = cu_ft / min = cfm")
unit_registry.define("gallons_per_minute = gallon / min = gpm")
unit_registry.define("thermal_resistance_SI = m**2*K/W = R_value_SI = R_SI")
unit_registry.define("thermal_resistance_IP = ft**2*degR*h/Btu = R_value_IP = R_IP")
unit_registry.define("thermal_conductance_SI = W/(m**2*K) = U_factor_SI = U_SI")
unit_registry.define("thermal_conductance_IP = Btu/(ft**2*degR*h) = U_factor_IP = U_IP")


# Private functions (used in CLI)
def fr_q(value: float, from_units: str):
    """Convert a value from given units to a quantity in base SI units"""
    return unit_registry.Quantity(value, from_units).to_base_units()


def to_q(value: float, to_units: str):
    """Convert a value from base SI units to a quantity in any other units"""
    base_units = unit_registry.Quantity(value, to_units).to_base_units().units
    return unit_registry.Quantity(value, base_units).to(to_units)


def convert_q(value: float, from_units: str, to_units: str):
    """Convert a value from any units to a quantity in another units of the same dimension"""
    return unit_registry.Quantity(value, from_units).to(to_units)


# Public functions
def fr_u(value: float, from_units: str):
    """Convert a value from given units to base SI units"""
    return fr_q(value, from_units).magnitude


def to_u(value: float, to_units: str):
    """Convert a value from base SI units to any other units"""
    return to_q(value, to_units).magnitude


def convert(value: float, from_units: str, to_units: str):
    """Convert a value from any units to another units of the same dimension"""
    return convert_q(value, from_units, to_units).magnitude

def get_unit_list():
    """Get list of valid units."""
    unit_list = {}
    for u in unit_registry:
        if u in unit_registry:  # Certain symbols do not show up
            if unit_registry[u].dimensionless:
                dimensionality = "[]"
            else:
                dimensionality = f"{unit_registry[u].dimensionality}"
            if dimensionality not in unit_list:
                unit_list[dimensionality] = {"aliases": [], "units": {}}
            unit = list(unit_registry[u]._units._d.keys())[0]  # pylint: disable=protected-access
            if unit not in unit_list[dimensionality]["units"]:
                unit_list[dimensionality]["units"][unit] = []
            if u != unit:
                unit_list[dimensionality]["units"][unit].append(u)

    # Get dimension aliases
    for dim in unit_registry._dimensions:  # pylint: disable=protected-access
        if dim in unit_list:
            continue

        reference = unit_registry._dimensions[dim].reference  # pylint: disable=protected-access
        dimensionality = f"{unit_registry.get_dimensionality(reference)}"
        if dimensionality not in unit_list:
            unit_list[dimensionality] = {"aliases": [], "units": {}}
        unit_list[dimensionality]["aliases"].append(dim)
    return OrderedDict(sorted(unit_list.items(), key=lambda x: len(x[0])))
