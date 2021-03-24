# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-25
# version: 0.0.2

from mollab.core.mapper import Mapper
from mollab.core.item import Item
import numpy as np
from mollab.i18n.i18n import _
from mollab.core.topo import Topo
from tqdm import tqdm


class Molecule(Item):
    def __init__(self, loadAtom=None, **kwarg):

        super().__init__('Molecule')

        self.register_properties(style=kwarg.get('style', 'Molecule'),
                                mass=0,
                                type='',
                                parent='',
                                label=kwarg.get('label', ''),
                                root='')
        self.atomTypeMapper = Mapper('atomTypeMapper')
        self.bondTypeMapper = Mapper('bondTypeMapper')
        self.angleTypeMapper = Mapper('angleTypeMapper')
        self.dihedralTypeMapper = Mapper('dihedralTypeMapper')
        self.improperTypeMapper = Mapper('improperTypeMapper')
        self.pairTypeMapper = Mapper('pairTypeMapper')

        self._duplicate = [self]
        self.topo = Topo()

    def __str__(self) -> str:
        return f'< Molecule {self.label} >'

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

    @property
    def bonds(self):
        return self.topo.bonds

    @property
    def angles(self):
        return self.topo.angles

    @property
    def dihedrals(self):
        return self.topo.dihedrals

    @property
    def impropers(self):
        return self.topo.impropers

    @property
    def atomCount(self):
        ac = getattr(self, '_atomCount', None)
        if not ac:
            self._atomCount = len(self.atoms)
        return self._atomCount

    @property
    def bondCount(self):
        bc = getattr(self, '_bondCount', None)
        if not bc:
            self._bondCount = len(self.bonds)
        return self._bondCount

    @property
    def angleCount(self):
        ac = getattr(self, '_angleCount', None)
        if not ac:
            self._angleCount = len(self.angles)
        return self._angleCount

    @property
    def dihedralCount(self):
        dc = getattr(self, '_dihedralCount', None)
        if not dc:
            self._dihedralCount = len(self.dihedrals)
        return self._dihedralCount

    @property
    def improperCount(self):
        ic = getattr(self, '_improperCount', None)
        if not ic:
            self._improperCount = len(self.impropers)
        return self._improperCount

    @property
    def atomTypeCount(self):
        return len(self.atomTypeMapper)

    @property
    def bondTypeCount(self):
        return len(self.bondTypeMapper)

    @property
    def angleTypeCount(self):
        return len(self.angleTypeMapper)
    
    @property
    def dihedralTypeCount(self):
        return len(self.dihedralTypeMapper)

    @property
    def improperTypeCount(self):
        return len(self.improperTypeMapper)

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
                dir.append(str(item.label))
                item.path = '/'.join(dir)
                atoms.append(item)
                dir.pop()

            elif item.itemType == 'Molecule':

                atoms.extend(item.flatten(dir))

                if isMol:
                    atoms.append(item)

        dir.pop()
        return atoms

    def adopt(self, topo, mappers, forcefield, remap=False):
        for atom in self.atoms:
            self.atomTypeMapper.update({atom.type: mappers[0][atom.type]})

        if mappers[1]:
            for bond in topo.bonds:
                if atom in bond and bond not in self.topo.bonds:
                    self.topo.bonds.append(bond)
                    self.bondTypeMapper.update({bond.type: mappers[1].retrieve(bond.type)})

            for angle in topo.angles:
                if atom in angle and angle not in self.topo.angles:

                    self.topo.angles.append(angle)
                    self.angleTypeMapper.update({angle.type: mappers[2].retrieve(angle.type)})

            for dihedral in topo.dihedrals:
                if atom in dihedral and dihedral not in self.topo.dihedrals:

                    self.topo.dihedrals.append(dihedral)
                    self.dihedralTypeMapper.update({dihedral.type: mappers[3].retrieve(dihedral.type)})

            for improper in topo.impropers:
                if atom in improper and improper not in self.topo.impropers:
                    self.topo.impropers.append(improper)
                    self.improperTypeMapper.update({improper.type: mappers[4].retrieve(improper.type)})

        # TODO: extract to a boardCast method
        for item in self.container:
            if item.itemType == 'Molecule':
                item.adopt(topo, forcefield)

        if remap:
            self.atomIdMapper = Mapper('atomIdMapper')
            for atom in self.atoms:
                self.atomIdMapper.map(atom.atomId)
                atom.atomId = self.atomIdMapper.retrieve(atom.atomId)

    def calc_centroid(self, mode='zhixin'):
        """计算Molecule的质心
        """
        atoms = self.flatten()
        masses = list()
        vecs = list()
        for atom in atoms:

            if mode == 'zhixin':
                masses.append(atom.mass)
            vecs.append(atom.position)

        vec = np.array(vecs)
        if mode == 'zhixin':
            masses = np.array(masses)
            return (masses@vec) / masses.sum()
        else:
            return vec.sum(axis=0)

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
            self._position = self.calc_centroid()
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
