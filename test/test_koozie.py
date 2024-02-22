"""koozie unit tests"""

from pytest import approx
from click.testing import CliRunner
from koozie import fr_u, to_u, convert, get_dimensionality
from koozie.cli import koozie_cli


def test_units():
    """Test various unit conversions"""
    assert fr_u(-40.0, "°F") == approx(fr_u(-40.0, "°C"))
    assert convert(-40.0, "°F", "°C") == approx(convert(-40.0, "°C", "°F"))
    assert fr_u(32.0, "°F") == approx(fr_u(0.0, "°C"))
    assert to_u(273.15, "°C") == approx(0.0)
    assert fr_u(1.0, "in") == approx(0.0254)
    assert fr_u(1, "in") == approx(0.0254)
    assert to_u(0.0254, "in") == approx(1.0)
    assert fr_u(3.41241633, "Btu/h") == approx(1.0, 0.0001)


def test_dimensionality():
    """Test dimensionality"""
    assert get_dimensionality("°F") == get_dimensionality("°C")
    assert get_dimensionality("kW") == get_dimensionality("(lb_m*inch*meter)/(minute^2*day)")
    assert get_dimensionality("F") != get_dimensionality("C")


def test_iterable():
    """Test converting iterable"""
    temperatures = fr_u([5, 17, 35, 47, 82, 95], "°F")
    assert isinstance(temperatures, list)
    assert len(temperatures) == 6


runner = CliRunner()


def cli_wrapper(args=None, expect_failure=False):
    """Wrapper function for testing the CLI programmatically"""
    if args is None:
        args = []
    result = runner.invoke(koozie_cli, args)
    assert (result.exit_code != 0) == expect_failure
    return result.output


def test_cli():
    """Test command line interface functionality"""
    cli_wrapper(["--help"])
    cli_wrapper(["-l"])

    output = cli_wrapper(["-40", "degF", "degC"])
    assert round(float(output[:8])) == -40.0
    assert output[-3:-1] == "°C"

    output = cli_wrapper(["1", "in"])
    assert float(output.split(" ")[0]) == 0.0254

    output = cli_wrapper(["1", "in", "day"], True)
    assert "Cannot convert from 'inch' ([length]) to 'day' ([time])" in output

    output = cli_wrapper(["1", "cubit"], True)
    assert "'cubit' is not defined in the unit registry" in output
