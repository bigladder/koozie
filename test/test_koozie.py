from pytest import approx
from koozie import fr_u, to_u, convert
from koozie.cli import koozie_cli
from click.testing import CliRunner


def test_units():
    assert fr_u(-40.0, "°F") == approx(fr_u(-40.0, "°C"))
    assert convert(-40.0, "°F", "°C") == approx(convert(-40.0, "°C", "°F"))
    assert fr_u(32.0, "°F") == approx(fr_u(0.0, "°C"))
    assert to_u(273.15, "°C") == approx(0.0)
    assert fr_u(1.0, "in") == approx(0.0254)
    assert to_u(0.0254, "in") == approx(1.0)
    assert fr_u(3.41241633, "Btu/h") == approx(1.0, 0.0001)


runner = CliRunner()


def cli_wrapper(args=[], expect_failure=False):
    result = runner.invoke(koozie_cli, args)
    assert (result.exit_code != 0) == expect_failure
    return result.output


def test_cli():
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
