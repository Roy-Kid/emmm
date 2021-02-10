# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1

from mollab.core.world import World
import pytest


@pytest.fixture(scope='module')
def world():
    return World()

@pytest.fixture(scope='module')
def reader(world):
    reader = world.active_plugin('INpdb')
    reader = reader.read_data('test/benezen/pdb', xml='test/benezen/xml')

    world.add_items(reader.molecules)

    yield reader

class TestINpdb:

    def test_system(self, reader):
        assert len(reader.atomRaw) == 12
        assert len(reader.bondRaw) == 12
        assert len(reader.atoms) == 12
