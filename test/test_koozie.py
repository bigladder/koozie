from pytest import approx
from koozie import fr_u, to_u, convert

def test_units():
  assert fr_u(-40.0,"°F") == approx(fr_u(-40.0,"°C"))
  assert convert(-40.0,"°F","°C") == approx(convert(-40.0,"°C","°F"))
  assert fr_u(32.0,"°F") == approx(fr_u(0.0,"°C"))
  assert to_u(273.15,"°C") == approx(0.0)
  assert fr_u(1.0,"in") == approx(0.0254)
  assert to_u(0.0254,"in") == approx(1.0)
  assert fr_u(3.41241633,"Btu/h") == approx(1.0,0.0001)
