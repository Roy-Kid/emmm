from .dstru import ndarray
class ForceField:

    def __init__(self, world):
        
        self.world = world

        self.typeMap = list() # =ndarray(256)
        self.bondMap = ndarray((256, 256))

        self.bondCoeffMap = dict()

        # type->typeMap->typeId->bondId->bondCoeffMap

    def _type_map(self, *types):
        for type in types:
            if type not in self.typeMap:
                self.typeMap.append(type)

    def get_typeId(self, type):

        return self.typeMap.index(type)

    def _bond_map(self, style, coeffs):
        bondId = len(self.bondCoeffMap)
        self.bondCoeffMap[bondId] = {'style':style, 'coeffs':coeffs}
        return bondId

    def set_bond_coeffs(self, style, type1, type2, *coeffs):

        self._type_map(type1, type2)

        typeId1 = self.get_typeId(type1)
        typeId2 = self.get_typeId(type2)

        bondId = self._bond_map(style, coeffs)

        self.bondMap.symetry_assign(bondId, typeId1, typeId2)

    def get_bond_coeffs(self, type1, type2):
        typeId1 = self.get_typeId(type1)
        typeId2 = self.get_typeId(type2)
        
        bondId = self.bondMap[typeId1][typeId2]
        print(self.bondCoeffMap[bondId])

        return self.bondCoeffMap[bondId]

    def match_ff(self, types):
        return True