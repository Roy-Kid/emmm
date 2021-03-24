# # author: Roy Kid
# # contact: lijichen365@126.com
# # date: 2021-02-24
# # version: 0.0.1

import math
from mollab.core.dstru import ndarray

class NeighborList:

    def __init__(self, world, cutoff=None) -> None:
        self.world = world
        self.atoms = world.atoms

        self.maxCutoff = cutoff

        # for atom in self.atoms:
        #     self.maxCutoff = max(self.maxCutoff, atom.cutoff)
        self.build(self.mesh())


    def mesh(self):
        self.xlo, self.xhi = self.world.xlo, self.world.xhi
        self.ylo, self.yhi = self.world.ylo, self.world.yhi
        self.zlo, self.zhi = self.world.zlo, self.world.zhi
        self.xl = self.xhi - self.xlo
        self.yl = self.yhi - self.ylo
        self.zl = self.zhi - self.zlo
        self.x_meshCount = self.xl / math.floor(self.xl/self.maxCutoff)
        self.y_meshCount = self.yl / math.floor(self.yl/self.maxCutoff)
        self.z_meshCount = self.zl / math.floor(self.zl/self.maxCutoff) 
        mesh = ndarray(self.x_meshCount, self.y_meshCount, self.z_meshCount)

        for atom in self.atoms:
            x_meshIndex = (atom.x + self.xlo) // self.x_meshCount
            y_meshIndex = (atom.y + self.xlo) // self.y_meshCount
            z_meshIndex = (atom.z + self.xlo) // self.z_meshCount
            mesh.get(x_meshIndex, y_meshIndex, z_meshIndex).append(atom)

        return mesh

    def build(self, atom, mesh):

        x_mesh_index = (atom.x + self.xlo) / self.maxCutoff
        y_mesh_index = (atom.y + self.ylo) / self.maxCutoff
        z_mesh_index = (atom.z + self.zlo) / self.maxCutoff
        