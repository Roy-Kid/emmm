# author: Roy Kid

from emmm.core.topo import Topo
from emmm.core.forcefield import ForceField
from emmm.plugins import PluginManager
from emmm.core.molecule import Molecule

class World:

    def __init__(self):

        self.xlo = float()
        self.xhi = float()
        self.ylo = float()
        self.yhi = float()
        self.zlo = float()
        self.zhi = float()

        self.forcefield = ForceField(self)

        self.topo  = Topo(self)

        self._molecules = Molecule('world')

        self.pluginManager = PluginManager(self)

    def active_plugin(self, pname):
        """ to instanciate a plugin and return its instance

        Args:
            pname ([str]): [class name of plugin]

        Returns:
            [plugin]: [instance of plugin]
        """

        return self.pluginManager.plugins[pname]()


    def add_items(self, *items):
        self._molecules.add_items(*items)

    @property
    def atoms(self):
        return self.molecule.flatten()

    @property
    def molecules(self):    
        return self._molecules

    @property
    def items(self):
        return self._molecules