# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-03-07
# version: 0.0.1

from mollab.core.item import Item
import numpy as np

class Pair(Item):

    def __init__(self, atom1, atom2, pp=None):
        super().__init__('Pair')
        self.atom1 = atom1
        self.atom2 = atom2
        self._pp = pp

    @property
    def pp(self):
        return self._pp

    @property
    def type(self):
        self._type = self.pp.type
        return self._type

    @property
    def typeId(self):
        self._typeId = self.pp.typeId
        return self._typeId

    