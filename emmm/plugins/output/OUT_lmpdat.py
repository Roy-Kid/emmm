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
        self.atoms()
        self.bonds()
        self.angles()
        self.dihedrals()
        self.impropers()
        self.atom_types()
        self.bond_types()
        self.angle_types()
        self.dihedral_types()
        self.improper_types()
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

    def atoms(self):
        return f'\t  {self.world.atomCount}  atoms\n'

    def bonds(self):
        return f'\t  {self.world.bondCount}  bonds\n'

    def angles(self):
        return f'\t  {self.world.angleCount}  angles\n'

    def dihedrals(self):
        return f'\t  {self.world.dihedralCount}  dihedrals\n\n'

    def impropers(self):
        return f'\t  {self.world.improperCount}  dihedrals\n\n'

    def atom_types(self):
        return f'\t  {self.world.atomTypeCount}  atom types\n'

    def bond_types(self):
        return f'\t  {self.world.bondTypeCount}  bond types\n'

    def angle_types(self):
        return f'\t  {self.world.angleTypeCount}  angle types\n'

    def dihedral_types(self):
        return f'\t  {self.world.dihedralTypeCount}  dihedral types\n'

    def improper_types(self):
        return f'\t  {self.world.improperTypeCount}  improper types\n\n'

    def boundary(self):
        return [f'\t  {self.world.xlo}\t{self.world.xhi}\txlo\txhi\n',
                f'\t  {self.world.ylo}\t{self.world.yhi}\tylo\tyhi\n',
                f'\t  {self.world.zlo}\t{self.world.zhi}\tzlo\tzhi\n\n']

    def masses(self):
        lines = list()
        lines.append(f'Masses\n\n')
        for id, mass in self.world.masses.items():
            lines.append(f'\t{id}\t{mass}\n')

        lines.append('\n')

    def pair_coeffs(self):
        lines = list()
        lines.append(f'Pair Coeffs\n\n')
        for id, pp in self.world.forcefield.pairPotential.items():
            lines.append(f'\t{id}\t{pp.lmpformat.join("  ")}\n')
        lines.append('\n')

    def bond_coeffs(self):
        lines = list()
        lines.append(f'Bond Coeffs\n\n')
        for id, bp in self.wold.forcefield.bondPotential.items():
            lines.append(f'\t{id}\t{bp.lmpformat.join("  ")}\n')
        lines.append('\n')

    def angle_coeffs(self):
        lines = list()
        lines.append(f'Angle Coeffs\n\n')
        for id, ap in self.world.forcefield.anglePotential.items():
            lines.append(f'\t{id}\t{ap.lmpformat.join("  ")}\n')
        lines.append('\n')

    def dihedral_coeffs(self):
        lines = list()
        lines.append(f'Dihedral Coeffs\n\n')
        for id, dp in self.world.forcefield.dihedralPotential.items():
            lines.append(f'\t{id}\t{dp.lmpformat.join("  ")}\n')
        lines.append('\n')

    def improper_coeffs(self):
        lines = list()
        lines.append(f'Improper Coeffs\n\n')
        for id, ip in self.world.forcefield.improperPotential.items():
            lines.append(f'\t{id}\t{ip.lmpformat.join("  ")}\n')
        lines.append('\n')

    def Atoms(self):
        lines = list()
        lines.append(f'Atoms\n\n')

        self.atomIdMap = dict()

        # atom map to index(int)
        # atom - index - id
        self.atomTypeMap = dict()
        atomTypeMapCounter = 0

        for i, atom in enumerate(self.world.atoms):
            # there is no repeart atom id
            self.atomIdMap[atom.id] = i

            # but yes, repear atom type
            atomTypeId = self.atomTypeMap.setdefault(
                atom.type, atomTypeMapCounter)
            atomTypeMapCounter += 1
            # if atom.type not in self.atomTypeMap:
            #     self.atomTypeMap[atom.type] = atomTypeMapCounter
            #     atomTypeId = atomTypeMapCounter
            #     atomTypeMapCounter += 1
            # else:
            #     atomTypeId = self.atomTypeMap[atom.type]

            molid = atom.root

            if self.atomStyle == 'full':
                lines.append(f'\t{id}\t{molid}\t{atomTypeId}\t{atom.q}\t{atom.x}\t{atom.y}\t{atom.z}\n')

            elif self.atomStyle == 'molecular':
                lines.append(f'\t{id}\t{molid}\t{atomTypeId}\t{atom.x}\t{atom.y}\t{atom.z}\n')

        lines.append('\n')

    def Bonds(self):
        lines = list()
        lines.append(f'Bonds\n\n')

        self.bondTypeMap = list()

        for id, bond in enumerate(self.world.topo.topoBonds):

            bondType = [self.atomTypeMap.index(
                bond[0].type), self.atomTypeMap.index(bond[0].type)]
            sorted(bondType)
            if bondType not in self.bondTypeMap:
                self.bondTypeMap.append(bondType)
            type = self.bondTypeMap.index(bondType)

            lines.append(f'\t{id}\t{type}\t{self.atomIdMap[bond[0].id]}\t{self.atomIdMap[bond[1].id]}\n')

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

            lines.append(f'\t{id}\t{type}\t{self.atomIdMap[angle[0].id]}\t{self.atomIdMap[angle[1].id]}\t{self.atomIdMap[angle[2].id]}\n')

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

            lines.append(f'\t{id}\t{type}\t{self.atomIdMap[dihedral[0].id]}\t{self.atomIdMap[dihedral[1].id]}\t{self.atomIdMap[dihedral[2].id]}\t{self.atomIdMap[dihedral[3].id]}')
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

            lines.append(f'\t{id}\t{type}\t{self.atomIdMap[improper[0].id]}\t{self.atomIdMap[improper[1].id]}\t{self.atomIdMap[improper[2].id]}\t{self.atomIdMap[improper[3].id]}')
        lines.append(f'\n')
