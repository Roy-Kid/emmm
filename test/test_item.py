<<<<<<< HEAD
from mollab.item import Item
from mollab.atom import Atom
from mollab.particle import Particle
from mollab.segment import Segment

p0 = Particle()
p0.label = 'p0'
s0 = Segment()
s0.label = 's0'
s0.append(p0)
s1 = Segment()
s1.label = 's1'
s1.append(s0)

print((s1.toJson()))
s1Json = s1.toJson()

s2 = Segment()
s2.fromJson(s1Json)

def test_consistency():
    assert s2.toJson() == s1.toJson()



a1 = Atom()
a1.label = 'a1'
a1.type = 'C'
a1.q = 0

a2 = Atom()
a2.label = 'a2'
a2.type = 'C'
a2.q = 0

a3 = Atom()
a3.label = 'a3'
a3.type = 'C'
a3.q = 0

a1.link(a2)
a2.link(a3)
a3.link(a1)

def test_atom():

    ajson = a1.toJson()
    assert ajson['type'] == 'C'
    assert ajson['q'] == 0

def test_ring_molecule():


    assert len(a1.links) == 2
    assert len(a2.links) == 2
    assert len(a3.links) == 2

    assert len(a1.getBonds()) == 2
    assert len(a1.getAngles()) == 1

    seg = Segment()
    seg.label = 'Ternary'
    seg.append(a1, a2, a3)
    print(seg.toJson())

    seg.updateTopo()
    assert len(seg.getBonds()) == 3

def test_duplicate():
    a11 = a1.duplicate()
    assert a11.label == a1.label
    assert a11.type == a1.type
    assert a11.id != a1.id
=======

from mollab.core.item import Item
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

>>>>>>> 048eb4a4c3aaf58d0cc2d4b7b096e90f3d9fc807
