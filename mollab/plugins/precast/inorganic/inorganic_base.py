from .. import PrecastBase
from mollab.core.molecule import Molecule

class InorganicBase(PrecastBase):
    def __init__(self, world) -> None:
        self.world = world
        super().__init__(world)
    
    def _duplicate(self, move_vec, num_replicas):
        mol_temp = self.mol.get_replica('template')
        for i in range(1, num_replicas):
            mol_new = mol_temp.get_replica('none')
            mol_new.move(move_vec[0]*i, move_vec[1]*i, move_vec[2]*i)
            for mol in mol_new.container:
                mol.label = '%s_%d' %(self.name, len(self.mol.container))
                self.mol.add_items(mol)

    def _input_complete(self):
        self._generateLattice()
        self._duplicate(self.cell_vec[:, 0], self.num_x)
        self._duplicate(self.cell_vec[:, 1], self.num_y)
        self._duplicate(self.cell_vec[:, 2], self.num_z) 