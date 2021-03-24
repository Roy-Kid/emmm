# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-31
# version: 0.0.1

from mollab.core.molecule import Molecule
from mollab.core.atom import Atom, fullAtom
from mollab.core.mapper import Mapper
from mollab.core.forcefield import ForceField
from mollab.core.item import Item
from mollab.core.topo import Topo


class World(Item):
    def __init__(self, label=None):

        super().__init__('World')

        self.forcefield = ForceField(self)

        self.topo = Topo()
        self.register_properties(label=label, root='World', comment='world '+label)
        self.atomTypeMapper = Mapper('atomTypeMapper')
        self.bondTypeMapper = Mapper('bondTypeMapper')
        self.angleTypeMapper = Mapper('angleTypeMapper')
        self.dihedralTypeMapper = Mapper('dihedralTypeMapper')
        self.improperTypeMapper = Mapper('improperTypeMapper')
        self.pairTypeMapper = Mapper('pairTypeMapper')
        self.massMapper = {}

    def add_items(self, *items, isUpdate=True):

        for item in items:
            item.parent = self.label
            if item.itemType == 'Atom':
                raise TypeError('暂不支持Atom直接添加到World中, 请包装成Molecule')
            else:
                for atom in item.flatten():
                    self.atomTypeMapper.map(atom.type)
                    atom.typeId = self.atomTypeMapper.retrieve(atom.type)
                    self.massMapper.update({atom.type: atom.mass})

        self.container.extend(items)
        if isUpdate:
            self.update()

    def update(self, isTopoBond=True, isTopoAngle=True, isTopoDihedral=True, isTopoImproper=True):

        self.atomCount = len(self.flatten())

        self.atomTypeCount = len(self.atomTypeMapper)

        self.topo.search_topo(self, isTopoBond, isTopoAngle, isTopoDihedral, isTopoImproper)
        mappers = [
            self.atomTypeMapper, self.bondTypeMapper, self.angleTypeMapper,
            self.dihedralTypeMapper, self.improperTypeMapper,
            self.dihedralTypeMapper
        ]
        self.boardCast(self.topo, mappers, self.forcefield, remap=True)

        # TODO: remove all the *Count setter
        # generate them automatically
        self.bondCount = len(self.bonds)
        self.angleCount = len(self.angles)
        self.dihedralCount = len(self.dihedrals)
        self.improperCount = len(self.impropers)

        self.bondTypeCount = len(self.bondTypeMapper)

        self.angleTypeCount = len(self.angleTypeMapper)

        self.dihedralTypeCount = len(self.dihedralTypeMapper)

        self.improperTypeCount = len(self.improperTypeMapper)

    def boardCast(self, topo, mappers, forcefield, remap=True):
        for molecule in self.container:
            molecule.adopt(topo, mappers, forcefield, remap)

    def flatten(self, dir=None, isMol=False):
        """将world中储存的item压平, 换言之就是提取出所有的atom

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

    def __getitem__(self, i):
        for item in self.container:
            if item.label == i:
                return item

    @property
    def label(self):
        return self.properties['label']

    @label.setter
    def label(self, l):
        self.properties['label'] = l

    @property
    def root(self):
        return self.properties['root']

    @property
    def comment(self):
        return self.properties['comment']

    @comment.setter
    def comment(self, c):
        self.properties['comment'] = c

    @property
    def atoms(self):
        return self.flatten()

    @property
    def molecules(self):
        return self.container

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
        return self._atomCount

    @atomCount.setter
    def atomCount(self, v):
        self._atomCount = int(v)

    @property
    def bondCount(self):
        return self._bondCount

    @bondCount.setter
    def bondCount(self, v):
        self._bondCount = int(v)

    @property
    def angleCount(self):
        return self._angleCount

    @angleCount.setter
    def angleCount(self, v):
        self._angleCount = int(v)

    @property
    def dihedralCount(self):
        return self._dihedralCount

    @dihedralCount.setter
    def dihedralCount(self, v):
        self._dihedralCount = int(v)

    @property
    def improperCount(self):
        return self._improperCount

    @improperCount.setter
    def improperCount(self, v):
        self._improperCount = int(v)

    @property
    def atomTypeCount(self):
        return self._atomTypeCount

    @atomTypeCount.setter
    def atomTypeCount(self, v):
        self._atomTypeCount = int(v)

    @property
    def bondTypeCount(self):
        return self._bondTypeCount

    @bondTypeCount.setter
    def bondTypeCount(self, v):
        self._bondTypeCount = int(v)

    @property
    def angleTypeCount(self):
        return self._angleTypeCount

    @angleTypeCount.setter
    def angleTypeCount(self, v):
        self._angleTypeCount = int(v)

    @property
    def dihedralTypeCount(self):
        return self._dihedralTypeCount

    @dihedralTypeCount.setter
    def dihedralTypeCount(self, v):
        self._dihedralTypeCount = int(v)

    @property
    def improperTypeCount(self):
        return self._improperTypeCount

    @improperTypeCount.setter
    def improperTypeCount(self, v):
        self._improperTypeCount = int(v)

    @property
    def xlo(self):
        return self._xlo

    @xlo.setter
    def xlo(self, xlo):
        self._xlo = float(xlo)

    @property
    def xhi(self):
        return self._xhi

    @xhi.setter
    def xhi(self, xhi):
        self._xhi = float(xhi)

    @property
    def ylo(self):
        return self._ylo

    @ylo.setter
    def ylo(self, ylo):
        self._ylo = float(ylo)

    @property
    def yhi(self):
        return self._yhi

    @yhi.setter
    def yhi(self, yhi):
        self._yhi = float(yhi)

    @property
    def zlo(self):
        return self._zlo

    @zlo.setter
    def zlo(self, zlo):
        self._zlo = float(zlo)

    @property
    def zhi(self):
        return self._zhi

    @zhi.setter
    def zhi(self, zhi):
        self._zhi = float(zhi)

    def set_pair(
        self,
        style,
        typeName1,
        typeName2,
        *coeffs,
        id=None,
        type=None,
    ):

        pp = self.forcefield.set_pair(style, typeName1, typeName2, coeffs, id,
                                      type)
        self.pairTypeMapper.map(pp.type)
        pp.typeId = self.pairTypeMapper.retrieve(pp.type)

    def set_bond(self, style, typeName1, typeName2, *coeff, type=None, id=None):
        bp = self.forcefield.set_bond(style, typeName1, typeName2, coeff, id,
                                      type)
        self.bondTypeMapper.map(type)
        bp.typeId = self.bondTypeMapper.retrieve(type)
        return bp

    def set_angle(self,
                  style,
                  typeName1,
                  typeName2,
                  typeName3,
                  *coeffs,
                  type=None,
                  id=None):

        ap = self.forcefield.set_angle(style, typeName1, typeName2, typeName3,
                                       coeffs, id, type)
        self.angleTypeMapper.map(type)
        ap.typeId = self.angleTypeMapper.retrieve(type)
        return ap

    def set_dihedral(self,
                     style,
                     typeName1,
                     typeName2,
                     typeName3,
                     typeName4,
                     *coeffs,
                     id=None,
                     type=None):

        dp = self.forcefield.set_dihedral(style, typeName1, typeName2,
                                          typeName3, typeName4, coeffs, id,
                                          type)
        self.dihedralTypeMapper.map(type)
        dp.typeId = self.dihedralTypeMapper.retrieve(type)
        return dp

    def set_improper(self,
                     style,
                     typeName1,
                     typeName2,
                     typeName3,
                     typeName4,
                     *coeffs,
                     id=None,
                     type=None):
        ip = self.forcefield.set_improper(style, typeName1, typeName2,
                                          typeName3, typeName4, coeffs, id,
                                          type)
        self.improperTypeMapper.map(type)
        ip.typeId = self.improperTypeMapper.retrieve(type)
        return ip
