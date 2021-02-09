# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-06
# version: 0.0.1

from emmm.core.atom import Atom
from emmm.core.molecule import Molecule
import numpy as np


class Mapper:

    def __init__(self, world) -> None:
        self.world = world

        # type to atom typeID
        self.typeID = dict()
        self.typeIDCounter = 1

        # atom types to bondID
        self.bondID = np.zeros((16, 16))
        self.bondIDCounter = 1
        # bondID to bond potential
        self.bondID2bp = dict()

        # atom type to angle ID
        self.angleID = np.zeros((16, 16, 16))
        self.angleIDCounter = 1
        # angleID to angle potential
        self.angleID2ap = dict()

        # atom type to pair ID
        self.pairID = np.zeros((16, 16))
        self.pairIDCounter = 1

        self.pairID2pp = dict()

        # atom type to dihedral ID
        self.dihedralID = np.zeros((16, 16, 16, 16))
        self.dihedralIDCounter = 1
        # dihedralID to dihedral potential
        self.dihedralID2dp = dict()

        # atom type to improper ID
        self.improperID = np.zeros((16, 16, 16, 16))
        self.improperIDCounter = 1
        # improperID to improper potential
        self.improperID2ip = dict()

    def set_types(self, items):
        for item in items:
            if isinstance(item, Molecule):
                self.set_types(item)
            elif isinstance(item, Atom):
                self.set_type(item)

    def set_type(self, atom):

        # if there is no type in the map
        if not self.typeID.get(atom.type, None):

            self.typeID[atom.type] = self.typeIDCounter

        setattr(atom, 'typeID', self.typeIDCounter)
        self.typeIDCounter += 1

        return self.typeID[atom.type]

    def get_typeID(self, typeName):

        return self.typeID[typeName]

    def set_bond(self, typeName1, typeName2, bp):

        # two typeID can allocate a bondID in 2D matrix (t2bondID)
        # then the bondID: bp

        typeID1 = self.get_typeID(typeName1)
        typeID2 = self.get_typeID(typeName2)

        bondID0 = self.bondID[typeID1][typeID2]
        bondID1 = self.bondID[typeID2][typeID1]
        if bondID0 != bondID1:
            raise ValueError('big problem, bondID matrix is asymmetry')

        elif not (bondID1 and bondID0):  # if not map:
            # atom typeID to bondID
            self.bondID[typeID1][typeID2] = self.bondIDCounter
            self.bondID[typeID2][typeID1] = self.bondIDCounter
            # bondID to bondpotential
            self.bondID2bp[self.bondIDCounter] = bp
            # set bondPotential a bondID attribute
            setattr(bp, 'bondID', self.bondIDCounter)
            self.bondIDCounter += 1
            return self.bondIDCounter - 1

        else:
            # already map
            return self.bondID[typeID1][typeID2]

    def get_bondID(self, typeName1, typeName2):
        tid1 = self.get_typeID(typeName1)
        tid2 = self.get_typeID(typeName2)

        return self.bondID[tid1][tid2]

    def get_bondP(self, typeName1, typeName2):
        bondID = self.get_bondID(typeName1, typeName2)
        return self.bondID2bp[bondID]

    def set_angle(self, typeName1, typeName2, typeName3, ap):

        typeID1 = self.get_typeID(typeName1)
        typeID2 = self.get_typeID(typeName2)
        typeID3 = self.get_typeID(typeName3)

        aid0 = self.angleID[typeID1][typeID2][typeID3]
        aid1 = self.angleID[typeID2][typeID3][typeID1]
        aid2 = self.angleID[typeID3][typeID1][typeID2]

        if not (aid0 and aid1 and aid2):
            self.angleID[typeID1][typeID2][typeID3] = self.angleIDCounter
            self.angleID[typeID3][typeID2][typeID2] = self.angleIDCounter

            self.angleID2ap[self.angleIDCounter] = ap

            setattr(ap, 'angleID', self.angleIDCounter)
            self.angleIDCounter += 1
            return self.angleIDCounter - 1

        else:
            return self.angleID[typeID1][typeID2][typeID3]

    def get_angleID(self, typeName1, typeName2, typeName3):
        tid1 = self.get_typeID(typeName1)
        tid2 = self.get_typeID(typeName2)
        tid3 = self.get_typeID(typeName3)
        return self.angleID[tid1][tid2][tid3]

    def get_angleP(self, typeName1, typeName2, typeName3):
        angleID = self.get_angleID(typeName1, typeName2, typeName3)
        return self.angleP[angleID]

    def set_pair(self, typeName1, typeName2, pp):
        typeID1 = self.get_typeID(typeName1)
        typeID2 = self.get_typeID(typeName2)

        pid0 = self.pairID[typeID1][typeID2]
        pid1 = self.pairID[typeID2][typeID1]

        if not (pid0 and pid1):
            self.pairID[typeID1][typeID2] = self.pairIDCounter
            self.pairID[typeID2][typeID1] = self.pairIDCounter

            self.pairID2pp[self.angleIDCounter] = pp

            setattr(pp, 'pairID', self.pairIDCounter)
            self.pairIDCounter += 1
            return self.pairIDCounter - 1
        else:
            return self.pairID[typeID1][typeID2]

    def get_pairID(self, typeName1, typeName2):
        tid0 = self.get_typeID(typeName1)
        tid1 = self.get_typeID(typeName2)
        return self.pairID[tid1][tid0]

    def get_pairP(self, typeName1, typeName2):
        pairID = self.get_pairID(typeName1, typeName2)
        return self.pairID2pp[pairID]

    def set_dihedral(self, typeName1, typeName2, typeName3, typeName4, dp):
        typeID1 = self.get_typeID(typeName1)
        typeID2 = self.get_typeID(typeName2)
        typeID3 = self.get_typeID(typeName3)
        typeID4 = self.get_typeID(typeName4)

        self.dihedralID[typeID1][typeID2][typeID3][typeID4] = self.dihedralIDCounter
        self.dihedralID[typeID4][typeID3][typeID2][typeID1] = self.dihedralIDCounter

        self.dihedralID2dp[self.dihedralIDCounter] = dp
        setattr(dp, 'dihedralID', self.dihedralIDCounter)
        self.dihedralIDCounter += 1
        return self.dihedralIDCounter - 1

    def get_dihedralID(self, typeName1, typeName2, typeName3, typeName4):
        return self.dihedralID[self.get_typeID[typeName1]][self.get_typeID[typeName2]][self.get_typeID[typeName3]][self.get_typeID[typeName4]]

    def get_dihedralP(self, typeName1, typeName2, typeName3, typeName4):
        return self.dihedralID2dp[self.get_dihedralID(typeName1, typeName2, typeName3, typeName4)]

    def set_improper(self, typeName1, typeName2, typeName3, typeName4, ip):
        typeID1 = self.get_typeID(typeName1)
        typeID2 = self.get_typeID(typeName2)
        typeID3 = self.get_typeID(typeName3)
        typeID4 = self.get_typeID(typeName4)

        self.improperID[typeID1][typeID2][typeID3][typeID4] = self.improperIDCounter
        self.improperID[typeID1][typeID2][typeID4][typeID3] = self.improperIDCounter
        self.improperID[typeID1][typeID3][typeID2][typeID4] = self.improperIDCounter
        self.improperID[typeID1][typeID3][typeID4][typeID2] = self.improperIDCounter
        self.improperID[typeID1][typeID4][typeID2][typeID3] = self.improperIDCounter
        self.improperID[typeID1][typeID4][typeID3][typeID2] = self.improperIDCounter

        self.improperID2ip[self.improperIDCounter] = ip
        setattr(ip, 'improperID', self.improperIDCounter)
        self.improperIDCounter += 1
        return self.improperIDCounter - 1

    def get_improperID(self, typeName1, typeName2, typeName3, typeName4):
        return self.improperID[self.get_typeID[typeName1]][self.get_typeID[typeName2]][self.get_typeID[typeName3]][self.get_typeID[typeName4]]

    def get_improperP(self, typeName1, typeName2, typeName3, typeName4):
        return self.improperID2ip[self.get_improperID(typeName1, typeName2, typeName3, typeName4)]
