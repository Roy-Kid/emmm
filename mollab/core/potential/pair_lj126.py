# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-30
# version: 0.0.1

from mollab.core.potential.potential_base import PairBase


class PairLj126(PairBase):
    def __init__(self, typeName1, typeName2, coeffs) -> None:
        super().__init__(typeName1, typeName2)
        self._style = 'lj126'
        self.epsilon = coeffs['epsilon']
        self.sigma = coeffs['sigma']
        if len(coeffs) == 3:
            self.cutoff = coeffs[2]

    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, e):
        self._epsilon = float(e)

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, s):
        self._sigma = float(s)

    def energy(self, r):
        r6inv = 1 / r**6
        e = self.epsilon
        s = self.sigma
        lj3 = 4 * e * s**12
        lj4 = 4 * e * s**6
        return r6inv * (lj3 * r6inv - lj4)

    def force(self, r):
        r2inv = 1 / r**2
        r6inv = r2inv**3
        e = self.epsilon
        s = self.sigma
        lj1 = 48 * e * s**12
        lj2 = 24 * e * s**6
        return r6inv * (lj1 * r6inv - lj2)

    @property
    def lmp_format(self):
        return [self.epsilon, self.sigma]