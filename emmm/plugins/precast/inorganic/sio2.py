from emmm.core.create import CreateAtom
from emmm.core.molecule import Molecule
from . import InorganicBase

class SiO2(InorganicBase):
    def __init__(self, world) -> None:
        super().__init__(world)
        self.mol = Molecule("SIO")
