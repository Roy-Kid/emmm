# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-30
# version: 0.0.1

from core.potential.potential_base import PairBase


class PairLjcut(PairBase):

    def __init__(self, typeName1, typeName2, coeffs) -> None:
        super().__init__(typeName1, typeName2)
        self.style = 'ljcut'
        self.epsilon = coeffs['epsilon']
        self.sigma = coeffs['sigma']
        


    def energy(self, r):
        r6inv = 1/r**6
        e = self.epsilon
        s = self.sigma
        lj3 = 4*e*s**12
        lj4 = 4*e*s**6
        return r6inv*(lj3*r6inv - lj4)

    def force(self, r):
        r2inv = 1/r**2
        r6inv = r2inv**3
        e = self.epsilon
        s = self.sigma
        lj1 = 48*e*s**12
        lj2 = 24*e*s**6
        return r6inv*(lj1*r6inv - lj2)