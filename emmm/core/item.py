# author: Roy Kid

import numpy as np
from uuid import uuid4

class Item:

    def __init__(self):

        self._label = str()
        self._parent = str()
        self._path = str()
        self._type = str()

        self._x = float()
        self._y = float()
        self._z = float()
        self.__id = uuid4()

        self.container = list()
        self.__pos = 0

        # in the Atom, _coords = _position
        # in the mol, _coords contains all the atoms' coordinates, _position is the barycenter of the moleule

    @property
    def id(self):
        return self.__id

    def __iter__(self):
        return iter(self.container)

    def __next__(self):
        try:
            n = self.container[self.__pos]
            self.__pos += 1
        except IndexError:
            raise StopIteration
        return n

    def ls(self):
        print(self.container)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, v):
        self._label = str(v)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, v):
        self._type = str(v)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, v):
        self._parent = str(v)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, v):
        self._path = str(v)

    @property
    def position(self):
        return np.array([self.x, self.y, self.z])

    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z


    

    def move(self, x, y, z):
        pass

    def randmove(self, length):
        pass

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        pass

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):
        pass

    def seperate_with(self, targetItem, type, value):
        pass
    
    def distance_to(self, targetItem):
        pass

    def get_replica(self, newLabal):
        pass

    def compute_bounding_box(self):
        pass

    def compute_bounding_sphere(self):
        pass
