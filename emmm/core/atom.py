# author: Roy Kid
from emmm.core.item import Item

class Atom(Item):

    id = 0

    def __init__(self, label=None, type=None, parent=None, path=None):
        super().__init__(label=label, type=type, parent=parent, path=path)

        self.id = Atom.id
        Atom.id += 1

    def __str__(self) -> str:
        return f' < Atom: {self.label} in {self.parent} > '

    __repr__ = __str__

    def get_neighbors(self):
        return self

    def add_neighbors(self, *atoms):
        for atom in atoms:
            if isinstance(atom, Atom):
                if atom not in self:
                    self.append(atom)
                if self not in atom:
                    atom.append(self)
                
            else:
                raise TypeError(f'"{type(atom)}"" is not an Atom class')       

    def toDict(self):
        """ convert atom to dict

        Returns:
            dict
        """
        a = dict()
        a['label'] = self.label
        a['type'] = self.type
        a['parent'] = self.parent
        a['path'] = self.path
        a['x'] = self.x
        a['y'] = self.y
        a['z'] = self.z
        return a 
