# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-03-07
# version: 0.0.1

from mollab.core.item import Item
from mollab.core.atom import Atom
import numpy as np


class Improper(Item):
    def __init__(self,
                 atom1: Atom,
                 atom2: Atom,
                 atom3: Atom,
                 atom4: Atom,
                 ip=None) -> None:
        super().__init__('Dihedral')
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.atom4 = atom4

        self._ip = ip

    def __str__(self) -> str:
        return f'< Improper: {self.atom1}-{self.atom2}-{self.atom3}-{self.atom4} >'

    @property
    def ip(self):
        return self._ip

    @property
    def type(self):
        self._type = self.ip.type
        return self._type

    @property
    def typeId(self):
        self._typeId = self.ip.typeId
        return self._typeId

    def __contains__(self, atom):
        if atom in [self.atom1, self.atom2, self.atom3, self.atom4]:
            return True
        else:
            return False