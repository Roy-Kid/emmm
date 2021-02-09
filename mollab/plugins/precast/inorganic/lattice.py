# File: lattice.py
# Author: Zhenyu Wei
# This file will contain the constructors for the basic
#  lattcie structure like sc, bcc, fcc, dc, etc

from mollab.core.create import CreateAtom
from mollab.core.atom import Atom
from mollab.core.molecule import Molecule
from . import InorganicBase
import numpy as np

class Lattice(InorganicBase):
    def __init__(self, world):
        super().__init__(world)
        self.mol = Molecule('Lattice')
    
    def _generateLattice(self):
        lattice = Molecule('%s_%d' %(self.name, 0))
        for i in range(self.atom_relative_coord.shape[0]):
            coord = self.cell_vec.dot(self.atom_relative_coord[i, :])
            lattice.add_items(Create.create_atom_from_coord('%s_atom_%d' %(self.name, i), coord))
        self.mol.add_items(lattice)
        self.mol.label = self.name

    def _addWorld(self):
        self.world.molecules.add_items(self.mol)

    def sc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='sc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])      
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()

    def bcc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='bcc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0.5, 0.5, 0.5],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()

    def fcc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='fcc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()
    
    def dc(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='dc'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0],
            [0.25, 0.25, 0.25],
            [0.25, 0.75, 0.75],
            [0.75, 0.25, 0.75],
            [0.75, 0.75, 0.25],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()

    def hcp(self, lattice_constant=1, num_x=1, num_y=1, num_z=1, name='hcp'):
        # Structure info
        self.atom_relative_coord = np.array([
            [0, 0, 0],
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0],
            [0.25, 0.25, 0.25],
            [0.25, 0.75, 0.75],
            [0.75, 0.25, 0.75],
            [0.75, 0.75, 0.25],
        ])
        self.cell_vec = np.array([
            [lattice_constant, 0, 0],
            [0, lattice_constant, 0],
            [0, 0, lattice_constant],
        ])
        self.num_x = num_x
        self.num_y = num_y
        self.num_z = num_z
        self.name = name
        self._input_complete()