# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-29
# version: 0.0.1

from mollab.core.item import Item

class Universe(Item):
    def __init__(self):
        
        super().__init__('Universe')

        self.worlds = list()

    def add_world(self, world):
        self.worlds.append(world)
