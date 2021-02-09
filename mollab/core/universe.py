# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-29
# version: 0.0.1

from .world import World

class Universe(World):

    def __init__(self) -> None:
        super().__init__()

        self.worlds = list()

    def __str__(self) -> str:
        return f'<Universe has {len(self.worlds)} worlds>'

    def add_worlds(self, *worlds):

        for w in worlds:
            self.worlds.append(w)
        