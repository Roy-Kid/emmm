# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-27
# version: 0.0.1

from mollab.core.dstru import ndarray
import pytest

class TESTndarray:

    @pytest.fixture(scope='class')
    def threed(self):

        return ndarray((16,16,16))

    def test_shape(self, threed):

        assert len(threed) == 16
        assert len(threed[0]) == 16
        assert len(threed[0][0]) == 16