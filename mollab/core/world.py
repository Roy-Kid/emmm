# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-31
# version: 0.0.1

from mollab.core.mapper import Mapper
from mollab.core.topo import Topo
from mollab.core.forcefield import ForceField
from mollab.plugins import PluginManager
from mollab.core.molecule import Molecule


class World:

    worldCount = 0
    worldCount += 1

    def __init__(self):

        self.comment = 'world' + str(World.worldCount)

        self.mapper = Mapper(self)

        self.forcefield = ForceField(self)

        self.topo = Topo(self)

        # container?
        self._molecules = Molecule('world')

        self.pluginManager = PluginManager(self)

        self.get_bond = self.forcefield.get_bond

        self.get_improper = self.forcefield.get_improper

        # track atom type

    def active_plugin(self, pname):
        """ to instanciate a plugin and return its instance

        Args:
            pname ([str]): [class name of plugin]

        Returns:
            [plugin]: [instance of plugin]
        """

        return self.pluginManager.plugins[pname]()

    def add_items(self, items):
        self.mapper.set_types(items)


        self._molecules.add_items(*items)

    def update(self):
        self._atom = self.molecules.flatten()
        self.topo.search_topo(self.molecules)

    @property
    def atoms(self):
        if not getattr(self, '_atom', 0):
            self._atom = self.molecules.flatten()
        return self._atom

    @property
    def molecules(self):
        return self._molecules

    @property
    def items(self):
        return self._molecules

    @property
    def atomCount(self):
        return len(self.atoms)

    @property
    def bondCount(self):
        return len(self.topo.bonds)

    @property
    def angleCount(self):
        return len(self.topo.angles)

    @property
    def dihedralCount(self):
        return len(self.topo.dihedrals)

    @property
    def improperCount(self):
        return len(self.topo.impropers)

    @property
    def atomTypeCount(self):

        return len(self.mapper.typeID)

    @property
    def bondTypeCount(self):
        return len(self.forcefield.bondPotentialList)

    @property
    def angleTypeCount(self):
        return len(self.forcefield.anglePotentialList)

    @property
    def dihedralTypeCount(self):
        return len(self.forcefield.dihedralPotentialList)

    @property
    def improperTypeCount(self):
        return len(self.forcefield.improperPotentialList)

    @property
    def xlo(self):
        return self._xlo

    @xlo.setter
    def xlo(self, xlo):
        if not getattr(self, 'xlo', None) or xlo < self.xlo:
            self._xlo = xlo

    @property
    def xhi(self):
        return self._xhi

    @xhi.setter
    def xhi(self, xhi):
        if not getattr(self, 'xhi', 0) or xhi > self.xhi:
            self._xhi = xhi

    @property
    def ylo(self):
        return self._ylo

    @ylo.setter
    def ylo(self, ylo):

        if not getattr(self, 'ylo', None) or ylo < self.ylo:
            self._ylo = ylo

    @property
    def yhi(self):
        return self._yhi

    @yhi.setter
    def yhi(self, yhi):
        if not getattr(self, 'yhi', 0) or yhi > self.xhi:
            self._yhi = yhi

    @property
    def zlo(self):
        return self._zlo

    @zlo.setter
    def zlo(self, zlo):
        if not getattr(self, 'zlo', None) or zlo < self.zlo:
            self._zlo = zlo

    @property
    def zhi(self):
        return self._zhi

    @zhi.setter
    def zhi(self, zhi):
        if not getattr(self, 'zhi', 0) or zhi > self.xhi:
            self._zhi = zhi

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

    def set_pair(self, style, typeName1, typeName2, **coeffs):

        pp = self.forcefield.set_pair(style, typeName1, typeName2, coeffs)

        self.mapper.set_pair(typeName1, typeName2, pp)

    def set_mass(self, typeName, mass):
        self.forcefield.set_mass(typeName, mass)

    def get_mass(self, typeName):
        return self.forcefield.get_mass(typeName)

    @property
    def masses(self):
        return self.forcefield.massList

    @property
    def pairPotentials(self):
        return self.forcefield.pairPotentialList

    @property
    def bondPotentials(self):
        return self.forcefield.bondPotentialList

    @property
    def anglePotentials(self):
        return self.forcefield.anglePotentialList

    @property
    def dihedralPotentials(self):
        return self.forcefield.dihedralPotentialList

    @property
    def improperPotentials(self):
        return self.forcefield.improperPotentialList

    
