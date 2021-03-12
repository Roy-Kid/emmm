# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-24
# version: 0.0.2

from mollab.core.neighborlist import NeighborList
from mollab.core.item import Item
import numpy as np


class Atom(Item):
    """Atom 是所有粒子的基类, 提供了所有粒子共有的方法. 在这个基础上可以派生出各种具有不同属性的Atom类
    """
    def __init__(self, loadAtom=None, **kwarg):

        super().__init__('Atom')

        self.register_properties(style=kwarg.get('style', 'Atom'),
                                 mass=0,
                                 type='',
                                 label='',
                                 parent='',
                                 root='')
        # 自复制的列表
        self._duplicate = [self]
        # 键接原子的列表
        self._linkedAtoms = list()
        # 临近原子
        self._neighbors = NeighborList()

    def __str__(self) -> str:
        return f' < Atom > '

    @property
    def type(self):
        return self.properties['type']

    @type.setter
    def type(self, t):
        self.properties['type'] = t

    @property
    def label(self):
        return self.properties['label']

    @label.setter
    def label(self, v):
        self.properties['label'] = v

    @property
    def parent(self):
        return self.properties['parent']

    @parent.setter
    def parent(self, p):
        self.properties['parent'] = p

    @property
    def root(self):
        return self.properties['root']

    @root.setter
    def root(self, r):
        self.properties['root'] = r

    __repr__ = __str__

    @property
    def style(self):
        return self.properties['style']

    @property
    def mass(self):
        return self.properties['mass']

    @mass.setter
    def mass(self, m):
        self.properties['mass'] = float(m)

    @property
    def linkedAtoms(self):
        return self._linkedAtoms

    def add_linkedAtoms(self, *atoms):
        """添加键接的Atom. TODO: 将键接Atom和临近Atom区分开

        Raises:
            TypeError: 添加了错误种类的对象而不是Atom
        """
        for atom in atoms:
            if isinstance(atom, Atom):
                if atom not in self:
                    self._linkedAtoms.append(atom)
                if self not in atom:
                    atom._linkedAtoms.append(self)

            else:
                raise TypeError('相邻的atom应该是 ATOM类 而不是 %s' % (type(atom)))

    # _move()方法输入的是np.array和float
    # 输出的是np.array, 所以测试的时候仅需要测试这个函数即可

    def move(self, x, y, z):
        """将Atom向一个方向移动

        Args:
            x (float): 在x方向的移动
            y (float): 在y方向的移动
            z (float): 在z方向的移动

        Returns:
            Atom: 返回自身, 以供链式操作
        """
        newpos = self._move(self.position, x, y, z)
        self.position = newpos
        return self

    def move_to(self, x, y, z):
        """将Atom移动到

        Args:
            x (float): 目标x坐标
            y (float): 目标y坐标
            z (float): 目标z坐标

        """
        self.position = (x, y, z)
        return self

    def randmove(self, length):
        """以当前位置为球心, length为半径随机方向移动

        Args:
            length (float): 移动距离
        """
        vec = np.random.rand(3)
        vec /= np.linalg.norm(vec)
        vec *= length

        self.move(*vec)
        return self

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        """以四元数的方式旋转atom. (x,y,z)是旋转轴空间指向, (x0,y0,z0)是旋转轴起始点(默认原点), 即旋转轴为(x-xo,y-yo,z-zo). theta则是围绕旋转轴逆时针旋转的弧度(多少个π).

        Args:
            theta ([type]): [description]
            x ([type]): [description]
            y ([type]): [description]
            z ([type]): [description]
            x0 (int, optional): [description]. Defaults to 0.
            y0 (int, optional): [description]. Defaults to 0.
            z0 (int, optional): [description]. Defaults to 0.

        Returns:
            [type]: [description]
        """
        disVec = np.array([x0, y0, z0])

        self.move(*-disVec)

        # np.dot(rotm, self.position, out=self.position)

        self.position = self._rotate(self.position, theta, x, y, z)

        self.move(*disVec)
        return self

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):
        """围绕在(x,y,z)点的x/y/z轴旋转theta

        Args:
            theta (deg): 旋转角
            x (float): 旋转参考点
            y (float): 旋转参考点
            z (float): 旋转参考点
            xAxis (bool): 旋转轴指向
            yAxis (bool): 旋转轴指向
            zAxis (bool): 旋转轴指向

        Raises:
            SyntaxError: 只能有一个方向被设置成True来代表旋转轴指向
        """

        if (xAxis, yAxis, zAxis) == (1, 0, 0) or\
           (xAxis, yAxis, zAxis) == (0, 1, 0) or\
           (xAxis, yAxis, zAxis) == (0, 0, 1):

            self.rotate(theta, xAxis, yAxis, zAxis, x, y, z)
        else:
            raise SyntaxError(
                _('为了指定空间中(x,y,z)的旋转轴的朝向, 需要将方向设定为1. 如: 旋转轴指向x方向则xAxis=1, yAxis=zAxis=0'
                  ))
        return self

    def seperate_with(self, targetItem, type, value):
        """ [Bioperate] to seperate two items in opposite direction: (rel)ative distance is move EACH item in a distance under system unit; (abs)olute distance is the time of current distance of two items, e.g.: item+=unit_orientation_vector*rel; item+=orientation_vector*abs.

        Args:
            targetItem (Item): Atom|Molecule
            type (str): rel|abs
            value (Float): distance
        """
        # orientation vector
        if all(self.position == targetItem.position):
            raise ValueError(_("两个atom完全重叠, 无法计算方向矢量"))
        oriVec = targetItem.position - self.position

        distance = np.linalg.norm(oriVec)

        uniVec = oriVec / distance

        if type == 'relative' or type == 'rel':

            distance = distance * (value - 1) / 2

            self.move(*-uniVec * distance)
            targetItem.move(*+uniVec * distance)

        if type == 'abusolute' or type == 'abs':
            self.move(*-uniVec * value)
            targetItem.move(*+uniVec * value)
        return self

    def distance_to(self, targetItem):
        """[Bioperate] return the distance to a target item

        Args:
            targetItem (Item): Atom|Molecule
        """
        coords1 = self.position
        coords2 = targetItem.position

        dist = np.linalg.norm(coords2 - coords1)

        return dist

    def duplicate(self, n, x, y, z):
        """沿着一个方向边移动边复制

        Args:
            n (int): 复制个数
            x (float): 每移动距离复制一次
            y (float): 每移动距离复制一次
            z (float): 每移动距离复制一次

        """

        temp = []
        for j in self._duplicate:
            for i in range(1, n + 1):
                atom = j.get_replica(j.label)
                atom.move(i * x, i * y, i * z)
                temp.append(atom)

        self._duplicate.extend(temp)

        return self

    def save_dict(self, fname=None):

        if not fname:
            return self.properties


