# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1
# reference: http://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html

from collections import defaultdict
from mollab.core.atom import pdbAtom
from mollab.core.world import World
from mollab.plugins.input.input_base import InputBase
from mollab.core.molecule import pdbMolecule
from mollab.plugins.input.IN_xml import INxml


class INpdb(InputBase):
    def __init__(self) -> None:
        super().__init__()
        # Record name -> KEYWORD
        self.KEYWORLD = ['ATOM', 'CONECT', 'TER']
        self.atoms = list()
        self.bonds = list()

    def skipblank(self, line):
        # while line.isspace() or line.strip().startswith('#'):
        while self.isblank(line):
            line = self.readline()
        return line

    def readline(self):
        return self.f.readline()

    def isblank(self, line: str):
        return not bool(line.strip())

    def read(self, file, xml=None):

        self.world = World()

        self.f = open(file, 'r')
        line = self.readline()
        self.world.comment = line
        line = self.readline()

        while True:
            line = self.readline()
            if line.strip() == 'END':
                # read EOF
                break

            status = line.split()[0]
            execute = getattr(self, status, self.status_error)
            execute(line)

        # if xml:
        #     inxml = INxml().read_data(xml)

        self._post_process()

        return self.world

    def status_error(self, line):
        raise Exception(f'read error at "{line}"')

    def ATOM(self, line):
        # COLUMNS        DATA  TYPE    FIELD        DEFINITION                   FIELD IN MOLLAB
        # -------------------------------------------------------------------------------------
        #  1 -  6        Record name   "ATOM  "
        #  7 - 11        Integer       serial       Atom  serial number.                id
        # 13 - 16        Atom          name         Atom name.                         label
        # 17             Character     altLoc       Alternate location indicator.       \
        # 18 - 20        Residue name  resName      Residue name.                      parent
        # 22             Character     chainID      Chain identifier.                   \
        # 23 - 26        Integer       resSeq       Residue sequence number.            \
        # 27             AChar         iCode        Code for insertion of residues.     \
        # 31 - 38        Real(8.3)     x            coordinates for X in Angstroms.     x
        # 39 - 46        Real(8.3)     y            coordinates for Y in Angstroms.     y
        # 47 - 54        Real(8.3)     z            coordinates for Z in Angstroms.     z
        # 55 - 60        Real(6.2)     occupancy    Occupancy.                          \
        # 61 - 66        Real(6.2)     tempFactor   Temperature  factor.                \
        # 77 - 78        LString(2)    element      Element symbol, right-justified.    \
        # 79 - 80        LString(2)    charge       Charge  on the atom.                \
        line.ljust(81)

        serial = line[7:12].strip()
        name = line[13:17].strip()
        altLoc = line[17].strip()
        resName = line[17:21].strip()
        chainID = line[22].strip()
        resSeq = line[23:27].strip()
        x = line[31:39].strip()
        y = line[39:47].strip()
        z = line[47:55].strip()
        occupancy = line[55:61].strip()
        tempFactor = line[61:67].strip()
        element = line[77:79].strip()
        charge = line[79:81].strip()

        self.atoms.append(
            pdbAtom(serial, name, altLoc, resName, chainID, resSeq, x, y, z,
                    occupancy, tempFactor, element, charge))

    def TER(self, line):
        pass

    def CONNET(self, line):
        line.ljust(31)

        a = line[7:12].strip()
        a1 = line[12:17].strip()
        a2 = line[17:22].strip()
        a3 = line[22:27].strip()
        a4 = line[27:31].strip()

        self.bonds.append([i for i in [a, a1, a2, a3, a4] if i != ''])

    def _post_process(self):

        # section 1: add neighbors to atom
        grouped_atoms = defaultdict(list)
        for b in self.bonds:
            cid = b[0]
            for bb in b[1:]:
                pid = bb
                catom = None
                patom = None
                for atom in self.atoms:
                    if atom.serial == cid:
                        catom = atom
                    if atom.serial == pid:
                        patom = atom

                if catom is None or patom is None:
                    raise ValueError('拓扑结构没有匹配到相应的Atom')
                catom.add_neighbors(patom)

        # section 2
        molecules = list()
        for ref, gatom in grouped_atoms.items():
            mol = pdbMolecule(ref)
            mol.add_items(*gatom)
            molecules.append(mol)

        self.world.add_items(*molecules)
