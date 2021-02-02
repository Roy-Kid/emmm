# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-27
# version: 0.0.1

from emmm.core.world import World

class TestForcefieldViaH2o:

    def test_bondCount(self, h2oWorld):
        assert h2oWorld.bondCount == 2
        
    def test_angleCount(self, h2oWorld):
        assert h2oWorld.angleCount == 1

    def test_dihedralCount(self, h2oWorld):
        assert h2oWorld.dihedralCount == 0

    def test_improperCount(self, h2oWorld):
        assert h2oWorld.improperCount == 0

class TestForceFieldViaCH4:

    def test_bondCount(self, ch4World):
        assert ch4World.bondCount == 4

    def test_angleCount(self, ch4World):
        assert ch4World.angleCount == 6

    def test_dihedralCount(self, ch4World):
        assert ch4World.dihedralCount == 0

    def test_improperCount(self, ch4World):
        assert ch4World.improperCount == 4
