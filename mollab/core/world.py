# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-31
# version: 0.0.1

from mollab.core.mapper import Mapper
from mollab.core.topo import Topo
from mollab.core.forcefield import ForceField
from mollab.core.item import Item


class World(Item):

    worldCount = 0
    worldCount += 1

    def __init__(self):

        self.comment = 'world' + str(World.worldCount)

        self.mapper = Mapper(self)

        self.forcefield = ForceField(self)

        self.topo = Topo(self)

    #     self.get_bond = self.forcefield.get_bond

    #     self.get_improper = self.forcefield.get_improper

    #     # track atom type

    def add_items(self, items):
        for item in items:
            item.parent = self.label
        self.container.extend(items)

    # def update(self):
    #     self._atom = self.molecules.flatten()
    #     self.topo.search_topo(self.molecules)

    # @property
    # def atoms(self):
    #     if not getattr(self, '_atom', 0):
    #         self._atom = self.molecules.flatten()
    #     return self._atom

    # @property
    # def molecules(self):
    #     return self._molecules

    # @property
    # def items(self):
    #     return self._molecules

    @property
    def atomCount(self):
        return self._atomCount

    @atomCount.setter
    def atomCount(self, v):
        self._atomCount = int(v)

    @property
    def bondCount(self):
        return self._bondCount

    @bondCount.setter
    def bondCount(self, v):
        self._bondCount = int(v)

    @property
    def angleCount(self):
        return self._angleCount

    @angleCount.setter
    def angleCount(self, v):
        self._angleCount = int(v)

    @property
    def dihedralCount(self):
        return self._dihedralCount

    @dihedralCount.setter
    def dihedralCount(self, v):
        self._dihedralCount = int(v)

    @property
    def improperCount(self):
        return self._improperCount

    @improperCount.setter
    def improperCount(self, v):
        self._improperCount = int(v)

    @property
    def atomTypeCount(self):
        return self._atomTypeCount

    @atomTypeCount.setter
    def atomTypeCount(self, v):
        self._atomTypeCount = int(v)

    @property
    def bondTypeCount(self):
        return self._bondTypeCount

    @bondTypeCount.setter
    def bondTypeCount(self, v):
        self._bondTypeCount = int(v)

    @property
    def angleTypeCount(self):
        return self._angleTypeCount

    @angleTypeCount.setter
    def angleTypeCount(self, v):
        self._angleTypeCount = int(v)

    @property
    def dihedralTypeCount(self):
        return self._dihedralTypeCount

    @dihedralTypeCount.setter
    def dihedralTypeCount(self, v):
        self._dihedralTypeCount = int(v)

    @property
    def improperTypeCount(self):
        return self._improperTypeCount

    @improperTypeCount.setter
    def improperTypeCount(self, v):
        self._improperTypeCount = int(v)

    @property
    def xlo(self):
        return self._xlo

    @xlo.setter
    def xlo(self, xlo):
        self._xlo = float(xlo)

    @property
    def xhi(self):
        return self._xhi

    @xhi.setter
    def xhi(self, xhi):
        self._xhi = float(xhi)

    @property
    def ylo(self):
        return self._ylo

    @ylo.setter
    def ylo(self, ylo):
        self._ylo = float(ylo)

    @property
    def yhi(self):
        return self._yhi

    @yhi.setter
    def yhi(self, yhi):
        self._yhi = float(yhi)

    @property
    def zlo(self):
        return self._zlo

    @zlo.setter
    def zlo(self, zlo):
        self._zlo = float(zlo)

    @property
    def zhi(self):
        return self._zhi

    @zhi.setter
    def zhi(self, zhi):
        self._zhi = float(zhi)

    def set_pair(self, style, typeName1, typeName2, **coeffs):

        pp = self.forcefield.set_pair(style, typeName1, typeName2, coeffs)

        self.mapper.set_pair(typeName1, typeName2, pp)

    def set_bond(self, style, typeName1, typeName2, **coeff):

        bp = self.forcefield.set_bond(style, typeName1, typeName2, coeff)

        self.mapper.set_bond(typeName1, typeName2, bp)

    def set_angle(self, style, typeName1, typeName2, typeName3, **coeffs):

        ap = self.forcefield.set_angle(style, typeName1, typeName2, typeName3,
                                       coeffs)

        self.mapper.set_angle(typeName1, typeName2, typeName3, ap)

    def set_dihedral(self, style, typeName1, typeName2, typeName3, typeName4,
                     **coeffs):

        dp = self.forcefield.set_dihedral(style, typeName1, typeName2,
                                          typeName3, typeName4, coeffs)

        self.mapper.set_dihedral(typeName1, typeName2, typeName3, typeName4,
                                 dp)

    def set_improper(self, style, typeName1, typeName2, typeName3, typeName4,
                     **coeffs):
        ip = self.forcefield.set_improper(style, typeName1, typeName2,
                                          typeName3, typeName4, coeffs)

        self.mapper.set_improper(typeName1, typeName2, typeName3, typeName4,
                                 ip)

    def set_mass(self, typeName, mass):
        self.forcefield.set_mass(typeName, mass)

    # def get_mass(self, typeName):
    #     return self.forcefield.get_mass(typeName)

    # @property
    # def masses(self):
    #     return self.forcefield.massList

    # @property
    # def pairPotentials(self):
    #     return self.forcefield.pairPotentialList

    # @property
    # def bondPotentials(self):
    #     return self.forcefield.bondPotentialList

    # @property
    # def anglePotentials(self):
    #     return self.forcefield.anglePotentialList

    # @property
    # def dihedralPotentials(self):
    #     return self.forcefield.dihedralPotentialList

    # @property
    # def improperPotentials(self):
    #     return self.forcefield.improperPotentialList
