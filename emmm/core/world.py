# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-31
# version: 0.0.1

from emmm.core.topo import Topo
from emmm.core.forcefield import ForceField
from emmm.plugins import PluginManager
from emmm.core.molecule import Molecule

class World:

    worldCount = 0
    worldCount += 1

    def __init__(self):

        self.comment = 'world'+str(World.worldCount)

        self.forcefield = ForceField(self)

        self.topo  = Topo(self)

        # container?
        self._molecules = Molecule('world')

        self.pluginManager = PluginManager(self)

        self.get_bond = self.forcefield.get_bond

        self.get_improper = self.forcefield.get_improper

    def active_plugin(self, pname):
        """ to instanciate a plugin and return its instance

        Args:
            pname ([str]): [class name of plugin]

        Returns:
            [plugin]: [instance of plugin]
        """

        return self.pluginManager.plugins[pname]()


    def add_items(self, items):

        self._molecules.add_items(*items)

    def update(self):
        self._atom = self.molecules.flatten()
        self.topo.search_topo(self.molecules)

    @property
    def atoms(self):
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

    def countAtomType(self):
        atc = 0
        atclist = list()
        for atom in self.atoms:
            if atom.type not in atclist:
                atc += 1
        self._atomTypeCount = atc

    @property
    def atomTypeCount(self):
        return self._atomTypeCount

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
        if xlo < self._xlo:
            self._xlo = xlo

    @property
    def xhi(self):
        return self._xhi
    @xhi.setter
    def xhi(self, xhi):
        if xhi > self._xhi:
            self._xhi = xhi

    @property
    def ylo(self):
        return self._ylo
    @ylo.setter
    def ylo(self, ylo):
        if ylo < self._ylo:
            self._ylo = ylo

    @property
    def yhi(self):
        return self._xhi
    @yhi.setter
    def yhi(self, yhi):
        if yhi > self._yhi:
            self._yhi = yhi

    @property
    def zlo(self):
        return self._zlo
    @zlo.setter
    def zlo(self, zlo):
        if zlo < self._zlo:
            self._zlo = zlo

    @property
    def zhi(self):
        return self._zhi
    @zhi.setter
    def zhi(self, zhi):
        if zhi > self._zhi:
            self._zhi = zhi

    def set_bond(self, style, typeName1, typeName2, **coeff):
        self.forcefield.set_bond(style, typeName1, typeName2, coeff)

    def set_angle(self, style, typeName1, typeName2, typeName3, **coeffs):
        self.forcefield.set_angle(style, typeName1, typeName2, typeName3, coeffs)

    def set_dihedral(self, style, typeName1, typeName2, typeName3, typeName4, **coeff):
        self.forcefield.set_dihedral(style, typeName1, typeName2, typeName3, typeName4, coeff)

    def set_improper(self, style, typeName1, typeName2, typeName3, typeName4, **coeff):
        self.forcefield.set_improper(style, typeName1, typeName2, typeName3, typeName4, coeff)     

    def set_pair(self, style, typeName1, typeName2, **coeffs):
        self.forcefield.set_pair(style, typeName1, typeName2, coeffs)

    