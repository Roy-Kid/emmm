
import pytest
from mollab.core.world import World
from mollab.core.atom import fullAtom

@pytest.fixture()
def initWorld():
    world = World()
    world.xlo = 0
    world.xhi = 10
    a1 = fullAtom(1, 1, 1, 0, -1, 0, 0)
    a2 = fullAtom(2, 1, 1, 0, 0, 0, 0)
    a3 = fullAtom(3, 1, 1, 0, 1, 0, 0)
    a4 = fullAtom(4, 1, 1, 0, 3, 0, 0)
    a5 = fullAtom(5, 1, 1, 0, 11, 0, 0)
    a1.cutoff = 3
    a2.cutoff = 3
    a3.cutoff = 3
    a4.cutoff = 3
    a5.cutoff = 3
    world.add_items(a1, a2, a3, a4, a5)
    for atom in world.atoms:
        world.neighborlist.build(atom)

class TestNeighbor:

    def test_neighbor(self, initWorld):
        for atom in initWorld.atoms:
            print(atom.neighbor)