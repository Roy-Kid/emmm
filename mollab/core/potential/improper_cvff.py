# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-31
# version: 0.0.1

from mollab.core.potential.potential_base import ImproperBase
import math

class ImproperCvff(ImproperBase):

    def __init__(self, typeName1, typeName2, typeName3, typeName4, coeffs) -> None:
        super().__init__(typeName1, typeName2, typeName3, typeName4)
        self._style = 'cvff'
        self.k = coeffs['k']
        self.d = coeffs['d']
        self.n = coeffs['n']

    @property
    def k(self):
        return self._k
    @k.setter
    def k(self, k):
        self._k = float(k)

    @property
    def n(self):
        return self._n
    @n.setter
    def n(self, n):
        self._n = float(n)

    @property
    def d(self):
        return self._d
    @d.setter
    def d(self, d):
        d = int(d)
        if d == 1 or d == -1:
            self._d = d
        else:
            raise ValueError('d param in cvff should be 1 or -1')

    def energy(self, phi):
        return self.k*(1+self.d*math.cos(phi*self.n))

    def force(self, phi):
        return -1*self.n*self.k*math.sin(self.n*phi)

    @property
    def lmp_format(self):
        return [self.k, self.d, self.n]