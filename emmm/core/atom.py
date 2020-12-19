# author: Roy Kid

from emmm.core.item import Item
import numpy as np

class Atom(Item):

    def __init__(self, label=None, type=None, parent=None, path=None):

        super().__init__()

        self.label = label
        self.type = type
        self.parent = parent
        self.path = path

    def __str__(self) -> str:
        return f' < Atom: {self.label} in {self.parent} > '

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

    def randmove(self, length):
        """ 以当前位置为球心, length为半径随机方向移动
        Args:
            length (Float): 移动距离
        """
        vec = np.random.rand(3)
        vec /= np.linalg.norm(vec)
        vec *= length

        self.position += vec

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        """ 以四元数的方式旋转atom. (x0=0,y0=0,z0=0)到(x,y,z)形成旋转轴, theta则是围绕旋转轴逆时针旋转的弧度(多少个π). 

        Args:
            theta (radian): theta:=theta*PI
            x (float): to
            y (float): to
            z (float): to
            x0 (float): from
            y0 (float): from
            z0 (float): from
        """
        # rotation axis
        x = float(x)
        y = float(y)
        z = float(z)
        x0 = float(x0)
        y0 = float(y0)
        z0 = float(z0)
        disVec = np.array([x0, y0, z0])
        rotAxis = np.array([x, y, z])

        rotAxis = rotAxis/np.linalg.norm(rotAxis)
        rotAxisX, rotAxisY, rotAxisZ = rotAxis

        # half theta = theta/2
        htheta = np.pi*theta/2
        # sin theta = sin(htheta)
        stheta = np.sin(htheta)

        a = np.cos(htheta)
        b = stheta*rotAxisX
        c = stheta*rotAxisY
        d = stheta*rotAxisZ
        b2 = b**2
        c2 = c**2
        d2 = d**2
        ab = a*b
        ac = a*c
        ad = a*d
        bc = b*c
        bd = b*d
        cd = c*d

        # rotation matrix
        rotm = np.array([[1-2*(c2+d2), 2*(bc-ad), 2*(ac+bd)],
                         [2*(bc+ad), 1-2*(b2+d2), 2*(cd-ab)],
                         [2*(bd-ac), 2*(ab+cd), 1-2*(b2+c2)]])

        self.position -= disVec
        self.position = np.dot(rotm, self.position)
        self.position += disVec

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):

        """ 围绕(x,y,z)点的x/y/z轴旋转theta角

        Raises:
            SyntaxError: [description]
        """

        if (x, y, z) == (1, 0, 0) or\
           (x, y, z) == (0, 1, 0) or\
           (x, y, z) == (0, 0, 1):

            self.rotate(self, theta, x+xAxis, y+yAxis, z+zAxis, x, y, z)
        else:
            raise SyntaxError(_('为了指定空间中(x,y,z)的旋转轴的朝向, 需要将方向设定为1. 如: 旋转轴指向x方向则xAxis=1, yAxis=zAxis=0'))

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
        print(oriVec, targetItem.position, self.position)
        uniVec = oriVec/np.linalg.norm(oriVec)
        print(oriVec)

        if type == 'relative' or type == 'rel':
            self.move( *-uniVec*value )
            targetItem.move(*+uniVec*value)
        if type == 'abusolute' or type == 'abs':
            self.move( *-oriVec*value )
            targetItem.move(*+oriVec*value)

    def distance_to(self, targetItem):
        """[Bioperate] return the distance to a target item

        Args:
            targetItem (Item): Atom|Molecule
        """
        coords1 = self.position
        coords2 = targetItem.position
        print(coords1, coords2)

        dist = np.linalg.norm(coords2-coords1)

        return dist

    def get_replica(self, newLabal):

        atom = Atom()
        for k,v in self.__dict__.items():
            if k != "_Item__id":
                setattr(atom, str(k), v)
        return atom

    @property
    def pwd(self):
        return self.path