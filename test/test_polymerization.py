
from mollab.plugins.method.polym import Polymerization

def test_polym():
    p = Polymerization()
    world = p.world
    world.set_bond('harmonic', '1', '4', 410, 1.44, type='nl-cl')
    p.loop()