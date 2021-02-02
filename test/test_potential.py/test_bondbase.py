# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1
from emmm.core.potential.potential_base import BondBase
import pytest

@pytest.fixture()
def a_tuple():
    return 'data'

def test_data(a_tuple):
    assert a_tuple=='data'

class TestBondBase:

    @pytest.fixture(scope='class')
    def bondbase(self):
        bb = BondBase()
        yield bb

    def test_grid(self, bondbase):
        bb = bondbase
        bb.r0 = 1.23
        rlist = bb._grid()
        assert len(rlist) == 100