from emmm.core.atom import Atom
import pytest
import numpy as np

class TestAtom:

    @pytest.fixture
    def atom(self):
        yield Atom()


    def test_atom_move(self, atom):

        atom.position = (0,0,0)
        atom.move(1,1,1)
        assert (atom.position == np.array([1,1,1])).all()

   
    def test_move_to(self, atom):

        atom.move_to(1,1,1)
        assert (atom.position == np.array([1,1,1])).all()


    def test_atom_rotate(self, atom):

        atom.position = (0, 0, 0)
        atom.rotate(1,1,0,0)
        assert (atom.position == np.array([0, 0, 0])).all()
        atom.rotate(1.0,1.0,0.0,0.0)
        assert (atom.position == np.array([0, 0, 0])).all()