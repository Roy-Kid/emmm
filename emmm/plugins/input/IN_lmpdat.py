# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-24
# version: 0.0.2

from emmm.plugins.input.input_base import InputData
from emmm.core.create import CreateAtom
from . import InputBase

class INlmpdat(InputBase):

    def __init__(self, world):
        super().__init__(world)
        # the raw data stores the original data from the lmp
        #   may it would get post-processed such as kwremap
        self.rawData = InputData()
        
        

    def _read_title(self, line):
        self.comment = line
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

            i+=1

        # TODO: move all the post-processes to the _post_process
        
        # After reading all the info from the lmp file,
        # you should post-processe them from rawData 
        # and store them to muture data

        create = CreateAtom.genericAtoms(atom_style)
        atoms = create(self.rawData['Atoms'])
        self.rawData.atoms = atoms

        # First : create topo from the bond section
        for b in self.rawData['Bonds']:
            clabel = b[2] # center atom id
            plabel = b[3] # pair atom id
            catom = None
            patom = None
            for atom in atoms:
                if atom.label == clabel:
                    catom = atom
                if atom.label == plabel:
                    patom = atom
            
            if catom is None or patom is None:
                raise ValueError(_('拓扑结构没有匹配到相应的Atom'))
            catom.add_neighbors(patom)
        
        # Second : orgnize atoms to the molecules according to the reference
        # default refer to atom.parent
        # because the lmpdat only have one hierarchy
        self.rawData.molecules = self.group_by('lmpdat', atoms, reference='parent')

        # Third : remap the lmp key words to standard keywords

        self._post_process(self.rawData)

        # Fourth : deal with coefficient
        # bond_coeff = self.rawData['bond_coeffs']

        self.file.close()
        return self.rawData

    def _post_process(self, rawData):
        """ to process raw data to the mutural data

        Args:
            rawData ([type]): [description]

        Returns:
            [type]: [description]
        """
        # muturalData = InputData()

        return rawData

    def _read_atoms(self, line):
        line = self._skipblankline(line)        
        if 'Atoms' in line:
            line = self._skipblankline(self._readline())
            Atoms = list()
            while line != '\n' and line != '':
                line = self._deal_with_comment(line.split())
                Atoms.append(line)
                line = self._readline()

            self.rawData['Atoms'] = Atoms

        return line 

    def _read_bonds(self, line):
        line = self._skipblankline(line)

        if 'Bonds' in line :
            line = self._skipblankline(self._readline())
            Bonds = list()

            while line != '\n' and line != '':
                Bonds.append(self._deal_with_comment(line.split()))
                line = self._readline()
            self.rawData['Bonds'] = Bonds

        return line

    def _read_angles(self, line):
        line = self._skipblankline(line)
        if 'Angles' in line :
            line = self._skipblankline(self._readline())
            self.Angles = list()

            while line != '\n' and line != '':
                self.Angles.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.rawData['Angles'] = self.Angles

        return line

    def _read_dihedrals(self, line):
        line = self._skipblankline(line)
        if 'Dihedrals' in line:
            line = self._skipblankline(self._readline())
            self.Dihedrals = list()

            while line != '\n' and line != '':
                self.Dihedrals.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.rawData['Dihedrals'] = self.Dihedrals

        return line

    def _read_impropers(self, line):
        line = self._skipblankline(line)
        if 'Impropers' in line:
            line = self._skipblankline(self._readline())
            self.Impropers = list()

            while line != '\n' and line != '':
                self.Impropers.append(self._deal_with_comment(line.split()))
                line = self._readline()

            self.rawData['Impropers'] = self.Impropers

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

            self.rawData['velocities'] = velocities
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

            self.rawData['improper_coeffs'] = improper_coeff
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

            self.rawData['dihedral_coeffs'] = dihedral_coeffs
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
            self.rawData['angle_coeffs'] = angle_coeffs
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
            self.rawData['bond_coeffs'] = bond_coeffs
        return line    

    def _read_pair_coeffs(self, line):
        line = self._skipblankline(line) # /n
        if 'Pair' in line and 'Coeffs' in line:
            line = self._skipblankline(self._readline())
            pair_coeffs = list()

            while line != '\n':
                line = self._deal_with_comment(line.split())
                pair_coeffs.append(line)
                line = self._readline()
            self.rawData['pair_coeffs'] = pair_coeffs
        return line

    def _read_masses(self, line):
        line = self._skipblankline(line) # Masses
        if 'Masses' in line:
            line = self._skipblankline(self._readline())
            
            masses = list()

            while line!= '\n':
                line = self._deal_with_comment(line.split())
                masses.append(line)
                line = self._readline()
            self.rawData['Masses'] = masses
            
        return line

    def _read_system(self, line):
        line = self._skipblankline(line)
        def _check_system(line):
            KEYWORDS = ['atoms', 'atom types', 'bonds', 'bond types', 'angles', 'angle types', 'dihedrals', 'dihedral types', 'impropers', 'improper types']

            for k in KEYWORDS:
                if k in line:
                    return k # while 'atom' == while True

            return False

        KEYWORD = _check_system(line)
        while KEYWORD:

            line = self._deal_with_comment(line.split())

            self.rawData[KEYWORD] = int(line[0])

            line = self._readline()
            KEYWORD = _check_system(line)
        

        return line

    def _read_bondaries(self, line):

        line = self._skipblankline(line)
        def _check_system(line):
            KEYWORDS = ['xlo', 'ylo', 'zlo']

            for k in KEYWORDS:
                if k in line:
                    return k # while 'atom' == while True

            return False

        KEYWORD = _check_system(line)
        while KEYWORD:
            line = self._deal_with_comment(line.split())
            self.rawData[KEYWORD] = float(line[0])
            self.rawData[line[-1]] = float(line[1])
            
            line = self._readline()
            KEYWORD = _check_system(line)

        return line
