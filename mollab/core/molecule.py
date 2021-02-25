# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-25
# version: 0.0.2

from mollab.core.item import Item
import numpy as np
from mollab.i18n.i18n import _
from mollab.core.topo import Topo


class Molecule(Item):
    def __init__(self, loadAtom=None, **kwarg):

        super().__init__('Molecule')

        self.registe_properties(style=kwarg.get('style', 'Molecule'),
                                mass=0,
                                type='',
                                parent='',
                                label='',
                                root='')

        self._duplicate = [self]


    def __str__(self) -> str:
        return f'< Molecule >'

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

    @property
    def atoms(self):
        return self.flatten()

    __repr__ = __str__

    def add_items(self, *items):
        """向Molecule中添加item

        Raises:
            TypeError: 如果不是Atom或者Molecule则报错
        """
        for item in items:
            if item.itemType == 'Molecule' or item.itemType == 'Atom':
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
        """将Molecule中储存的item压平, 换言之就是提取出所有的atom

        Args:
            dir (str, optional): 压平时需要传递的路径. Defaults to None.
            isMol (bool, optional): 压平时是否将Molecule也添加到列表中. Defaults to False.

        Returns:
            list: 由atoms组成的列表
        """

        if dir is None:
            dir = [self.label]

        else:
            dir.append(self.label)
        atoms = list()
        for item in self:

            item.root = self.root

            if item.itemType == 'Atom':
                dir.append(item.label)
                item.path = '/'.join(dir)
                atoms.append(item)
                dir.pop()

            elif item.itemType == 'Molecule':

                atoms.extend(item.flatten(dir))

                if isMol:
                    atoms.append(item)

        dir.pop()
        return atoms

    def calc_centroid(self):
        """计算Molecule的质心
        """
        atoms = self.flatten()
        vec = np.array([0, 0, 0], dtype=float)
        for atom in atoms:
            vec += atom.position

        centroid = vec / len(atoms)
        setattr(self, '_position', centroid)

    def save_dict(self):
        m = dict()
        m.update(self.properties)
        i = list()
        for item in self.container:
            if item.itemType == 'Atom':
                i.append(item.save_dict())
            elif item.itemType == 'Molecule':
                i.append(item.save_dict())
        m.update({'item': i})
        return m


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
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
            z ([type]): [description]

        Returns:
            [type]: [description]
        """

        for atom in self:
            atom.move(x, y, z)

        self.update()

        return self

    def update(self):
        """手动更新Molecule的状态
        """
        self.calc_centroid()

    def distance_to(self, item):
        position1 = self.position
        position2 = item.position
        dist = np.linalg.norm(position2 - position1)

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
                _('为了指定空间中(x,y,z)的旋转轴的朝向, 需要将方向设定为1. 如: 旋转轴指向x方向则xAxis=1, yAxis=zAxis=0'
                  ))

    def seperate_with(self, targetItem, type, value):
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

    def duplicate(self, n, x, y, z):

        temp = []
        for j in self._duplicate:
            for i in range(1, n + 1):
                mol = j.get_replica(j.label)
                mol.move(i * x, i * y, i * z)
                temp.append(mol)

        self._duplicate.extend(temp)

        return self


class lmpMolecule(Molecule):
    def __init__(self, molId):
        super().__init__('lmpMolecule')


class pdbMolecule(Molecule):
    def __init__(self, molId):
        super().__init__('pdbMolecule')
