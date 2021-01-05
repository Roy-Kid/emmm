from emmm.core.world import World
import pytest
import emmm as em

class TestLMPDAT:

    def test_read(self):

        world = World()
        reader = world.active_plugin('INlmpdat')
        h2o = reader.read_data('h2o.lmpdat')

        