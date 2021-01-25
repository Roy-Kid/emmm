# author: Roy Kid

from collections import defaultdict
from emmm.core.molecule import Molecule


class InputData(dict):

    def __init__(self) -> None:
        self.filename = str()
        self.molecules = list()

    def __str__(self):
        return f'< InputData of {self.filename} >'

    __repr__ = __str__



class InputBase:
    """ The parent class for all the input parser
    """
    def __init__(self, world):
        
        self.world = world

    def group_by(self, filename:str, atoms:list, reference:str='parent'):
        """ Util method to group atoms by a certain reference. For example, you can group them by the molLable, which means those atoms in a same molecule. 

        Args:
            atoms (list): a list of atoms, usually generate by flatten()
            reference (str, optional): Keyword in Atom. Defaults to 'molLabel'.
            returnType (str, optional): [description]. Defaults to 'Molecule'.

        Returns:
            dict: {reference: molecule, } 
        """ 

        grouped_atoms = defaultdict(list)
        for atom in atoms:
            ref = getattr(atom, reference, 'UNDEFINED')
            atom.parent = ref
            grouped_atoms[ref].append(atom)
        ## above test passed
        molecules = list()
        for ref, gatom in grouped_atoms.items():
            mol = Molecule(ref)
            mol.parent = filename
            mol.add_items(*gatom)
            molecules.append(mol)
        return molecules