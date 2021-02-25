from mollab.core.atom import Atom, fullAtom
import pytest
import numpy as np

@pytest.fixture(scope='module')
def full():
    atom = fullAtom('1', '1', 'full', '0.123', '0', '0', '0')
    return atom

class TestAtom:
    def test_atom_move(self, a000):

        a000.position = (0, 0, 0)
        a000.move(1, 1, 1)
        assert (a000.position == np.array([1, 1, 1])).all()

    def test_move_to(self, a000):

        a000.move_to(1, 1, 1)
        assert (a000.position == np.array([1, 1, 1])).all()

    def test_atom_rotate(self, a000):

        a000.position = (0, 0, 0)
        a000.rotate(1, 1, 0, 0)
        assert (a000.position == np.array([0, 0, 0])).all()
        a000.rotate(1.0, 1.0, 0.0, 0.0)
        assert (a000.position == np.array([0, 0, 0])).all()

    def test_save_dict(self, a000, full):
        print(a000.save_dict())
        print(full.save_dict())