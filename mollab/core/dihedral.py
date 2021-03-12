# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-03-07
# version: 0.0.1

from mollab.core.item import Item
from mollab.core.atom import Atom
import numpy as np


class Dihedral(Item):
    def __init__(self, atom1: Atom, atom2: Atom, atom3: Atom, atom4: Atom, dp=None) -> None:
        super().__init__('Dihedral')
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.atom4 = atom4


        self._dp = dp

    def __str__(self) -> str:
        return f'< Dihedral: {self.atom1}-{self.atom2}-{self.atom3}-{self.atom4} >'

    @property
    def dp(self):
        return self._dp

    @property
    def type(self):
        self._type = self.dp.type
        return self._type

    @property
    def typeId(self):
        self._typeId = self.dp.typeId
        return self._typeId

    def __contains__(self, atom):
        if atom in [self.atom1, self.atom2, self.atom3, self.atom4]:
            return True
        else:
            return False
            