# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-24
# version: 0.0.2

import numpy as np
import copy


class Item:
    def __init__(self, itemType='Item'):
        """ Item 是所有物体的基类, 包括Universe, World, Molecule, Atom
        """

        self.properties = {
            'itemType': itemType,
            'x': 0,
            'y': 0,
            'z': 0,
            'pos': 0
        }

        self._x = 0
        self._y = 0
        self._z = 0
        self._pos = 0

        self.container = list()

    @property
    def id(self):
        return id(self)

    @property
    def itemType(self):
        return self.properties['itemType']

    def __iter__(self):
        return iter(self.container)

    def __next__(self):
        try:
            n = self.container[self.__pos]
            self.__pos += 1
        except IndexError:
            raise StopIteration
        return n

    # x,y,z(float) -> position(array) -> [operate] -> newpos(array)
    #      ^                                             |
    #      |-----------------assign--------------------- v

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
        return self.properties['x']

    @x.setter
    def x(self, x):
        self.properties['x'] = float(x)

    @property
    def y(self):
        return self.properties['y']

    @y.setter
    def y(self, y):
        self.properties['y'] = float(y)

    @property
    def z(self):
        return self.properties['z']

    @z.setter
    def z(self, z):
        self.properties['z'] = float(z)

    def _move(self, original, x, y, z):
        """move 的抽象数学方法
        """
        vec = np.array([x, y, z], dtype=float)
        return original + vec

    def _rotate(self, o, theta, x, y, z):
        """旋转的抽象方法
        """

        rotm = self._quaternion2rotmatrix(theta, x, y, z)

        newpos = np.dot(rotm, o)

        return newpos

    def _quaternion2rotmatrix(self, theta, x, y, z):
        """将四元数转换成旋转矩阵
        """

        # rotation axis
        x = float(x)
        y = float(y)
        z = float(z)

        if x == 0 and y == 0 and z == 0:
            raise ValueError('旋转轴设置错误')

        rotAxis = np.array([x, y, z])

        rotAxis = rotAxis / np.linalg.norm(rotAxis)
        rotAxisX, rotAxisY, rotAxisZ = rotAxis

        # half theta = theta/2
        htheta = np.pi * theta / 2
        # sin theta = sin(htheta)
        stheta = np.sin(htheta)

        a = np.cos(htheta)
        b = stheta * rotAxisX
        c = stheta * rotAxisY
        d = stheta * rotAxisZ
        b2 = b**2
        c2 = c**2
        d2 = d**2
        ab = a * b
        ac = a * c
        ad = a * d
        bc = b * c
        bd = b * d
        cd = c * d

        # rotation matrix
        return np.array([[1 - 2 * (c2 + d2), 2 * (bc - ad), 2 * (ac + bd)],
                         [2 * (bc + ad), 1 - 2 * (b2 + d2), 2 * (cd - ab)],
                         [2 * (bd - ac), 2 * (ab + cd), 1 - 2 * (b2 + c2)]])

    def get_replica(self, newLabal):
        newMol = copy.deepcopy(self)
        newMol.label = newLabal
        return newMol

    def registe_properties(self, **kwargs):
        self.properties.update(kwargs)
        