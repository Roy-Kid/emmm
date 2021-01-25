# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1


from emmm.plugins.output.output_base import OutputBase


class OUTlmpdat(OutputBase):
    def __init__(self, world) -> None:
        super().__init__(world)

    def write_data(self, fname, atomStyle='full'):

        self.atomStyle = atomStyle

        self.file = open(fname, 'w')
        global w
        w = self.file.write

        # states = ['atoms', 'bonds', 'angles', 'dihedrals', 'impropers',
        #          'atom types', 'bond types', 'angle types', 'dihedral types',
        #          'improper types', 'xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi',
        #          'Masses', 'pair_coeffs', 'bond_coeffs', 'angle_coeffs',
        #          'dihedral_coeffs', 'improper_coeffs', 'Atoms', 'Bonds',
        #          'Angles', 'Dihedrals', 'Impropers']
        executeWhen = {
            'commet': self.commet,
            'atoms': self.atoms,
            'bonds': self.bonds,
            'angles': self.angles,
            'dihedrals': self.dihedrals,
            'impropers': self.impropers,
            'atom types': self.atom_types,
            'bond types': self.bond_types,
            'angle types': self.angle_types,
            'dihedral types': self.dihedral_types,
            'improper types': self.improper_types,
            'boundary': self.boundary,
            'Masses': self.masses,
            'pair_coeffs': self.pair_coeffs,
            'bond_coeffs': self.bond_coeffs,
            'angle_coeffs': self.angle_coeffs,
            'dihedral_coeffs': self.dihedral_coeffs,
            'improper_coeffs': self.improper_coeffs,
            'Atoms': self.Atoms,
            'Bonds': self.Bonds,
            'Angles': self.Angles,
            'Dihedrals': self.Dihedrals,
            'Impropers': self.Impropers}

        for state, execute in executeWhen.items():
            execute()

        self.file.close()

    def commet(self):
        w(f'LAMMPS data from {self.world.title} Created by \n\n')

    def atoms(self):
        w(f'\t  {self.world.atomCount}  atoms\n')

    def bonds(self):
        w(f'\t  {self.world.bondCount}  bonds\n')

    def angles(self):
        w(f'\t  {self.world.angleCount}  angles\n')

    def dihedrals(self):
        w(f'\t  {self.world.dihedralCount}  dihedrals\n\n')

    def impropers(self):
        w(f'\t  {self.world.improperCount}  dihedrals\n\n')

    def atom_types(self):
        w(f'\t  {self.world.atomTypeCount}  atom types\n')

    def bond_types(self):
        w(f'\t  {self.world.bondTypeCount}  bond types\n')

    def angle_types(self):
        w(f'\t  {self.world.angleTypeCount}  angle types\n')

    def dihedral_types(self):
        w(f'\t  {self.world.dihedralTypeCount}  dihedral types\n')

    def improper_types(self):
        w(f'\t  {self.world.improperTypeCount}  improper types\n\n')

    def boundary(self):
        w(f'\t  {self.world.xlo}\t{self.world.xhi}\txlo\txhi\n')
        w(f'\t  {self.world.ylo}\t{self.world.yhi}\tylo\tyhi\n')
        w(f'\t  {self.world.zlo}\t{self.world.zhi}\tzlo\tzhi\n\n')

    def masses(self):
        w(f'Masses\n\n')
        for id, mass in self.world.masses.items():
            w(f'\t{id}\t{mass}\n')

        w('\n')

    def pair_coeffs(self):
        w(f'Pair Coeffs\n\n')
        for id, pp in self.world.forcefield.pairPotential.items():
            w(f'\t{id}\t{pp.lmpformat.join("  ")}\n')
        w('\n')

    def bond_coeffs(self):
        w(f'Bond Coeffs\n\n')
        for id, bp in self.wold.forcefield.bondPotential.items():
            w(f'\t{id}\t{bp.lmpformat.join("  ")}\n')
        w('\n')

    def angle_coeffs(self):
        w(f'Angle Coeffs\n\n')
        for id, ap in self.world.forcefield.anglePotential.items():
            w(f'\t{id}\t{ap.lmpformat.join("  ")}\n')
        w('\n')

    def dihedral_coeffs(self):
        w(f'Dihedral Coeffs\n\n')
        for id, dp in self.world.forcefield.dihedralPotential.items():
            w(f'\t{id}\t{dp.lmpformat.join("  ")}\n')
        w('\n')

    def improper_coeffs(self):
        w(f'Improper Coeffs\n\n')
        for id, ip in self.world.forcefield.improperPotential.items():
            w(f'\t{id}\t{ip.lmpformat.join("  ")}\n')
        w('\n')

    def Atoms(self):
        w(f'Atoms\n\n')

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
                w(f'\t{id}\t{molid}\t{atomTypeId}\t{atom.q}\t{atom.x}\t{atom.y}\t{atom.z}\n')

            elif self.atomStyle == 'molecular':
                w(f'\t{id}\t{molid}\t{atomTypeId}\t{atom.x}\t{atom.y}\t{atom.z}\n')

        w('\n')

    def Bonds(self):
        w(f'Bonds\n\n')

        self.bondTypeMap = list()

        for id, bond in enumerate(self.world.topo.topoBonds):

            bondType = [self.atomTypeMap.index(
                bond[0].type), self.atomTypeMap.index(bond[0].type)]
            sorted(bondType)
            if bondType not in self.bondTypeMap:
                self.bondTypeMap.append(bondType)
            type = self.bondTypeMap.index(bondType)

            w(f'\t{id}\t{type}\t{self.atomIdMap[bond[0].id]}\t{self.atomIdMap[bond[1].id]}\n')

        w(f'\n')

    def Angles(self):
        w(f'Angles\n\n')

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

            w(f'\t{id}\t{type}\t{self.atomIdMap[angle[0].id]}\t{self.atomIdMap[angle[1].id]}\t{self.atomIdMap[angle[2].id]}\n')

        w(f'\n')

    def Dihedrals(self):
        w(f'Dihedrals\n\n')

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

            w(f'\t{id}\t{type}\t{self.atomIdMap[dihedral[0].id]}\t{self.atomIdMap[dihedral[1].id]}\t{self.atomIdMap[dihedral[2].id]}\t{self.atomIdMap[dihedral[3].id]}')
        w(f'\n')

    def Impropers(self):
        w(f'Impropers\n\n')

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

            w(f'\t{id}\t{type}\t{self.atomIdMap[improper[0].id]}\t{self.atomIdMap[improper[1].id]}\t{self.atomIdMap[improper[2].id]}\t{self.atomIdMap[improper[3].id]}')
        w(f'\n')
