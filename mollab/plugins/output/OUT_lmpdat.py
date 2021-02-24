# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from mollab.plugins.output.output_base import Mapper, OutputBase


class OUTlmpdat(OutputBase):

    def __init__(self, item) -> None:
        super().__init__()
        self.item = item
        self.atomIdMapper = Mapper('atomId')
        for atom in self.item.atoms:
            self.atomIdMapper.add(atom.id)


    def write_data(self, fname, item):

        if not getattr(self, 'item', None):
            raise KeyError('assign a universe/world first')

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
        return f'LAMMPS data from {self.item.comment} Created by \n\n'

    def atomCount(self):
        return f'\t  {self.item.atomCount}  atoms\n'

    def bondCount(self):
        return f'\t  {self.item.bondCount}  bonds\n'

    def angleCount(self):
        return f'\t  {self.item.angleCount}  angles\n'

    def dihedralCount(self):
        return f'\t  {self.item.dihedralCount}  dihedrals\n\n'

    def improperCount(self):
        return f'\t  {self.item.improperCount}  impropers\n\n'

    def atomTypeCount(self):
        return f'\t  {self.item.atomTypeCount}  atom types\n'

    def bondTypeCount(self):
        return f'\t  {self.item.bondTypeCount}  bond types\n'

    def angleTypeCount(self):
        return f'\t  {self.item.angleTypeCount}  angle types\n'

    def dihedralTypeCount(self):
        return f'\t  {self.item.dihedralTypeCount}  dihedral types\n'

    def improperTypeCount(self):
        return f'\t  {self.item.improperTypeCount}  improper types\n\n'

    def boundary(self):
        return [
            f'\t  {self.item.xlo}\t{self.item.xhi}\txlo\txhi\n',
            f'\t  {self.item.ylo}\t{self.item.yhi}\tylo\tyhi\n',
            f'\t  {self.item.zlo}\t{self.item.zhi}\tzlo\tzhi\n\n'
        ]

    def masses(self):


        lines = list()
        lines.append('Masses\n\n')

        for atom in self.item.atoms:

            lines.append(f'\t{self.atomIdMapper.retrieve(atom.id)}\t{atom.mass}\n')

        return lines

    def pair_coeffs(self):
        lines = list()
        lines.append('Pair Coeffs\n\n')
        for pp in self.item.forcefield.pairPotentialList:
            coeffs = [pp.type, *pp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            pc = '\t'.join(coeffs)
            lines.append(f'\t\t{ pc }\n')

        return lines

    def bond_coeffs(self):
        lines = list()
        lines.append('Bond Coeffs\n\n')
        for bp in self.item.forcefield.bondPotentialList:

            coeffs = [bp.type, *bp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            bc = '\t'.join(coeffs)
            lines.append(f'\t\t{bc}\n')

        return lines

    def angle_coeffs(self):
        lines = list()
        lines.append('Angle Coeffs\n\n')
        for ap in self.item.forcefield.anglePotentialList:
            coeffs = [ap.type, *ap.lmp_format]
            coeffs = [str(i) for i in coeffs]
            ac = '\t'.join(coeffs)
            lines.append(f'\t\t{ac}\n')

        return lines

    def dihedral_coeffs(self):
        lines = list()
        lines.append('Dihedral Coeffs\n\n')
        for dp in self.item.forcefield.dihedralPotentialList:
            coeffs = [dp.type, *dp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            dc = '\t'.join(coeffs)
            lines.append(f'\t\t{dc}\n')

        return lines

    def improper_coeffs(self):
        lines = list()
        lines.append('Improper Coeffs\n\n')

        for ip in self.item.forcefield.improperPotentialList:
            coeffs = [ip.type, *ip.lmp_format]
            coeffs = [str(i) for i in coeffs]
            ip = '\t'.join(coeffs)
            lines.append(f'\t\t{ip}\n')

        return lines

    def Atoms(self):
        lines = list()
        lines.append('Atoms\n\n')

        for atom in self.item.atoms:
            lines.append(
                f'\t{self.atomIdMapper.retrieve(atom.id)}\t{atom.molId}\t{atom.type}\t{atom.q}\t{atom.x}\t{atom.y}\t{atom.z}\n'
            )

        lines.append('\n')
        return lines

    def Bonds(self):
        lines = list()
        lines.append(f'Bonds\n\n')

        for id, bond in enumerate(self.item.topo.bonds, 1):

            lines.append(
                f'\t{id}\t{bond.type}\t{self.atomIdMapper.retrieve(bond.atom1.id)}\t{self.atomIdMapper.retrieve(bond.atom2.id)}\n'
            )

        lines.append(f'\n')
        return lines

    def Angles(self):
        lines = list()
        lines.append(f'Angles\n\n')

        self.angleTypeMap = list()

        for id, angle in enumerate(self.item.topo.topoAngles, 1):

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
        return lines

    def Dihedrals(self):
        lines = list()
        lines.append(f'Dihedrals\n\n')

        self.dihedralTypeMap = list()

        for id, dihedral in enumerate(self.item.topo.topoDihedrals, 1):
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
        return lines

    def Impropers(self):
        lines = list()
        lines.append(f'Impropers\n\n')

        self.ImproperTypeMap = list()

        for id, improper in enumerate(self.item.topo.topoImpropers, 1):
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
        return lines
