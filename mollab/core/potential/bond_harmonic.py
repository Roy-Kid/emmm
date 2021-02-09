# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from mollab.core.potential.potential_base import BondBase

class BondHarmonic(BondBase):
    def __init__(self, typeName1, typeName2, coeffs) -> None:
        super().__init__(typeName1, typeName2)
        if not isinstance(coeffs, dict):
            raise TypeError(f'coeffs 应为dict类型而不是{type(coeffs)}')
        self._style = 'harmonic'
        self.k = coeffs['k']
        self.r0 = coeffs['r0']
        # self.cutoff = coeffs['cutoff']

    @property
    def style(self):
        return self.style

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, k):
        self._k = float(k)

    @property
    def r0(self):
        return self._r0

    @r0.setter
    def r0(self, r0):
        self._r0 = float(r0)

    def energy(self, r):
        """ get the energy when bond length=r

        Args:
            r (float): bond length

        Returns:
            energy: bond energy
        """
        return self.k*(r - self.r0)**2

    def force(self, r):
        """ get the force when bond length=r

        Args:
            r (float): bond length

        Returns:
            force: bond force
        """
        return 2*self.k*(r - self.r0)
    @property
    def lmp_format(self):
        # k r0
        return [self.k, self.r0]