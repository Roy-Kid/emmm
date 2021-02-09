from . import Item
class select:
    """ A class stores operations to select and filter molecules
 
    """

    @staticmethod
    def union(item1:Item, item2:Item):
        """Take Union in two groups of molecules. If two args are both a list of atom/molecule, then return the union of theirs. If one is a list atoms and other is a molecule then also can return the union. DO NOT PASS A LIST OF ATOMS AND A LIST OF MOLECULE.

        Args:
            item1 (Atoms|Molecule): atoms in list, or a molecule.
            item2 (Atoms|Molecule)

        Returns:
            item: union
        """
        atoms = list()
        return atoms

    @staticmethod
    def intersection(item1, item2):
        """Take Intersection in two groups of molecules. If two args are both a list of atom/molecule, then return the union of theirs. If one is a list atoms and other is a molecule then also can return the union. DO NOT PASS A LIST OF ATOMS AND A LIST OF MOLECULE.

        Args:
            item1 (Item):
            item2 (Item):

        Returns:
            item: intersection
        """
        atoms = list()
        return atoms

    @staticmethod
    def complement(item1, item2):
        """Take complement of item1 in item2; that means item2 is bigger range than item1. If two args are both a list of atom/molecule, then return the union of theirs. If one is a list atoms and other is a molecule then also can return the union. DO NOT PASS A LIST OF ATOMS AND A LIST OF MOLECULE.

        Args:
            item1 (Item):small one
            item2 (Item):big one

        Returns:
            item: complement
        """
        atoms = list()
        return atoms