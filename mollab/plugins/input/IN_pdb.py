# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1
# reference: http://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html

from . import InputBase
from . import INxml
from mollab.plugins.input.input_base import InputData
from mollab.core.create import CreateAtom


class INpdb(InputBase):
    def __init__(self) -> None:

        self.data = InputData()
        self.data.atomRaw = list()
        self.data.atoms = list()
        self.data.bondRaw = list()
        # Record name -> KEYWORD
        self.KEYWORLD = ['ATOM', 'CONECT', 'TER']
        self.executor = {
            'ATOM': self.ATOM,
            'CONECT': self.CONNET,
            'TER': self.TER
        }

    def read_data(self, file, xml=None):

        f = open(file, 'r')
        line = f.readline()
        self.data.comment = line.split()[1:]
        line = f.readline()
        while not line.startswith('END'):
            record_name = line[:7].strip()
            if record_name not in self.KEYWORLD:
                raise KeyError('wrong keyword')
            else:
                self.executor[record_name](line)

            line = f.readline()

        if xml:
            inxml = INxml().read_data(xml)
            

        self._post_process()

        return self.data

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

        self.data.atomRaw.append([
            serial, name, altLoc, resName, chainID, resSeq, x, y, z, occupancy,
            tempFactor, element, charge
        ])

    def TER(self, line):
        pass

    def CONNET(self, line):
        line.ljust(31)

        a = line[7:12].strip()
        a1 = line[12:17].strip()
        a2 = line[17:22].strip()
        a3 = line[22:27].strip()
        a4 = line[27:31].strip()

        self.data.bondRaw.append([i for i in [a, a1, a2, a3, a4] if i != ''])

    def _post_process(self):

        # Atom section
        create = CreateAtom.genericAtom('pdb')
        for r in self.data.atomRaw:
            atom = create(r[0], r[1], r[3], r[6], r[7], r[8])
            self.data.atoms.append(atom)

        # Bond section
        for b in self.data.bondRaw:
            cid = b[0]
            pid = b[1]
            catom = None
            patom = None
            for atom in self.data.atoms:
                if atom.id == cid:
                    catom = atom
                if atom.id == pid:
                    patom = atom

            if catom is None or patom is None:
                raise ValueError('拓扑结构没有匹配到相应的Atom')
            catom.add_neighbors(patom)

        self.data.molecules = self.group_by('pdb', self.data.atoms)

