# author: Roy Kid

from emmm.core.item import Item
import numpy as np
from emmm.i18n.i18n import _

class Atom(Item):

    def __init__(self, label=None, type=None):

        super().__init__()

        self._label = label
        self._type = type

        self._duplicate = [self]


    def __str__(self) -> str:
        return f' < Atom: {self.label} in {self.parent} at {self.position}> '

    __repr__ = __str__ 

    def get_neighbors(self):
        return self.container

    def add_neighbors(self, *atoms):
        """ 给atom添加相键接的atom

        """
        for atom in atoms:
            if isinstance(atom, Atom):
                if atom not in self:
                    self.container.append(atom)
                if self not in atom:
                    atom.container.append(self)
                
            else:
                raise TypeError(_('相邻的atom应该是 ATOM类 而不是 %s'% (type(atom))))      

    def toDict(self):
        """ 输出到字典格式

        Returns:
            dict
        """

        # TODO: 适配额外添加的属性
        # atom.__dict__
        a = dict()
        a['label'] = self.label
        a['type'] = self.type
        a['parent'] = self.parent
        a['path'] = self.path
        a['x'] = self.x
        a['y'] = self.y
        a['z'] = self.z

    def move(self, x, y, z):
        """ 按照(x,y,z)矢量移动

        """
        vec = np.array([x, y, z], dtype=float)
        self.position += vec
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

    def rotate(self, theta, x, y, z, xo=0, yo=0, zo=0):
        """ 以四元数的方式旋转atom. (x,y,z)是空间指向, (xo,yo,zo)是中心点, 即旋转轴为(x-xo,y-yo,z-zo). theta则是围绕旋转轴逆时针旋转的弧度(多少个π).

        Args:
            theta (radian): theta:=theta*PI
            x (float): to
            y (float): to
            z (float): to
            xo (float): from
            yo (float): from
            zo (float): from
        """
        # rotation axis

        xo = float(xo)
        yo = float(yo)
        zo = float(zo)
        disVec = np.array([xo, yo, zo])

        rotm = self._quaternion2rotmatrix(theta, x, y, z)

        self.move(*-disVec)

        # np.dot(rotm, self.position, out=self.position)
        self.position = np.dot(rotm, self.position)

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
            raise SyntaxError(_('为了指定空间中(x,y,z)的旋转轴的朝向, 需要将方向设定为1. 如: 旋转轴指向x方向则xAxis=1, yAxis=zAxis=0'))
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

        uniVec = oriVec/distance

        if type == 'relative' or type == 'rel':

            distance = distance*(value-1)/2

            self.move( *-uniVec*distance )
            targetItem.move(*+uniVec*distance)

        if type == 'abusolute' or type == 'abs':
            self.move( *-uniVec*value )
            targetItem.move(*+uniVec*value)
        return self

    def distance_to(self, targetItem):
        """[Bioperate] return the distance to a target item

        Args:
            targetItem (Item): Atom|Molecule
        """
        coords1 = self.position
        coords2 = targetItem.position

        dist = np.linalg.norm(coords2-coords1)

        return dist

    def get_replica(self, newLabal):

        atom = Atom(newLabal)

        for k,v in self.__dict__.items():
            if k != "_Item__id":
                setattr(atom, str(k), v)
        return atom

    @property
    def pwd(self):
        return self.path

    def duplicate(self, n, x, y, z):
        
        temp = []
        for j in self._duplicate:
            for i in range(1, n+1):
                atom = j.get_replica(j.label)
                atom.move(i*x, i*y, i*z)
                temp.append(atom)

        self._duplicate.extend(temp)

        return self