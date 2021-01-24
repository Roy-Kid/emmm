from . import OutputBase
import sys, os, shutil

class OUTpdb(OutputBase):
    def __init__(self, world):
        super().__init__(world)

    def writeATOM(self):
        pass

    def writeCRYST1(self):
        pass

    def writeEND(self):
        pass