# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-24
# version: 0.0.2

from mollab.core.molecule import lmpMolecule
from mollab.plugins.input.input_base import InputBase
from mollab.core.atom import fullAtom, molecularAtom
from mollab.core.world import World
from collections import defaultdict


class INlmpdat(InputBase):
    def __init__(self) -> None:
        super().__init__()

    def skipblank(self, line):
        # while line.isspace() or line.strip().startswith('#'):
        while self.isblank(line):
            line = self.readline()
        return line

    def readline(self):
        return self.f.readline()

    def isblank(self, line: str):
        return not bool(line.strip())

    def read(self, fname):

        self.world = World()

        status = 'COMMENT'

        self.f = open(fname, 'r')
        self.world.label = fname
        line = self.readline()
        self.world.comment = line
        line = self.readline()

        while True:
            line = self.readline()
            if not line:
                # read EOF
                break
            line = self.skipblank(line)

            status = self.status_checker(line)
            self.status_executor(status, line)

        self.post_process()

        return self.world

    def status_checker(self, line):
        if 'atoms' in line:
            status = 'atomCount'
        elif 'bonds' in line:
            status = 'bondCount'
        elif 'angles' in line:
            status = 'angleCount'
        elif 'dihedrals' in line:
            status = 'dihedralCount'
        elif 'impropers' in line:
            status = 'improperCount'
        elif 'atom types' in line:
            status = 'atomTypeCount'
        elif 'bond types' in line:
            status = 'bondTypeCount'
        elif 'angle types' in line:
            status = 'angleTypeCount'
        elif 'dihedral types' in line:
            status = 'dihedralTypeCount'
        elif 'improper types' in line:
            status = 'improperTypeCount'
        elif 'xlo' in line:
            status = 'xBoundary'
        elif 'ylo' in line:
            status = 'yBoundary'
        elif 'zlo' in line:
            status = 'zBoundary'
        elif 'Masses' in line:
            status = 'Masses'
        elif 'Pair Coeffs' in line:
            status = 'pairCoeffs'
        elif 'Bond Coeffs' in line:
            status = 'bondCoeffs'
        elif 'Angle Coeffs' in line:
            status = 'angleCoeffs'
        elif 'Dihedral Coeffs' in line:
            status = 'dihedralCoeffs'
        elif 'Improper Coeffs' in line:
            status = 'improperCoeffs'
        elif 'Atoms' in line:
            status = 'Atoms'
        elif 'Bonds' in line:
            status = 'Bonds'
        elif 'Angles' in line:
            status = 'Angles'
        elif 'Dihedrals' in line:
            status = 'Dihedrals'
        elif 'Impropers' in line:
            status = 'Impropers'
        else:
            status = 'ERROR'

        self._status = status
        return status

    def status_executor(self, status, line):

        execute = getattr(self, status, self.status_error)
        execute(line)

    def status_error(self, line):
        raise Exception(f'read error at "{line}"')

    def post_process(self):

        # section 1: add neighbors to atom
        for b in self.bonds:
            cid = b[2]
            pid = b[3]
            catom = None
            patom = None
            for atom in self.atoms:
                if atom.atomId == cid:
                    catom = atom
                if atom.atomId == pid:
                    patom = atom

                # set mass
                for m in self.masses:
                    if m[0] == atom.atomId:
                        atom.mass = m[1]
            if catom is None or patom is None:
                raise ValueError('No atom matches topo')

            catom.add_neighbors(patom)

        # section 2: group atoms to the molecules
        molecules = list()
        grouped_atoms = defaultdict(list)
        for atom in self.atoms:
            ref = getattr(atom, 'molId', 'UNDEFINED')  # sec 2
            grouped_atoms[ref].append(atom)  # sec 2
        for ref, gatom in grouped_atoms.items():
            mol = lmpMolecule(ref)
            mol.add_items(*gatom)
            molecules.append(mol)

        self.world.add_items(*molecules)

        # section 3: set coeffs
        # section 3.1: set pair coeffs

        for pc in self.pairCoeffs:
            if len(pc) == 3:
                self.world.set_pair(self.pairStyle, pc[0], pc[0], *pc[1:], type=pc[0])

        for bc in self.bondCoeffs:
            bondType = bc[0]
            for b in self.bonds:
                if bondType == b[1]:
                    typeName1 = b[2]
                    typeName2 = b[3]
                    self.world.set_bond(self.bondStyle, typeName1, typeName2,
                                        *bc[1:], type=bondType)

        for ac in self.angleCoeffs:
            angleType = ac[0]
            for a in self.angles:
                if angleType == a[1]:
                    typeName1 = a[2]
                    typeName2 = a[3]
                    typeName3 = a[4]
                    self.world.set_angle(self.angleStyle, typeName1, typeName2,
                                         typeName3, *ac[1:], type=angleType)

        for dc in self.dihedralCoeffs:
            dihedralType = dc[0]
            for d in self.dihedrals:
                if dihedralType == d[1]:
                    typeName1 = d[2]
                    typeName2 = d[3]
                    typeName3 = d[4]
                    typeName4 = d[5]
                    self.world.set_dihedral(self.dihedralStyle, typeName1,
                                            typeName2, typeName3, typeName4,
                                            *dc[1:], type=dihedralType)

        for ic in self.improperCoeffs:
            improperType = ic[0]
            for i in self.impropers:
                if improperType == i[1]:
                    self.world.set_improper(self.improperStyle, i[2], i[3],
                                            i[4], i[5], *ic[1:], type=improperType)

        return self.world

    def atomCount(self, line: str):
        self.world.atomCount = line.split()[0]

    def bondCount(self, line: str):
        self.world.bondCount = line.split()[0]

    def angleCount(self, line: str):
        self.world.angleCount = line.split()[0]

    def dihedralCount(self, line: str):
        self.world.dihedralCount = line.split()[0]

    def improperCount(self, line: str):
        self.world.improperCount = line.split()[0]

    def atomTypeCount(self, line: str):
        self.world.atomTypeCount = line.split()[0]

    def bondTypeCount(self, line: str):
        self.world.bondTypeCount = line.split()[0]

    def angleTypeCount(self, line: str):
        self.world.angleTypeCount = line.split()[0]

    def dihedralTypeCount(self, line: str):
        self.world.dihedralTypeCount = line.split()[0]

    def improperTypeCount(self, line: str):
        self.world.improperTypeCount = line.split()[0]

    def xBoundary(self, line: str):
        self.world.xlo, self.world.xhi, *_ = line.split()

    def yBoundary(self, line: str):
        self.world.ylo, self.world.yhi, *_ = line.split()

    def zBoundary(self, line: str):
        self.world.zlo, self.world.zhi, *_ = line.split()

    def Masses(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.masses = list()

        while not self.isblank(line):
            # self.world.topo.set_mass(line[0], line[1])
            self.masses.append(line.split())
            line = self.readline()

        assert len(self.masses) == 12

    def pairCoeffs(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.pairCoeffs = list()
        while not self.isblank(line):
            self.pairCoeffs.append(line.split())
            line = self.readline()
        assert len(self.pairCoeffs) == 12

    def bondCoeffs(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.bondCoeffs = list()
        while not self.isblank(line):
            self.bondCoeffs.append(line.split())
            line = self.readline()
        assert len(self.bondCoeffs) == 12

    def angleCoeffs(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.angleCoeffs = list()
        while not self.isblank(line):
            self.angleCoeffs.append(line.split())
            line = self.readline()
        assert len(self.angleCoeffs) == 18

    def dihedralCoeffs(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.dihedralCoeffs = list()
        while not self.isblank(line):
            self.dihedralCoeffs.append(line.split())
            line = self.readline()
        assert len(self.dihedralCoeffs) == 24

    def improperCoeffs(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.improperCoeffs = list()
        while not self.isblank(line):
            self.improperCoeffs.append(line.split())
            line = self.readline()
        assert len(self.improperCoeffs) == 6

    def Atoms(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.atoms = list()
        if self.atomStyle == 'full':
            Atom = fullAtom
        elif self.atomStyle == 'molecular':
            Atom = molecularAtom
        while not self.isblank(line):
            atom = Atom(*line.split())
            self.atoms.append(atom)
            line = self.readline()

    def Bonds(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.bonds = list()

        while not self.isblank(line):
            self.bonds.append(line.split())
            line = self.readline()

    def Angles(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.angles = list()

        while not self.isblank(line):
            self.angles.append(line.split())
            line = self.readline()

    def Dihedrals(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.dihedrals = list()

        while not self.isblank(line):
            self.dihedrals.append(line.split())
            line = self.readline()

    def Impropers(self, line: str):

        line = self.readline()
        line = self.skipblank(line)

        self.impropers = list()

        while not self.isblank(line):
            self.impropers.append(line.split())
            line = self.readline()

# class INlmpdat(InputBase):
#     def __init__(self):

#         self.data = InputData()

#     def _read_title(self, line):
#         self.data.comment = line
#         return self._readline()

#     def _readline(self):
#         return self.file.readline()

#     def _skipblankline(self, line):
#         while line.isspace() or line.startswith('#'):
#             line = self.file.readline()
#         return line

#     def _deal_with_comment(self, line):

#         if '#' in line:
#             return line[:line.index('#')]
#         else:
#             return line

#     def read_data(self, file, atom_style='full'):
#         self.atomStyle = atom_style

#         self.file_name = file

#         self.file = open(self.file_name)

#         line = self._readline()
#         line = self._read_title(line)
#         line = self._skipblankline(line)
#         ##
#         number_of_section = 14
#         i = 0
#         while i < number_of_section and line != '':

#             line = self._read_bondaries(line)
#             line = self._read_system(line)
#             line = self._read_masses(line)
#             # section to read coefficients
#             line = self._read_pair_coeffs(line)
#             line = self._read_bond_coeffs(line)
#             line = self._read_angle_coeffs(line)
#             line = self._read_dihedral_coeffs(line)
#             line = self._read_improper_coeffs(line)
#             line = self._read_velocities(line)

#             line = self._read_atoms(line)
#             line = self._read_angles(line)
#             line = self._read_bonds(line)
#             line = self._read_dihedrals(line)
#             line = self._read_impropers(line)

#             i += 1

#         # TODO: after determining the name of properies of muturalData
#         # remove rawData and muturalData -> data
#         return self._post_process()

#     def _post_process(self):
#         """ to process raw data to the mutural data

#         Args:
#             rawData ([type]): [description]

#         Returns:
#             [type]: [description]
#         """

#         # After reading all the info from the lmp file,
#         # you should post-processe them from rawData
#         # and store them to muture data

#         create = CreateAtom.genericAtoms(self.atomStyle)
#         atoms = create(self.data.atomRaw)

#         # First : create topo from the bond section
#         for b in self.data.bondRaw:
#             clabel = b[2]  # center atom id
#             plabel = b[3]  # pair atom id
#             catom = None
#             patom = None
#             for atom in atoms:
#                 if atom.label == clabel:
#                     catom = atom
#                 if atom.label == plabel:
#                     patom = atom

#             if catom is None or patom is None:
#                 raise ValueError('拓扑结构没有匹配到相应的Atom')
#             catom.add_neighbors(patom)

#         self.data.atoms = atoms

#         self.data.molecules = self.group_by('lmpdat',
#                                             atoms,
#                                             reference='parent')

#         self.data.pairCoeffs = list()
#         for pc in self.data.pairCoeffRaw:
#             self.data.pairCoeffs.append([pc[0], pc[0], *pc[1:]])

#         self.data.bondCoeffs = list()
#         for bc in self.data.bondCoeffRaw:
#             bondType = bc[0]
#             for b in self.data.bondRaw:
#                 if bondType == b[1]:
#                     typeName1 = b[2]
#                     typeName2 = b[3]
#                     self.data.bondCoeffs.append(
#                         [typeName1, typeName2, *bc[1:]])

#         self.data.angleCoeffs = list()
#         for ac in self.data.angleCoeffRaw:
#             angleType = ac[0]
#             for a in self.data.angleRaw:
#                 if angleType == a[1]:
#                     typeName1 = a[2]
#                     typeName2 = a[3]
#                     typeName3 = a[4]
#                     self.data.angleCoeffs.append(
#                         [typeName1, typeName2, typeName3, *ac[1:]])

#         self.data.dihedralCoeffs = list()
#         for dc in self.data.dihedralCoeffRaw:
#             dihedralType = dc[0]
#             for d in self.data.dihedralRaw:
#                 if dihedralType == d[1]:
#                     self.data.dihedralCoeffs.append(
#                         [d[2], d[3], d[4], d[5], *dc[1:]])

#         self.data.improperCoeffs = list()
#         for ic in self.data.improperCoeffRaw:
#             it = ic[0]
#             for i in self.data.improperRaw:
#                 if it == i[1]:
#                     self.data.improperCoeffs.append(
#                         [i[2], i[3], i[4], i[5], *ic[1:]])

#         self.data.masses = list()
#         for m in self.data.massRaw:
#             self.data.masses.append([m[0], m[1]])

#         return self.data

#     def _read_atoms(self, line):
#         line = self._skipblankline(line)
#         if 'Atoms' in line:
#             line = self._skipblankline(self._readline())
#             Atoms = list()
#             while line != '\n' and line != '':
#                 line = self._deal_with_comment(line.split())
#                 Atoms.append(line)
#                 line = self._readline()

#             self.data.atomRaw = Atoms

#         return line

#     def _read_bonds(self, line):
#         line = self._skipblankline(line)

#         if 'Bonds' in line:
#             line = self._skipblankline(self._readline())
#             Bonds = list()

#             while line != '\n' and line != '':
#                 Bonds.append(self._deal_with_comment(line.split()))
#                 line = self._readline()
#             self.data.bondRaw = Bonds

#         return line

#     def _read_angles(self, line):
#         line = self._skipblankline(line)
#         if 'Angles' in line:
#             line = self._skipblankline(self._readline())
#             Angles = list()

#             while line != '\n' and line != '':
#                 Angles.append(self._deal_with_comment(line.split()))
#                 line = self._readline()

#             self.data.angleRaw = Angles

#         return line

#     def _read_dihedrals(self, line):
#         line = self._skipblankline(line)
#         if 'Dihedrals' in line:
#             line = self._skipblankline(self._readline())
#             Dihedrals = list()

#             while line != '\n' and line != '':
#                 Dihedrals.append(self._deal_with_comment(line.split()))
#                 line = self._readline()

#             self.data.dihedralRaw = Dihedrals

#         return line

#     def _read_impropers(self, line):
#         line = self._skipblankline(line)
#         if 'Impropers' in line:
#             line = self._skipblankline(self._readline())
#             Impropers = list()

#             while line != '\n' and line != '':
#                 Impropers.append(self._deal_with_comment(line.split()))
#                 line = self._readline()

#             self.data.improperRaw = Impropers

#         return line

#     def _read_velocities(self, line):
#         line = self._skipblankline(line)
#         if 'Velocities' in line:
#             line = self._skipblankline(self._readline())
#             velocities = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 velocities.append(line)
#                 line = self._readline()

#             self.velocitiesRaw = velocities
#         return line

#     def _read_improper_coeffs(self, line):
#         line = self._skipblankline(line)
#         if 'Improper' in line and 'Coeffs' in line:
#             line = self._skipblankline(self._readline())
#             improper_coeff = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 improper_coeff.append(line)
#                 line = self._readline()

#             self.data.improperCoeffRaw = improper_coeff
#         return line

#     def _read_dihedral_coeffs(self, line):
#         line = self._skipblankline(line)
#         if 'Dihedral' in line and 'Coeffs' in line:
#             line = self._skipblankline(self._readline())
#             dihedral_coeffs = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 dihedral_coeffs.append(line)
#                 line = self._readline()

#             self.data.dihedralCoeffRaw = dihedral_coeffs
#         return line

#     def _read_angle_coeffs(self, line):
#         line = self._skipblankline(line)
#         if 'Angle' in line and 'Coeffs' in line:
#             line = self._skipblankline(self._readline())
#             angle_coeffs = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 angle_coeffs.append(line)
#                 line = self._readline()
#             self.data.angleCoeffRaw = angle_coeffs
#         return line

#     def _read_bond_coeffs(self, line):
#         line = self._skipblankline(line)
#         if 'Bond' in line and 'Coeffs' in line:
#             line = self._skipblankline(self._readline())
#             bond_coeffs = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 bond_coeffs.append(line)
#                 line = self._readline()
#             self.data.bondCoeffRaw = bond_coeffs
#         return line

#     def _read_pair_coeffs(self, line):
#         line = self._skipblankline(line)  # /n
#         if 'Pair' in line and 'Coeffs' in line:
#             line = self._skipblankline(self._readline())
#             pair_coeffs = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 pair_coeffs.append(line)
#                 line = self._readline()
#             self.data.pairCoeffRaw = pair_coeffs
#         return line

#     def _read_masses(self, line):
#         line = self._skipblankline(line)  # Masses
#         if 'Masses' in line:
#             line = self._skipblankline(self._readline())

#             masses = list()

#             while line != '\n':
#                 line = self._deal_with_comment(line.split())
#                 masses.append(line)
#                 line = self._readline()
#             self.data.massRaw = masses

#         return line

#     def _read_system(self, line):
#         line = self._skipblankline(line)
#         KEYWORDS = {
#             'atoms': 'atomCount',
#             'atom types': 'atomTypeCount',
#             'bonds': 'bondCount',
#             'bond types': 'bondTypeCount',
#             'angles': 'angleCount',
#             'angle types': 'angleTypeCount',
#             'dihedrals': 'dihedralCount',
#             'dihedral types': 'dihedralTypeCount',
#             'impropers': 'improperCount',
#             'improper types': 'improperTypeCount'
#         }

#         def _check_system(line):

#             for k in KEYWORDS:
#                 if k in line:
#                     return k  # while 'atom' == while True

#             return False

#         KEYWORD = _check_system(line)
#         while KEYWORD:

#             line = self._deal_with_comment(line.split())

#             setattr(self.data, KEYWORDS[KEYWORD], int(line[0]))

#             line = self._readline()
#             KEYWORD = _check_system(line)

#         return line

#     def _read_bondaries(self, line):

#         line = self._skipblankline(line)

#         def _check_system(line):
#             KEYWORDS = ['xlo', 'ylo', 'zlo']

#             for k in KEYWORDS:
#                 if k in line:
#                     return k  # while 'atom' == while True

#             return False

#         KEYWORD = _check_system(line)
#         while KEYWORD:
#             line = self._deal_with_comment(line.split())
#             setattr(self.data, line[-2], float(line[0]))
#             setattr(self.data, line[-1], float(line[1]))

#             line = self._readline()
#             KEYWORD = _check_system(line)

#         return line
