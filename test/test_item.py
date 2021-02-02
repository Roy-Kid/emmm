
from emmm.core.item import Item
import pytest
import numpy as np

class TestItem:

    @pytest.fixture
    def item(self):
        yield Item()

    def test_move(self, item):

        o = np.array([0, 0, 0])

        assert (item._move(o, 1, 1, 1) == np.array([1,1,1])).all()
        assert (item._move(o, 1.1, 1.1, 1.1) == np.array([1.1, 1.1, 1.1])).all()

    def test_rotate(self, item):

        o = np.array([0, 0, 0])

        assert (item._rotate(o, 1, 1, 0, 0) == np.array([0, 0, 0])).all()
        assert (item._rotate(o, 1, 0, 1, 0) == np.array([0, 0, 0])).all()
        assert (item._rotate(o, 1, 0, 0, 1) == np.array([0, 0, 0])).all()
        assert (item._rotate(o, 2, 0, 1, 0) == np.array([0, 0, 0])).all()

        o = np.array([1, 0, 0])

        assert (np.round(item._rotate(o, 1, 1, 0, 0), 4) == np.array([1, 0, 0])).all()
        assert (np.round(item._rotate(o, 1, 0, 1, 0), 4) == np.array([-1,0, 0])).all()
        assert (np.round(item._rotate(o, 1, 0, 0, 1), 4) == np.array([-1,0,0,])).all()

