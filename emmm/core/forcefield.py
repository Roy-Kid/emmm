# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-24
# version: 0.0.1

from emmm.core.potential import bond_potential_interface, angle_potential_interface, pair_potential_interface, dihedral_potential_interface, improper_potential_interface


class ForceField:
    def __init__(self, world):

        self.world = world
        self.bondPotentialList = list()
        self.anglePotentialList = list()
        self.dihedralPotentialList = list()
        self.improperPotentialList = list()
        self.pairPotentialList = list()

        self.massList = list()

    def set_bond(self, style, typeName1, typeName2, coeffs):

        bp = bond_potential_interface(style, typeName1, typeName2, coeffs)
        self.bondPotentialList.append(bp)
        return bp

    def get_bond(self, typeName1, typeName2):

        for bp in self.bondPotentialList:
            if bp.compare(typeName1, typeName2):
                return bp

    def set_angle(self, style, typeName1, typeName2, typeName3, coeffs):

        ap = angle_potential_interface(style, typeName1, typeName2, typeName3,
                                       coeffs)
        self.anglePotentialList.append(ap)

        return ap

    def get_angle(self, typeName1, typeName2, typeName3):

        for ap in self.anglePotentialList:
            if ap.compare(typeName1, typeName2, typeName3):
                return ap

    def set_dihedral(self, style, typeName1, typeName2, typeName3, typeName4,
                     coeffs):

        dp = dihedral_potential_interface(style, typeName1, typeName2,
                                          typeName3, typeName4, coeffs)
        self.dihedralPotentialList.append(dp)

        return dp

    def get_dihedral(self, typeName1, typeName2, typeName3, typeName4):

        for dp in self.dihedralPotentialList:
            if dp.compare(typeName1, typeName2, typeName3, typeName4):
                return dp

    def set_improper(self, style, typeName1, typeName2, typeName3, typeName4,
                     coeffs):

        ip = improper_potential_interface(style, typeName1, typeName2,
                                          typeName3, typeName4, coeffs)
        self.improperPotentialList.append(ip)
        return ip

    def get_improper(self, typeName1, typeName2, typeName3, typeName4):

        for ip in self.improperPotentialList:
            if ip.compare(typeName1, typeName2, typeName3, typeName4):
                return ip

    def set_pair(self, style, typeName1, typeName2, coeffs):

        alreadySet = 0
        for pp in self.pairPotentialList:
            if pp.compare(typeName1, typeName2):
                alreadySet = 1
                break
        if not alreadySet:
            pp = pair_potential_interface(style, typeName1, typeName2, coeffs)
            self.pairPotentialList.append(pp)

        return pp

    def get_pair(self, typeName1, typeName2):

        for pp in self.pairPotentialList:
            if pp.compare(typeName1, typeName2):
                return pp

    def set_mass(self, typeName, mass):

        self.massList.append([typeName, mass])

    def get_mass(self, typeName):
        for m in self.massList:
            if m[0] == typeName:
                return m[1]