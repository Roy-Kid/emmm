# author: Roy Kids

import pkgutil, os
import inspect
from .input.input_base import InputBase
from .output.output_base import OutputBase
from .precast.precast_base import PrecastBase
from . import input
from . import output
from . import precast

class PluginManager:

    """
    该类会通过传入的package查找继承了Plugin类的插件类
    """

    def __init__(self, world) -> None:

        self.world = world
        self.packages = [
            'input',
            'output',
            'constructor'   
        ]

        self.baseClass=[
            'InputBase',
            'OutputBase',
            'Constructor'
        ]

        self.plugin_package = 'mollab.plugins'
        
        self.reload_plugins()

    def reload_plugins(self):

        self.plugins = dict()
        
        self.seen_paths = list()
        print('--- message ---')
        print(f'在 {self.plugin_package} 中查找插件')
        print('---------------')


        self.walk_package(self.plugin_package)

    def walk_package(self, package):

        imported_package = __import__(package, fromlist=['blah'])
        for _, pluginName, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__+'.'):
            if not ispkg:
                module = __import__(pluginName, fromlist=['blah'])
                clsMembers = inspect.getmembers(module, inspect.isclass)
                    

                for (_, c) in clsMembers:
                    if issubclass(c, (InputBase, OutputBase, PrecastBase)):
                        if c is not InputBase and c is not OutputBase and c is not PrecastBase: 
                        
                            print(f'找到插件类：{c.__module__}. {c.__name__}')
                            self.plugins[c.__name__] = c

   # 现在我们已经查找了当前package中的所有模块，现在我们递归查找子packages里的附件模块
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])
        
        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)
    
                # 获取当前package中的子目录
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p)) and p != '__pycache__']
    
                # 递归遍历子目录的package
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)        
