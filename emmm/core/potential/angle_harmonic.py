# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-30
# version: 0.0.1
from core.potential.potential_base import AngleBase
class AngleHarmonic(AngleBase):

    def __init__(self, typeName1, typeName2, typeName3, coeffs) -> None:
        super().__init__(typeName1, typeName2, typeName3)
        self.style = 'harmonic'
        self.theta0 = coeffs['theta']
        self.k = coeffs['k']

    def energy(self, theta):

        return self.k*(theta - self.theta0)**2

    def force(self, theta):
        return self.k*2 *(theta - self.theta0)

