# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-31
# version: 0.0.1

from mollab.core.forcefield import ForceField
from mollab.core.item import Item
from mollab.core.topo import Topo


class World(Item):
    def __init__(self):

        super().__init__('World')

        self.forcefield = ForceField(self)

        self.topo = Topo(self)

    def add_items(self, items):
        for item in items:
            item.parent = self.label
        self.container.extend(items)

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

    @property
    def atoms(self):
        return self.flatten()

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

    def set_pair(self,
                 style,
                 typeName1,
                 typeName2,
                 *coeffs,
                 id=None,
                 type=None):

        self.forcefield.set_pair(style, typeName1, typeName2, coeffs,
                                      id, type)

    def set_bond(self,
                 style,
                 typeName1,
                 typeName2,
                 *coeff,
                 id=None,
                 type=None):

        self.forcefield.set_bond(style, typeName1, typeName2, coeff,
                                      id, type)

    def set_angle(self,
                  style,
                  typeName1,
                  typeName2,
                  typeName3,
                  *coeffs,
                  id=None,
                  type=None):

        ap = self.forcefield.set_angle(style, typeName1, typeName2, typeName3,
                                       coeffs, id, type)

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
                                          typeName3, typeName4, coeffs,
                                          id, type)

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
                                          typeName3, typeName4, coeffs,
                                          id, type)
