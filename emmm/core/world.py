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

        self._world = dict()

        self.forcefield = ForceField(self)

        self.topo  = Topo(self)

        self.items = Molecule('world')

        self.pluginManager = PluginManager(self)

    def active_plugin(self, pname):
        """ to instanciate a plugin and return its instance

        Args:
            pname ([str]): [class name of plugin]

        Returns:
            [plugin]: [instance of plugin]
        """

        return self.pluginManager.plugins[pname](self)

    def vis(self):
        out = self.active_plugin('OUTjson')
        json = out.dump_data()
        import eel
        eel.init('/home/roy/Work/emmm/emmm/vis')
        eel.readDataInJs(json)
        eel.start('atom-sim.html', mode='chrome')

    def add_items(self, *items):
        self.items.add_items(*items)

    def __getitem__(self, index):

        if isinstance(index, int):

            return self.items[index]
        elif isinstance(index, str):
            for item in self.items:
                if item.label == index:
                    return item
                
            raise KeyError('没有这个item')
        else:
            raise IndexError('未支持的索引方式')       
