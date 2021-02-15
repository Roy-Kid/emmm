# author: Roy Kid

from mollab.core.item import Item
import numpy as np
from mollab.i18n.i18n import _


class Atom(Item):
    def __init__(self, style):

        super().__init__('Atom')
        self._style = style

        self._duplicate = [self]
        self._neighbors = list()

    def __str__(self) -> str:
        return f' < Atom: {self.label} in {self.parent} at {self.position} > '

    __repr__ = __str__

    @property
    def uuid(self):
        return id(self)

    @property
    def id(self):
        return self._id

    @property
    def style(self):
        return self._style

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, m):
        self._mass = float(m)

    @property
    def neighbors(self):
        return self._neighbors

    def add_neighbors(self, *atoms):
        """ 给atom添加相键接的atom

        """
        for atom in atoms:
            if isinstance(atom, Atom):
                if atom not in self:
                    self._neighbors.append(atom)
                if self not in atom:
                    atom._neighbors.append(self)

            else:
                raise TypeError(_('相邻的atom应该是 ATOM类 而不是 %s' % (type(atom))))

    # _move()方法输入的是np.array和float
    # 输出的是np.array, 所以测试的时候仅需要测试这个函数即可

    def move(self, x, y, z):
        """ move by (x, y, z)
        """
        newpos = self._move(self.position, x, y, z)
        self.position = newpos
        return self

    def move_to(self, x, y, z):
        """ move to (x, y, z)
        """
        self.position = (x, y, z)
        return self

    def randmove(self, length):
        """ 以当前位置为球心, length为半径随机方向移动
        Args:
            length (Float): 移动距离
        """
        vec = np.random.rand(3)
        vec /= np.linalg.norm(vec)
        vec *= length

        self.move(*vec)
        return self

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        """ 以四元数的方式旋转atom. (x,y,z)是空间指向, (xo,yo,zo)是中心点, 即旋转轴为(x-xo,y-yo,z-zo). theta则是围绕旋转轴逆时针旋转的弧度(多少个π).
        """
        disVec = np.array([x0, y0, z0])

        self.move(*-disVec)

        # np.dot(rotm, self.position, out=self.position)
        self.position = self._rotate(self.position, theta, x, y, z)

        self.move(*disVec)
        return self

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):
        """ 围绕(x,y,z)点的x/y/z轴旋转theta角

        Raises:        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
            SyntaxError: [description]
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

        temp = []
        for j in self._duplicate:
            for i in range(1, n + 1):
                atom = j.get_replica(j.label)
                atom.move(i * x, i * y, i * z)
                temp.append(atom)

        self._duplicate.extend(temp)

        return self

    def toDict(self):

        return {
            'item': self.itemType,
            'id': self.id,
            'label': self.label,
            'type': self.type,
            'parent': self.parent,
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }


class fullAtom(Atom):
    def __init__(self, atomId, molId, type, q, x, y, z):

        super().__init__('full')
        self.atomId = atomId
        self.molId = molId
        self.type = type
        self.q =  float(q)
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

        self._id = self.atomId
        self._type = self.type



class molecularAtom(Atom):
    def __init__(self, atomId, molId, typeId, x, y, z):
        super().__init__('molecular')
        self.atomId = atomId
        self.molId = molId
        self.type = type
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

        self._id = self.atomId


class pdbAtom(Atom):
    def __init__(self, serial, name, altLoc, resName, chainID, resSeq, x, y, z,
                 occupancy, tempFactor, element, charge):
        super().__init__('pdb')
        self.serial = serial
        self.name = name
        self.altLoc = altLoc
        self.resName = resName
        self.resSeq = resSeq
        self.chainID = chainID
        self._x = x
        self._y = y
        self._z = z
        self.occupancy = occupancy
        self.tempFactor = tempFactor
        self.element = element
        self.charge = charge

        self._id = self.serial