class fullAtom(Atom):
    def __init__(self, atomId, molId, type, q, x, y, z, mass=None):

        super().__init__(style='full')
        q = float(q)
        x = float(x)
        y = float(y)
        z = float(z)

        self.register_properties(atomId=atomId,
                                 molId=molId,
                                 type=type,
                                 q=q,
                                 x=x,
                                 y=y,
                                 z=z, 
                                 mass=mass)

        self.type = type
        self.label = atomId

    @property
    def atomId(self):
        return self.properties['atomId']

    @atomId.setter
    def atomId(self, v):
        self.properties['atomId'] = v

    @property
    def molId(self):
        return self.properties['molId']

    @property
    def q(self):
        return self.properties['q']

    def __str__(self) -> str:
        return f'< Atom {self.type}: {self.atomId} in {self.molId} at ({self.x},{self.y},{self.z})>'


class molecularAtom(Atom):
    def __init__(self, atomId, molId, type, x, y, z):
        super().__init__(style='molecular')
        x = float(x)
        y = float(y)
        z = float(z)
        self.register_properties(atomId=atomId,
                                 molId=molId,
                                 type=type,
                                 x=x,
                                 y=y,
                                 z=z)
        self.type = type

    @property
    def atomId(self):
        return self.properties['atomId']

    @atomId.setter
    def atomId(self, v):
        self.properties['atomId'] = v

    @property
    def molId(self):
        return self.properties['molId']

    def __str__(self) -> str:
        return f'< Atom {self.type}: {self.atomId} in {self.molId} at ({self.x},{self.y},{self.z})>'


class pdbAtom(Atom):
    def __init__(self, serial, name, altLoc, resName, chainID, resSeq, x, y, z,
                 occupancy, tempFactor, element, charge):
        super().__init__(style='pdb')
        x = float(x)
        y = float(y)
        z = float(z)
        self.register_properties(serial=serial,
                                 name=name,
                                 altLoc=altLoc,
                                 resName=resName,
                                 resSeq=resSeq,
                                 chainID=chainID,
                                 x=x,
                                 y=y,
                                 z=z,
                                 occupancy=occupancy,
                                 tempFactor=tempFactor,
                                 element=element,
                                 charge=charge)

        self.type = resName
