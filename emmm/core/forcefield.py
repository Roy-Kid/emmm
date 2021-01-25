# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-24
# version: 0.0.1 

from emmm.core.potential import bond_potential_interface
from .dstru import ndarray
class ForceField:

    def __init__(self, world):
        
        self.world = world

        self.typeMap = list() # =ndarray(256)

        self.bondMap = ndarray((16, 16))
        self.angleMap = ndarray((16,16,16))
        self.dihedralMap = ndarray((16,16,16,16))

        self.bondCoeffMap = list()
        self.angleCoeffMap = list()
        self.dihedralCoeffMap = list()

        # type->typeMap->typeId->bondId->bondCoeffMap

    def set_typeId(self, *types):
        typeId = list()
        for type in types:
            if type not in self.typeMap:
               self.typeMap.append(type)
               typeId.append(len(self.typeMap))
        return typeId
        

    def get_typeId(self, type):

        for i, t in enumerate(self.typeMap):
            if t == type:
                return i
        
        return None

    def set_styleId(self, styleCoeffMap, style, coeffs):
        styleId = len(styleCoeffMap)
        # TODO: replace here to an instance of bondPotential
        styleCoeffMap.append({'style':style, 'coeffs':coeffs})
        return styleId

    def get_styleId(self, styleId, styleMap):

        return styleMap[styleId]

    def set_bond_coeffs(self, style, type1, type2, *coeffs):
        """增加键参数. 

        Args:
            style (str): 键的类型
            type1 (str): atom1的类型
            type2 (str): atom2的类型
        """
        # 首先: 将atom type 映射到 typeId
        typeId1, typeId2 = self.set_typeId(type1, type2)


        # 其次: 将bond type 映射到 bondId
        bp = bond_potential_interface(style, coeffs)

        # 最后: 2darray中, 两个typeId对应两个坐标, 交点是bondId
        # 任给两个atom, 根据其type可以找到bondId, 
        # 使用这个bondId可以在bond_map中找到对应的键信息
        self.bondMap.assign(bp, typeId1, typeId2)
        self.bondMap.assign(bp, typeId2, typeId1)

    def get_bond_coeff(self, type1, type2):

        typeIds = [typeId1, typeId2] = [self.get_typeId(type1), self.get_typeId(type2)]

        if all(typeIds):

            bondId = self.bondMap[typeId1][typeId2]

            return self.bondCoeffMap[bondId]

        else:
            return None

    def set_angle_coeff(self, style, type1, type2, type3, *coeffs):

        typeId1, typeId2, typeId3 = self.set_typeId(type1, type2, type3)

        angleId = self.set_styleId(self.angleCoeffMap, style, coeffs)

        # angle 1-2-3 == angle 3-2-1
        self.angleMap.assign(angleId, typeId1, typeId2, typeId3)
        self.angleMap.assign(angleId, typeId3, typeId2, typeId1)


    def get_angle_coeff(self, type1, type2, type3):

        typeId1 = self.get_typeId(type1)
        typeId2 = self.get_typeId(type2)
        typeId3 = self.get_typeId(type3)

        if typeId1 and typeId2 and typeId3:
            angleId = self.angleMap[typeId1][typeId2][typeId3]
            return self.angleCoeffMap[angleId]
        else:
            return None

    def set_dihedral_coeff(self, style, type1, type2, type3, type4, *coeff):

        typeId1, typeId2, typeId3, typeId4 = self.set_typeId(type1, type2, type3, type4)

        dihedralId = self.set_styleId(self.angleCoeffMap, style, coeff)

        # dihedral 1-2-3-4 == 4-3-2-1
        self.dihedralMap.assign(dihedralId, typeId1, typeId2, typeId3, typeId4)
        self.dihedralMap.assign(dihedralId, typeId4, typeId3, typeId2, typeId1)

    def get_dihedral_coeff(self, type1, type2, type3, type4):

        typeId1 = self.get_typeId(type1)
        typeId2 = self.get_typeId(type2)
        typeId3 = self.get_typeId(type3)
        typeId4 = self.get_typeId(type4)

        if typeId1 and typeId2 and typeId3 and typeId4:
            dihedralId = self.dihedralMap[type1][type2][type3][type4]
            return self.dihedralCoeffMap[dihedralId]
        else:
            return None
