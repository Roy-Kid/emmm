# author: Roy Kid

from emmm.core.atom import Atom
from emmm.core.item import Item
from copy import deepcopy
import numpy as np


class Molecule(Item):

    id = 0

    def __init__(self, label=None, type=None, parent=None, path=None, isAdhere=False):

        self.container = list()

        self._id = Molecule.id
        Molecule.id += 1

    def __repr__(self) -> str:
        return f'< molecule: {self.label} in {self.parent}>'

    __str__ = __repr__ 

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, v):
        self._label = v

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, v):
        self._type = v

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, v):
        self._parent = v

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, v):
        self._path = v

    @property
    def isAdhere(self):
        return self._isAdhere

    @isAdhere.setter
    def isAdhere(self, v):
        self._isAdhere = v

    def get_items(self):
        return self

    def add_items(self, *items):
        """ 向molecule中添加item
        """
        for item in items:
            if isinstance(item, Atom):
                item.parent = self.label
                # Item has append method to add item to self.container
                self.container.append(item)
                self.coords.append(item.position)

            elif isinstance(item, Molecule):
                item.parent = self.label
                for i in item.coords:
                    self.coords.append(i)
                self.container.append(item)

    def __getitem__(self, label):

        if isinstance(label, str):
            for item in self:
                if item.label == label:
                    return item

        elif isinstance(label, slice):
            raise TypeError(_('暂不支持切片调用'))

    def flatten(self, dir=None, isSelf=False):

        if dir is None:
            dir = [self.label]

        else:
            dir.append(self.label)
        atoms = list()
        for item in self:
            if isinstance(item, Atom):
                dir.append(item.label)
                item.path = '/'.join(dir)
                atoms.append(item)
                dir.pop()

            elif isinstance(item, Molecule) and isSelf:
                atoms.append(item)
                atoms.append(item.flatten(dir))

            elif isinstance(item, Molecule) and not isSelf:
                atoms.extend(item.flatten(dir))

        dir.pop()
        return atoms

    def calc_centroid(self):
        atoms = self.flatten()
        vec = np.array([0, 0, 0], dtype=float)
        for atom in atoms:
            vec += atom.position

        centroid = vec/len(atoms)
        setattr(self, 'position', centroid)

    def toDict(self):
        m = dict()
        m['label'] = self.label
        m['type'] = self.type
        m['parent'] = self.parent
        m['path'] = self.path
        m['items'] = list()
        for i in self.container:
            m['items'].append(i.toDict())

        return m

    def get_replica(self, newLabal):

        newMol = Molecule(newLabal)
        for k, v in self.__dict__.items():
            newMol[k] = v

        return newMol

    @property
    def position(self):
        if not hasattr(self, 'coords'):
            self.calc_centroid()
        return self._position

    @property
    def coords(self):

        coords = list()

        atoms = self.flatten()
        for atom in atoms:

            coords.append(atom.position)

        self._coords = coords
        return self._coords
