# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-14
# version: 0.0.1

from mollab.core.item import Item
import numpy as np

class Angle(Item):

    def __init__(self, atom1, atom2, atom3, ap=None) -> None:
        super().__init__('Angle')
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self._calc_angle()

        self._ap = ap

    @property
    def ap(self):
        return self._ap

    def _calc_angle(self):
        vec1 = self.atom1.position - self.atom2.position
        vec2 = self.atom3.position - self.atom2.position
        cosa = np.dot(vec1, vec2)/ (np.linalg.norm(vec1)*np.linalg.norm(vec2))
        self._angle = np.arccos(cosa)

    @property
    def angle(self):
        return np.rad2deg(self._angle)
