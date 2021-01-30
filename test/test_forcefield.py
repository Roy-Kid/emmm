# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-27
# version: 0.0.1
from emmm.core.world import World
import pytest

@pytest.fixture(scope='module')
def reader():
    world = World()
    reader = world.active_plugin('INlmpdat')
    yield (world, reader.read_data('test/benezen/lmp'))

class TestSetForceField:
    """ test_lmpdat should be tested before
    """

    def test_set_bond(self, reader):
        world, data = reader
        # lmpdat dont contains the style of bond style
        for bc in data.bondCoeffs:
            world.forcefield.set_bond_coeff('harmonic', *bc)