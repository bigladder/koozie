from pytest import approx
from koozie import fr_u, to_u, convert
from koozie.cli import koozie_cli
from click.testing import CliRunner

def test_units():
  assert fr_u(-40.0,"°F") == approx(fr_u(-40.0,"°C"))
  assert convert(-40.0,"°F","°C") == approx(convert(-40.0,"°C","°F"))
  assert fr_u(32.0,"°F") == approx(fr_u(0.0,"°C"))
  assert to_u(273.15,"°C") == approx(0.0)
  assert fr_u(1.0,"in") == approx(0.0254)
  assert to_u(0.0254,"in") == approx(1.0)
  assert fr_u(3.41241633,"Btu/h") == approx(1.0,0.0001)

def test_cli():
  runner = CliRunner()
  result = runner.invoke(koozie_cli, ["--help"])
  assert result.exit_code == 0
  result = runner.invoke(koozie_cli, ["-l"])
  assert result.exit_code == 0
  result = runner.invoke(koozie_cli, ["-40", "degF", "degC"])
  assert result.exit_code == 0
  output = result.output
  assert round(float(output[:8])) == -40.
  assert output[-3:-1] == "°C"
  result = runner.invoke(koozie_cli, ["1", "in"])
  assert result.exit_code == 0
  assert float(result.output.split(' ')[0]) == 0.0254
  result = runner.invoke(koozie_cli, ["1", "in", "day"])
  assert result.exit_code != 0
  assert "Cannot convert from 'inch' ([length]) to 'day' ([time])" in result.output
  result = runner.invoke(koozie_cli, ["1", "cubit"])
  assert result.exit_code != 0
  assert "'cubit' is not defined in the unit registry" in result.output
