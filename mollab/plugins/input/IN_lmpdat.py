# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-24
# version: 0.0.2

from mollab.plugins.input.input_base import InputData
from mollab.core.create import CreateAtom
from . import InputBase


class INlmpdat(InputBase):
    def __init__(self):

        self.data = InputData()

    def _read_title(self, line):
        self.data.comment = line
        return self._readline()

    def _readline(self):
        return self.file.readline()

    def _skipblankline(self, line):
        while line.isspace() or line.startswith('#'):
            line = self.file.readline()
        return line

    def _deal_with_comment(self, line):

        if '#' in line:
            return line[:line.index('#')]
        else:
            return line

    def read_data(self, file, atom_style='full'):
        self.atomStyle = atom_style

        self.file_name = file

        self.file = open(self.file_name)

        line = self._readline()
        line = self._read_title(line)
        line = self._skipblankline(line)
        ##
        number_of_section = 14
        i = 0
        while i < number_of_section and line != '':

            line = self._read_bondaries(line)
            line = self._read_system(line)
            line = self._read_masses(line)
            # section to read coefficients
            line = self._read_pair_coeffs(line)
            line = self._read_bond_coeffs(line)
            line = self._read_angle_coeffs(line)
            line = self._read_dihedral_coeffs(line)
            line = self._read_improper_coeffs(line)
            line = self._read_velocities(line)

            line = self._read_atoms(line)
            line = self._read_angles(line)
            line = self._read_bonds(line)
            line = self._read_dihedrals(line)
            line = self._read_impropers(line)

            i += 1

        # TODO: after determining the name of properies of muturalData
        # remove rawData and muturalData -> data
        return self._post_process()

    def _post_process(self):
        """ to process raw data to the mutural data

        Args:
            rawData ([type]): [description]

        Returns:
            [type]: [description]
        """

        # After reading all the info from the lmp file,
        # you should post-processe them from rawData
        # and store them to muture data

        create = CreateAtom.genericAtoms(self.atomStyle)
        atoms = create(self.data.atomRaw)

        # First : create topo from the bond section
        for b in self.data.bondRaw:
            clabel = b[2]  # center atom id
            plabel = b[3]  # pair atom id
            catom = None
            patom = None
            for atom in atoms:
                if atom.label == clabel:
                    catom = atom
                if atom.label == plabel:
                    patom = atom

            if catom is None or patom is None:
                raise ValueError('拓扑结构没有匹配到相应的Atom')
            catom.add_neighbors(patom)

        self.data.atoms = atoms

        self.data.molecules = self.group_by('lmpdat',
                                            atoms,
                                            reference='parent')

        self.data.pairCoeffs = list()
        for pc in self.data.pairCoeffRaw:
            self.data.pairCoeffs.append([pc[0], pc[0], *pc[1:]])

        self.data.bondCoeffs = list()
        for bc in self.data.bondCoeffRaw:
            bondType = bc[0]
            for b in self.data.bondRaw:
                if bondType == b[1]:
                    typeName1 = b[2]
                    typeName2 = b[3]
                    self.data.bondCoeffs.append(
                        [typeName1, typeName2, *bc[1:]])

        self.data.angleCoeffs = list()
        for ac in self.data.angleCoeffRaw:
            angleType = ac[0]
            for a in self.data.angleRaw:
                if angleType == a[1]:
                    typeName1 = a[2]
                    typeName2 = a[3]
                    typeName3 = a[4]
                    self.data.angleCoeffs.append(
                        [typeName1, typeName2, typeName3, *ac[1:]])

        self.data.dihedralCoeffs = list()
        for dc in self.data.dihedralCoeffRaw:
            dihedralType = dc[0]
            for d in self.data.dihedralRaw:
                if dihedralType == d[1]:
                    self.data.dihedralCoeffs.append(
                        [d[2], d[3], d[4], d[5], *dc[1:]])

        self.data.improperCoeffs = list()
        for ic in self.data.improperCoeffRaw:
            it = ic[0]
            for i in self.data.improperRaw:
                if it == i[1]:
                    self.data.improperCoeffs.append(
                        [i[2], i[3], i[4], i[5], *ic[1:]])

        self.data.masses = list()
        for m in self.data.massRaw:
            self.data.masses.append([m[0], m[1]])

        return self.data

    def _read_atoms(self, line):
        line = self._skipblankline(line)
        if 'Atoms' in line:
            line = self._skipblankline(self._readline())
            Atoms = list()
            while line != '\n' and line != '':
                line = self._deal_with_comment(line.split())
                Atoms.append(line)
                line = self._readline()

            self.data.atomRaw = Atoms

        return line

    def _read_bonds(self, line):
        line = self._skipblankline(line)

        if 'Bonds' in line:
            line = self._skipblankline(self._readline())
            Bonds = list()

            while line != '\n' and line != '':
                Bonds.append(self._deal_with_comment(line.split()))
                line = self._readline()
            self.data.bondRaw = Bonds

        return line

    def _read_angles(self, line):
        line = self._skipblankline(line)
        if 'Angles' in line:
            line = self._skipblankline(self._readline())
            Angles = list()

            while line != '\n' and line != '':
                Angles.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.data.angleRaw = Angles

        return line

    def _read_dihedrals(self, line):
        line = self._skipblankline(line)
        if 'Dihedrals' in line:
            line = self._skipblankline(self._readline())
            Dihedrals = list()

            while line != '\n' and line != '':
                Dihedrals.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.data.dihedralRaw = Dihedrals

        return line

    def _read_impropers(self, line):
        line = self._skipblankline(line)
        if 'Impropers' in line:
            line = self._skipblankline(self._readline())
            Impropers = list()

            while line != '\n' and line != '':
                Impropers.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.data.improperRaw = Impropers

        return line

    def _read_velocities(self, line):
        line = self._skipblankline(line)
        if 'Velocities' in line:
            line = self._skipblankline(self._readline())
            velocities = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                velocities.append(line)
                line = self._readline()

            self.velocitiesRaw = velocities
        return line

    def _read_improper_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Improper' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            improper_coeff = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                improper_coeff.append(line)
                line = self._readline()

            self.data.improperCoeffRaw = improper_coeff
        return line

    def _read_dihedral_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Dihedral' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            dihedral_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                dihedral_coeffs.append(line)
                line = self._readline()

            self.data.dihedralCoeffRaw = dihedral_coeffs
        return line

    def _read_angle_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Angle' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            angle_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                angle_coeffs.append(line)
                line = self._readline()
            self.data.angleCoeffRaw = angle_coeffs
        return line

    def _read_bond_coeffs(self, line):
        line = self._skipblankline(line)
        if 'Bond' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            bond_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                bond_coeffs.append(line)
                line = self._readline()
            self.data.bondCoeffRaw = bond_coeffs
        return line

    def _read_pair_coeffs(self, line):
        line = self._skipblankline(line)  # /n
        if 'Pair' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            pair_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                pair_coeffs.append(line)
                line = self._readline()
            self.data.pairCoeffRaw = pair_coeffs
        return line

    def _read_masses(self, line):
        line = self._skipblankline(line)  # Masses
        if 'Masses' in line:
            line = self._skipblankline(self._readline())

            masses = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                masses.append(line)
                line = self._readline()
            self.data.massRaw = masses

        return line

    def _read_system(self, line):
        line = self._skipblankline(line)
        KEYWORDS = {
            'atoms': 'atomCount',
            'atom types': 'atomTypeCount',
            'bonds': 'bondCount',
            'bond types': 'bondTypeCount',
            'angles': 'angleCount',
            'angle types': 'angleTypeCount',
            'dihedrals': 'dihedralCount',
            'dihedral types': 'dihedralTypeCount',
            'impropers': 'improperCount',
            'improper types': 'improperTypeCount'
        }

        def _check_system(line):

            for k in KEYWORDS:
                if k in line:
                    return k  # while 'atom' == while True

            return False

        KEYWORD = _check_system(line)
        while KEYWORD:

            line = self._deal_with_comment(line.split())

            setattr(self.data, KEYWORDS[KEYWORD], int(line[0]))

            line = self._readline()
            KEYWORD = _check_system(line)

        return line

    def _read_bondaries(self, line):

        line = self._skipblankline(line)

        def _check_system(line):
            KEYWORDS = ['xlo', 'ylo', 'zlo']

            for k in KEYWORDS:
                if k in line:
                    return k  # while 'atom' == while True

            return False

        KEYWORD = _check_system(line)
        while KEYWORD:
            line = self._deal_with_comment(line.split())
            setattr(self.data, line[-2], float(line[0]))
            setattr(self.data, line[-1], float(line[1]))

            line = self._readline()
            KEYWORD = _check_system(line)

        return line
