# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-30
# version: 0.0.1

from core.potential.potential_base import ImproperBase

class ImproperHarmonic(ImproperBase):

    def __init__(self, typeName1, typeName2, typeName3, typeName4, coeffs) -> None:
        super().__init__(typeName1, typeName2, typeName3, typeName4)

        self.k = coeffs['k']
        self.chi0 = coeffs['chi']

    def energy(self, chi):
        return self.k*(chi - self.chi0)**2

    def force(self, chi):
        return 2*self.k*(chi - self.chi0)