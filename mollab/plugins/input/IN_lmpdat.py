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

        # section 1: add linkedAtoms to atom
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

            catom.add_linkedAtoms(patom)

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
