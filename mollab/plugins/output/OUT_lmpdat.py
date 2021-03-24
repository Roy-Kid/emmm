# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from mollab.plugins.output.output_base import Mapper, OutputBase
from jinja2 import Template

class OUTlmpdat(OutputBase):
    def __init__(self) -> None:
        super().__init__()


    def write_data(self, fname, item):
        self.item = item
        self.atomIdMapper = Mapper('atomId')
        for atom in self.item.atoms:
            self.atomIdMapper.add(atom.id)

        self.file = open(fname, 'w')

        write_order = [
            # item is a world or a molecule
            self.comment(item),
            self.atomCount(item),
            self.bondCount(item),
            self.angleCount(item),
            self.dihedralCount(item),
            # self.improperCount(item),
            self.atomTypeCount(item),
            self.bondTypeCount(item),
            self.angleTypeCount(item),
            self.dihedralTypeCount(item),
            # self.improperTypeCount(item),
            self.boundary(item),
            self.masses(item),
            self.pair_coeffs(item),
            self.bond_coeffs(item),
            self.angle_coeffs(item),
            self.dihedral_coeffs(item),
            # self.improper_coeffs(item),
            self.Atoms(item),
            self.Bonds(item),
            self.Angles(item),
            self.Dihedrals(item),
            # self.Impropers(item)
        ]

        for o in write_order:
            self.file.writelines(o)

        # # write types.txt
        # with open('types.txt', 'w') as f:
        #     f.write('atom types\n')
        #     for type, id in self.item.atomTypeMapper.items():
        #         f.write(f'{id}  {type.replace("-", ",")}\n')

        #     f.write('bond types\n')
        #     for type, id in self.item.bondTypeMapper.items():
        #         f.write(f'{id}  {type.replace("-", ",")}\n')

        #     f.write('angle types\n')
        #     for type, id in self.item.angleTypeMapper.items():
        #         f.write(f'{id}  {type.replace("-", ",")}\n')

        #     f.write('dihedral types\n')
        #     for type, id in self.item.dihedralTypeMapper.items():
        #         f.write(f'{id}  {type.replace("-", ",")}\n')

        #     # f.write('improper types\n')
        #     # for type, id in self.item.improperTypeMapper.items():
        #     #     f.write(f'{id} {type.replace("-", ",")}\n')

        self.file.close()

    def comment(self, item):
        return f'LAMMPS data from { getattr(item, "comment", "label") } Created by Mollab\n\n'

    def atomCount(self, item):

        return f'\t  {item.atomCount }  atoms\n'

    def bondCount(self, item):

        return f'\t  {item.bondCount}  bonds\n'

    def angleCount(self, item):

        return f'\t  {item.angleCount}  angles\n'

    def dihedralCount(self, item):

        return f'\t  {item.dihedralCount}  dihedrals\n'

    def improperCount(self, item):

        return f'\t  {item.improperCount}  impropers\n\n'

    def atomTypeCount(self, item):

        return f'\t  {self.item.atomTypeCount}  atom types\n'

    def bondTypeCount(self, item):
        return f'\t  {self.item.bondTypeCount}  bond types\n'

    def angleTypeCount(self, item):
        return f'\t  {self.item.angleTypeCount}  angle types\n'

    def dihedralTypeCount(self, item):
        return f'\t  {self.item.dihedralTypeCount}  dihedral types\n'

    def improperTypeCount(self, item):
        return f'\t  {self.item.improperTypeCount}  improper types\n\n'

    def boundary(self, item):
        return [
            f'\t  {self.item.xlo}\t{self.item.xhi}\txlo\txhi\n',
            f'\t  {self.item.ylo}\t{self.item.yhi}\tylo\tyhi\n',
            f'\t  {self.item.zlo}\t{self.item.zhi}\tzlo\tzhi\n\n'
        ]

    def masses(self, item):

        lines = list()
        lines.append('Masses\n\n')

        for k, v in self.item.massMapper.items():
            lines.append(f'\t{self.item.atomTypeMapper.retrieve(k)}\t{v}\n')
        lines.append('\n')
        return lines

    def pair_coeffs(self, item):
        lines = list()
        lines.append('Pair Coeffs\n\n')
        for pp in self.item.forcefield.pairPotentialList:
            coeffs = [pp.typeId, *pp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            pc = '\t'.join(coeffs)
            lines.append(f'\t\t{ pc }\n')
        lines.append('\n')
        return lines

    def bond_coeffs(self, item):
        lines = list()
        lines.append('Bond Coeffs\n\n')
        for bp in self.item.forcefield.bondPotentialList:

            coeffs = [bp.typeId, *bp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            bc = '\t'.join(coeffs)
            lines.append(f'\t\t{bc}\n')
        lines.append('\n')
        return lines

    def angle_coeffs(self, item):
        lines = list()
        lines.append('Angle Coeffs\n\n')
        for ap in self.item.forcefield.anglePotentialList:
            coeffs = [ap.typeId, *ap.lmp_format]
            coeffs = [str(i) for i in coeffs]
            ac = '\t'.join(coeffs)
            lines.append(f'\t\t{ac}\n')
        lines.append('\n')
        return lines

    def dihedral_coeffs(self, item):
        lines = list()
        lines.append('Dihedral Coeffs\n\n')
        for dp in self.item.forcefield.dihedralPotentialList:
            coeffs = [dp.typeId, *dp.lmp_format]
            coeffs = [str(i) for i in coeffs]
            dc = '\t'.join(coeffs)
            lines.append(f'\t\t{dc}\n')
        lines.append('\n')
        return lines

    def improper_coeffs(self, item):
        lines = list()
        lines.append('Improper Coeffs\n\n')

        for ip in self.item.forcefield.improperPotentialList:
            coeffs = [ip.typeId, *ip.lmp_format]
            coeffs = [str(i) for i in coeffs]
            ip = '\t'.join(coeffs)
            lines.append(f'\t\t{ip}\n')
        lines.append('\n')
        return lines

    def Atoms(self, item):
        lines = list()
        lines.append('Atoms\n\n')

        for atom in item.atoms:
            lines.append(
                f'\t{atom.atomId}\t{atom.molId}\t{atom.typeId}\t{atom.q}\t{atom.x}\t{atom.y}\t{atom.z}  # {atom.type}\n'
            )

        lines.append('\n')
        return lines

    def Bonds(self, item):
        lines = list()
        lines.append(f'Bonds\n\n')

        for id, bond in enumerate(item.bonds, 1):

            lines.append(
                f'\t{id}\t{bond.typeId}\t{bond.atom1.atomId}\t{bond.atom2.atomId}\n'
            )

        lines.append(f'\n')
        return lines

    def Angles(self, item):
        lines = list()
        lines.append(f'Angles\n\n')

        self.angleTypeMap = list()

        for id, angle in enumerate(item.angles, 1):

            lines.append(
                f'\t{id}\t{angle.typeId}\t{angle.atom1.atomId}\t{angle.atom2.atomId}\t{angle.atom3.atomId}\n'
            )

        lines.append(f'\n')
        return lines

    def Dihedrals(self, item):
        lines = list()
        lines.append(f'Dihedrals\n\n')

        self.dihedralTypeMap = list()

        for id, dihedral in enumerate(item.dihedrals, 1):

            lines.append(
                f'\t{id}\t{dihedral.typeId}\t{dihedral.atom1.atomId}\t{dihedral.atom2.atomId}\t{dihedral.atom3.atomId}\t{dihedral.atom4.atomId}  #{dihedral.atom1.type}-{dihedral.atom2.type}-{dihedral.atom3.type}-{dihedral.atom4.type}\n'
            )
        lines.append(f'\n')
        return lines

    def Impropers(self, item):
        lines = list()
        lines.append(f'Impropers\n\n')

        self.ImproperTypeMap = list()

        for id, improper in enumerate(item.impropers, 1):
            lines.append(
                f'\t{id}\t{improper.typeId}\t{improper.atom1.atomId}\t{improper.atom2.atomId}\t{improper.atom3.atomId}\t{improper.atom4.atomId}\n'
            )
        lines.append(f'\n')
        return lines
