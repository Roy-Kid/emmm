# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-15
# version: 0.0.2

import numpy as np
import copy


class Item:
    """Item 是几乎所有可操作实体的基类, 包括且不限于Atom, Molecule, World, Universe, Bond, Angle, Dihedral, Improper. 
    """
    def __init__(self, itemType):

        self._id = str()
        self._label = str()
        self._parent = str()
        self._path = str()
        self._type = str()

        self._root = str()

        self._x = 0
        self._y = 0
        self._z = 0

        self.container = list()
        self.__pos = 0
        self._itemType = itemType

    @property
    def itemType(self):
        return self._itemType

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, r):
        self._root = r

    def __iter__(self):
        return iter(self.container)

    def __next__(self):
        try:
            n = self.container[self.__pos]
            self.__pos += 1
        except IndexError:
            raise StopIteration
        return n

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

    def _move(self, original, x, y, z):
        """move()的抽象方法, 只关心数学层面的移动向量计算

        Args:
            original (np.array): 初始位置向量
            x (float): 在x方向的移动
            y (float): 在y方向的移动
            z (float): 在z方向的移动

        Returns:
            np.array: 移动后的位置向量
        """
        vec = np.array([x, y, z], dtype=float)
        return original + vec

    def randmove(self):
        pass

    def _rotate(self, o, theta, x, y, z):
        """rotate()的抽象方法, 只关心数学层面的旋转计算

        Args:
            o (np.array): 初始位置向量
            theta (deg): 旋转角度
            x (float): 旋转轴指向的x分量
            y (float): 旋转轴指向的x分量
            z (float): 旋转轴指向的x分量

        Returns:
            np.array: 旋转后的位置向量
        """
        theta = np.deg2rad(theta)
        rotm = self._quaternion2rotmatrix(theta, x, y, z)

        newpos = np.dot(rotm, o)

        return newpos

    def _quaternion2rotmatrix(self, theta, x, y, z):
        """将四元数转换为旋转矩阵的数学方法

        Args:
            theta (deg): 旋转角度
            x (float): 旋转轴指向的x分量
            y (float): 旋转轴指向的x分量
            z (float): 旋转轴指向的x分量

        Raises:
            ValueError: xyz全为零时无法确定旋转轴

        Returns:
            np.array: 旋转矩阵(3x3)
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

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):
        pass

    def seperate_with(self, targetItem, type, value):
        pass

    def distance_to(self, targetItem):
        pass

    def get_replica(self, newLabal):
        newMol = copy.deepcopy(self)
        newMol.label = newLabal
        return newMol

    def compute_bounding_box(self):
        pass

    def compute_bounding_sphere(self):
        pass
