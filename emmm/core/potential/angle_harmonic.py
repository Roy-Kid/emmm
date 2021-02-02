# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-30
# version: 0.0.1
from emmm.core.potential.potential_base import AngleBase
class AngleHarmonic(AngleBase):

    def __init__(self, typeName1, typeName2, typeName3, coeffs) -> None:
        super().__init__(typeName1, typeName2, typeName3)
        self._style = 'harmonic'
        self.theta0 = coeffs['theta']
        self.k = coeffs['k']

    @property
    def theta0 (self):
        return self._theta0
    @theta0.setter
    def theta0(self, t):
        self._theta0 = float(t)

    @property
    def k(self):
        return self._k
    @k.setter
    def k(self, k):
        self._k = float(k)

    def energy(self, theta):

        return self.k*(theta - self.theta0)**2

    def force(self, theta):
        return self.k*2 *(theta - self.theta0)

