# author: Roy Kids
from emmm.core.molecule import Molecule
from emmm.core.atom import Atom

class Topo:
    """ A class to search topological structure for the passed molecules; instanciated by the World class
    """
    def __init__(self, world) -> None:
        self.world = world
        
        # self.world['topoBond'] = list()
        # self.world['topoAngle'] = list()
        # self.world['topoDihedral'] = list()

    def search_topo(self, item, isBond=True, isAngle=True, isDihedral=True):
        """to search the topological structure for the passed molecules.

        Args:
            item (Molecule|Atom): item to be searche topo
            isBond (bool, optional): if need to search bond. Defaults to True.
            isAngle (bool, optional): if need to search angle. Defaults to True.
            isDihedral (bool, optional): if need to search dihedral. Defaults to True.
        """

        if isinstance(item, Molecule):
            self.atoms = item.flatten() # <-molecule._flatten()
        elif isinstance(item, Atom):
            self.atoms = [item]
            
        # self.atoms is a list of Atoms
        
        self.forcefield = self.world.forcefield
        if isBond:
            self.world['topoBond'].extend(self.search_bond(self.atoms))
        if isAngle:
            self.world['topoAngle'].extend(self.search_angle(self.atoms))
        if isDihedral:
            self.world['topoDihedral'].extend(self.search_dihedral(self.atoms))

    def search_bond(self, atoms):

        bonds = list()
        for atom in atoms:
            bond = [atom]
            for ato in atom.get_neighbors():
                if ato in bond:
                    continue
                elif ato not in bond:
                    bond.append(ato)
                    bon = sorted(bond)
                    if bon not in bonds:
                        bonds.append(bon)
                    bond.pop()
            bond.pop()
        return bonds

    def search_angle(self, atoms):
        angles = list()
        for atom in atoms:
            angle = [atom]
            for ato in atom.get_neighbors():
                angle.append(ato)

                for at in ato.get_neighbors():

                    if at in angle:
                        continue
                    elif at not in angle:
                        angle.append(at)
                        angl = sorted(angle)
                        if angl not in angles:
                            angles.append(angl)
                        angle.pop()
                angle.pop()
            angle.pop()

        return angles


    def search_dihedral(self, atoms):
        dihedrals = list()
        for atom in atoms:
            dihedral = [atom]
            for ato in atom.neighbor:
                dihedral.append(ato)
                for at in ato.neighbor:
                    if at in dihedral:
                        continue
                    elif at not in dihedral:
                        dihedral.append(at)
                        for a in at.neighbor:
                            if a in dihedral:
                                continue
                            elif a not in dihedral:
                                dihedral.append(a)
                                di = sorted(dihedral)
                                if di not in dihedrals:
                                    dihedrals.append(di)
                                dihedral.pop()
                        dihedral.pop()
                dihedral.pop()
            dihedral.pop()
        return dihedrals
        
    def match_atoms(self, atoms1:list, atoms2:list)->bool: 
        return sorted(atoms1) == sorted(atoms2)

    def gen_bond(self):
        """ match [Atom1, Atom2] with forcefield to get bond type; then convert it to [type, label1, label] in str.

        Args:
            source_bonds ([type]): [description]
            bond_coeff ([type]): [description]
        """
        raw_bonds = self.world['topoBond']
        typed_bonds = list()


        for bond in raw_bonds:

            # bondinfo = [bondStyle, coeff1, coeff2]
            bondinfo = self.world.forcefield.match_bond(*bond)
            typed_bonds.append([*bondinfo, *bond])


        return typed_bonds
    