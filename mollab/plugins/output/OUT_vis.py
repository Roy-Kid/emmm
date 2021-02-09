# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-09
# version: 0.0.1

from mollab.plugins.output.output_base import OutputBase
import eel


class OUTVis(OutputBase):

    def vis(self, world):

        self.world = world

        