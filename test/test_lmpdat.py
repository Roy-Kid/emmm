from emmm.core.world import World
import pytest
import emmm as em

class TestLMPDAT:

    @pytest.fixture(scope='class')
    def test_read(self):

        world = World()
        reader = world.active_plugin('INlmpdat')
        h2olmpdat = reader.read_data('h2o.lmpdat')

        h2o1 = h2olmpdat[0]

        h2o2 = h2olmpdat['2']

        h2o3 = h2olmpdat[-1]

        world.add_items(h2o1, h2o2, h2o3)
        print('init lmpdat')
 

        return world


    def test_topo(self, test_read):
        
        world = test_read 

        world.forcefield.set_bond_coeffs('harmonic', 1, 2, '2.7')

        world.topo.search_topo(world[0], isAngle=False, isDihedral=False, isForceField=True)

        assert len(world.topoBond)