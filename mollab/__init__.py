# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-13
# version: 0.0.1
from .plugins import PluginManager
from .core import Atom, World


pluginManager = PluginManager()

def active_plugin(pname):
    """ to instanciate a plugin and return its instance

    Args:
        pname ([str]): [class name of plugin]

    Returns:
        [plugin]: [instance of plugin]
    """

    return pluginManager.plugins[pname]()