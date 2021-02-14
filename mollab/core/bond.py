# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-14
# version: 0.0.1

from mollab.core.item import Item
from mollab.core.atom import Atom
import numpy as np


class Bond(Item):
    def __init__(self, atom1: Atom, atom2: Atom) -> None:
        super().__init__('Bond')
        self.atom1 = atom1
        self.atom2 = atom2
        self._calc_length()
        self._calc_orient()
        self._calc_position()
        self.__dict__ = {
            'x1': self.atom1.x,
            'x2': self.atom2.x,
        }

    def _calc_length(self):
        self._bond_vec = self.atom1.position - self.atom2.position
        self._length = np.linalg.norm(self._bond_vec)

    def _calc_orient(self):
        self._orient_vec = self._bond_vec / self._length

    def _calc_position(self):
        self.position = (self.atom1.position + self.atom2.position) / 2

    @property
    def length(self):
        return self._length

    @property
    def orient_vec(self):
        return self._orient_vec

