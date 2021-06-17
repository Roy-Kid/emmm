# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1

import pytest
import mollab as ml

@pytest.fixture(scope='module')
def pdbWorld():
    reader = ml.plugins.INpdb()
    world = reader.read('test/benezen/pdb', 'test/benezen/xml')

    world.topo.search_topo()
    return world

class TestINpdb:

    def test_