# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from emmm.plugins.output.output_base import OutputBase


class OUTlmpdat(OutputBase):
    def write_data(self, fname, atomStyle='full'):

        # check if there is a world to be written
        # TODO: generalize the world to item

        if not getattr(self, 'world', None):
            raise KeyError('assign a world first')

        self.atomStyle = atomStyle

        self.file = open(fname, 'w')

        self.comment()
        self.atomCount()
        self.bondCount()
        self.angleCount()
        self.dihedralCount()
        self.improperCount()
        self.atomTypeCount()
        self.bondTypeCount()
        self.angleTypeCount()
        self.dihedralTypeCount()
        self.improperTypeCount()
        self.boundary()
        self.masses()
        self.pair_coeffs()
        self.bond_coeffs()
        self.angle_coeffs()
        self.dihedral_coeffs()
        self.improper_coeffs()
        self.Atoms()
        self.Bonds()
        self.Angles()
        self.Dihedrals()
        self.Impropers()

        self.file.close()

        self.file.writelines

    def comment(self):
        return f'LAMMPS data from {self.world.comment} Created by \n\n'

    def atomCount(self):
        return f'\t  {self.world.atomCount}  atoms\n'

    def bondCount(self):
        return f'\t  {self.world.bondCount}  bonds\n'

    def angleCount(self):
        return f'\t  {self.world.angleCount}  angles\n'

    def dihedralCount(self):
        return f'\t  {self.world.dihedralCount}  dihedrals\n\n'

    def improperCount(self):
        return f'\t  {self.world.improperCount}  impropers\n\n'

    def atomTypeCount(self):
        return f'\t  {self.world.atomTypeCount}  atom types\n'

    def bondTypeCount(self):
        return f'\t  {self.world.bondTypeCount}  bond types\n'

    def angleTypeCount(self):
        return f'\t  {self.world.angleTypeCount}  angle types\n'

    def dihedralTypeCount(self):
        return f'\t  {self.world.dihedralTypeCount}  dihedral types\n'

    def improperTypeCount(self):
        return f'\t  {self.world.improperTypeCount}  improper types\n\n'

    def boundary(self):
        return [
            f'\t  {self.world.xlo}\t{self.world.xhi}\txlo\txhi\n',
            f'\t  {self.world.ylo}\t{self.world.yhi}\tylo\tyhi\n',
            f'\t  {self.world.zlo}\t{self.world.zhi}\tzlo\tzhi\n\n'
        ]

    def masses(self):
        lines = list()
        lines.append('Masses\n\n')
        for m in self.world.masses:
            lines.append(f'\t{m[0]}\t{m[1]}\n')

        return lines

    def pair_coeffs(self):
        lines = list()
        lines.append('Pair Coeffs\n\n')
        for pp in self.world.pairPotentials:
            coeffs = [pp.pairID, *pp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            pc = '\t'.join(coeffs)
            lines.append(f'\t\t{ pc }\n')

        return lines

    def bond_coeffs(self):
        lines = list()
        lines.append('Bond Coeffs\n\n')
        for bp in self.world.bondPotentials:

            coeffs = [bp.bondID, *bp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            bc = '\t'.join(coeffs)
            lines.append(f'\t\t{bc}\n')

        return lines

    def angle_coeffs(self):
        lines = list()
        lines.append('Angle Coeffs\n\n')
        for ap in self.world.anglePotentials:
            coeffs = [ap.angleID, *ap.lmp_format]
            coeffs = [str(i) for i in coeffs]
            ac = '\t'.join(coeffs)
            lines.append(f'\t\t{ac}\n')

        return lines

    def dihedral_coeffs(self):
        lines = list()
        lines.append('Dihedral Coeffs\n\n')
        for dp in self.world.dihedralPotentials:
            coeffs = [dp.dihedralID, *dp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            dc = '\t'.join(coeffs)
            lines.append(f'\t\t{dc}\n')

        return lines

    def improper_coeffs(self):
        lines = list()
        lines.append('Improper Coeffs\n\n')

        for ip in self.world.improperPotentials:
            coeffs = [ip.improperID, *ip.lmp_format]
            coeffs = [str(i) for i in coeffs]
            ip = '\t'.join(coeffs)
            lines.append(f'\t\t{ip}\n')

        return lines

    def Atoms(self):
        lines = list()
        lines.append('Atoms\n\n')

        self.atomIdMap = dict()

        # atom map to index(int)
        # atom - index - id
        self.atomTypeMap = dict()
        atomTypeMapCounter = 0

        for i, atom in enumerate(self.world.atoms):
            # there is no repeart atom id
            self.atomIdMap[atom.id] = i

            # but yes, repear atom type
            atomTypeId = self.atomTypeMap.setdefault(atom.type,
                                                     atomTypeMapCounter)
            atomTypeMapCounter += 1
            # if atom.type not in self.atomTypeMap:
            #     self.atomTypeMap[atom.type] = atomTypeMapCounter
            #     atomTypeId = atomTypeMapCounter
            #     atomTypeMapCounter += 1
            # else:
            #     atomTypeId = self.atomTypeMap[atom.type]

            molid = atom.root

            if self.atomStyle == 'full':
                lines.append(
                    f'\t{id}\t{molid}\t{atomTypeId}\t{atom.q}\t{atom.x}\t{atom.y}\t{atom.z}\n'
                )

            elif self.atomStyle == 'molecular':
                lines.append(
                    f'\t{id}\t{molid}\t{atomTypeId}\t{atom.x}\t{atom.y}\t{atom.z}\n'
                )

        lines.append('\n')

    def Bonds(self):
        lines = list()
        lines.append(f'Bonds\n\n')

        self.bondTypeMap = list()

        for id, bond in enumerate(self.world.topo.topoBonds):

            bondType = [
                self.atomTypeMap.index(bond[0].type),
                self.atomTypeMap.index(bond[0].type)
            ]
            sorted(bondType)
            if bondType not in self.bondTypeMap:
                self.bondTypeMap.append(bondType)
            type = self.bondTypeMap.index(bondType)

            lines.append(
                f'\t{id}\t{type}\t{self.atomIdMap[bond[0].id]}\t{self.atomIdMap[bond[1].id]}\n'
            )

        lines.append(f'\n')

    def Angles(self):
        lines = list()
        lines.append(f'Angles\n\n')

        self.angleTypeMap = list()

        for id, angle in enumerate(self.world.topo.topoAngles):

            angleType = [
                self.atomTypeMap.index(angle[0].type),
                self.atomTypeMap.index(angle[1].type),
                self.atomTypeMap.index(angle[2].type)
            ]

            sorted(angleType)
            if angleType not in self.angleTypeMap:
                self.angleTypeMap.append(angleType)
            type = self.angleTypeMap.index(angleType)

            lines.append(
                f'\t{id}\t{type}\t{self.atomIdMap[angle[0].id]}\t{self.atomIdMap[angle[1].id]}\t{self.atomIdMap[angle[2].id]}\n'
            )

        lines.append(f'\n')

    def Dihedrals(self):
        lines = list()
        lines.append(f'Dihedrals\n\n')

        self.dihedralTypeMap = list()

        for id, dihedral in enumerate(self.world.topo.topoDihedrals):
            dihedralType = [
                self.atomTypeMap.index(dihedral[0].type),
                self.atomTypeMap.index(dihedral[1].type),
                self.atomTypeMap.index(dihedral[2].type),
                self.atomTypeMap.index(dihedral[3].type),
            ]
            sorted(dihedralType)

            if dihedralType not in self.dihedralTypeMap:
                self.dihedralTypeMap.append(dihedralType)
            type = self.dihedralTypeMap.index(dihedralType)

            lines.append(
                f'\t{id}\t{type}\t{self.atomIdMap[dihedral[0].id]}\t{self.atomIdMap[dihedral[1].id]}\t{self.atomIdMap[dihedral[2].id]}\t{self.atomIdMap[dihedral[3].id]}'
            )
        lines.append(f'\n')

    def Impropers(self):
        lines = list()
        lines.append(f'Impropers\n\n')

        self.ImproperTypeMap = list()

        for id, improper in enumerate(self.world.topo.topoImpropers):
            improperType = [
                self.atomTypeMap.index(improper[0].type),
                self.atomTypeMap.index(improper[1].type),
                self.atomTypeMap.index(improper[2].type),
                self.atomTypeMap.index(improper[3].type),
            ]
            sorted(improperType)

            if improperType not in self.improperTypeMap:
                self.improperTypeMap.append(improperType)
            type = self.improperTypeMap.index(improperType)

            lines.append(
                f'\t{id}\t{type}\t{self.atomIdMap[improper[0].id]}\t{self.atomIdMap[improper[1].id]}\t{self.atomIdMap[improper[2].id]}\t{self.atomIdMap[improper[3].id]}'
            )
        lines.append(f'\n')
