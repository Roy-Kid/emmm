from mollab.item import Item
from pprint import pprint
from itertools import combinations
print = pprint
import numpy as np

class Particle(Item):

    def __init__(self, style=None) -> None:
        super().__init__('Particle')
        self.style = style
        self.parent = None
        self.links = self._container
        self._x = 0
        self._y = 0
        self._z = 0

    def toJson(self, properties: dict=None):
        pjson =  {}
        for p in self.properties:
            pjson[p] = getattr(self, p)
        if properties is not None:
            pjson.update(properties)
        return pjson

    def fromJson(self, particle: dict):
        for k, v in particle.items():
            setattr(self, k, v)

        return self

    def link(self, *particles):
        for particle in particles:

            if particle not in self.links:
                self.links.append(particle)
            if self not in particle:
                particle.links.append(self)

    @property
    def bonds(self):
        bonds = getattr(self, '_bonds', None)
        if bonds:
            return bonds
        else:
            self._bonds = self.search_bond()
            return self._bonds

    def getBonds(self):
        return [(self, i) for i in self]

    def getAngles(self):
        a = combinations(self, 2)
        tmp = [(i[0], self, i[1]) for i in a]
        return tmp

    def getDihedrals(self):
        angles = self.search_angle()
        tmp = []
        for angle in angles:
            dihedral = list(angle)
            bonded = angle[0]
            ds = bonded.linked
            for d in ds:
                if d not in dihedral:
                    t = tuple([d]+dihedral)
                    tmp.append(t)

            bonded = angle[-1]
            ds = bonded.linked
            for d in ds:
                if d not in dihedral:
                    tmp.append(tuple(dihedral+[d]))
                    
        return tmp

    def getImpropers(self):
        if len(self.linked) < 3:
            return None
        else:
            tmp = [ [self]+list(i) for i in combinations(self.linked, 3) ]
        return tmp

    def __str__(self) -> str:
        return f' < particle {self.label} > '

    __repr__ = __str__

    def getDistance(self, particle):
        pass

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = float(x)

    def getCoordinate(self, isNdarray=False):
        if isNdarray:
            return np.array([self.x, self.y, self.z])
        else:
            return (self.x, self.y, self.z)

    @property
    def coordinate(self, isNdarray=False):
        return self.getCoordinate()

    def setCoordinate(self, coord):
        self._x, self._y, self._z = coord

    def duplicate(self):
        return Particle().fromJson(self.toJson())
