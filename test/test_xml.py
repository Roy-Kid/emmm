# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-13
# version: 0.0.1

import pytest
import mollab as ml

@pytest.fixture(scope='module')
def xmlWorld():
    reader = ml.plugins.INxml()

    return reader.read('test/benezen/xml')

class TestINxml:

    def test_AtomType(self, xmlWorld):
        assert len(xmlWorld.AtomTypes) == 12