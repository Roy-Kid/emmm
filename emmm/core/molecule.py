# author: Roy Kid

from numpy.lib.arraysetops import isin
from emmm.core.atom import Atom
from emmm.core.item import Item
import numpy as np
from emmm.i18n.i18n import _


class Molecule(Item):



    def __init__(self, label=None, type=None, isAdhere=False):

        super().__init__()

        self._label = label
        self._type = type
        self.isAdhere = isAdhere        

        self._duplicate = [self]



    def __repr__(self) -> str:
        return f'< molecule: {self.label} in {self.parent}>'

    __str__ = __repr__



    def add_items(self, *items):
        """ 向molecule中添加item
        """
        for item in items:
            if isinstance(item, Atom) or isinstance(item, Molecule):
                item.parent = self.label
                self.container.append(item)

            else:
                raise TypeError(_('传入的类型错误'))

        self.update()

    def __getitem__(self, label):

        if isinstance(label, str):
            for item in self:
                if item.label == label:
                    return item

        elif isinstance(label, int):
            return self.container[label]

        elif isinstance(label, slice):
            raise TypeError(_('暂不支持切片调用'))

    def flatten(self, dir=None, isMol=False):

        if dir is None:
            dir = [self.label]

        else:
            dir.append(self.label)
        atoms = list()
        for item in self:

            if self.isAdhere:
                item.root = self.root
                if isinstance(item, Molecule): 
                    item.isAdhere = True

            if isinstance(item, Atom):
                dir.append(item.label)
                item.path = '/'.join(dir)
                atoms.append(item)
                dir.pop()

            elif isinstance(item, Molecule):

                atoms.extend(item.flatten(dir))

                if isMol:
                    atoms.append(item)


        dir.pop()
        return atoms

    def calc_centroid(self):
        atoms = self.flatten()
        vec = np.array([0, 0, 0], dtype=float)
        for atom in atoms:
            vec += atom.position

        centroid = vec/len(atoms)
        setattr(self, '_position', centroid)

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

    # def get_replica(self, newLabal):

    #     newMol = Molecule(newLabal)
    #     for k, v in self.__dict__.items():
    #         if k != "_Item__id" and k != "container":

    #             setattr(newMol, str(k), v)

    #     for item in self:
    #         newMol.add_items(item.get_replica(item.label))

    #     return newMol

    @property
    def position(self):
        if not hasattr(self, '_position'):
            self.calc_centroid()
        return self._position

    @property
    def coords(self):
        coords = list()
        for atom in self.flatten():
            coords.append(atom.position)
        return np.array(coords)

    def move(self, x, y, z):
        
        for atom in self:
            atom.move(x, y, z)

        self.update()

        return self

    def update(self):
        self.calc_centroid()

    def distance_to(self, item):
        position1 = self.position
        position2 = item.position
        dist = np.linalg.norm(position2-position1)

        return dist

    def randmove(self, length):
        vec = np.random.rand(3)
        vec /= np.linalg.norm(vec)
        vec *= length

        for atom in self.flatten():
            atom.move(*vec)

        self.update()

    def rotate(self, theta, x, y, z, xo=0, yo=0, zo=0):

        for atom in self.flatten():
            atom.rotate(theta, x, y, z, xo, yo, zo)

        self.update()
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
                _('为了指定空间中(x,y,z)的旋转轴的朝向, 需要将方向设定为1. 如: 旋转轴指向x方向则xAxis=1, yAxis=zAxis=0'))

    def seperate_with(self, targetItem, type, value):
        if all(self.position == targetItem.position):
            raise ValueError(_("两个atom完全重叠, 无法计算方向矢量"))
        oriVec = targetItem.position - self.position

        distance = np.linalg.norm(oriVec)

        uniVec = oriVec/distance

        if type == 'relative' or type == 'rel':

            distance = distance*(value-1)/2

            self.move(*-uniVec*distance)
            targetItem.move(*+uniVec*distance)

        if type == 'abusolute' or type == 'abs':
            self.move(*-uniVec*value)
            targetItem.move(*+uniVec*value)
        return self


    def duplicate(self, n, x, y, z):
        
        temp = []
        for j in self._duplicate:
            for i in range(1, n+1):
                mol = j.get_replica(j.label)
                mol.move(i*x, i*y, i*z)
                temp.append(mol)

        self._duplicate.extend(temp)

        return self