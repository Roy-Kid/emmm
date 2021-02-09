from mollab.core.create import CreateAtom
from mollab.core.molecule import Molecule
from . import InorganicBase

class SiO2(InorganicBase):
    def __init__(self, world) -> None:
        super().__init__(world)
        self.mol = Molecule("SIO")
