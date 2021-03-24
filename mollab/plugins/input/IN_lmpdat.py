# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-03-16
# version: 0.0.3

from collections import defaultdict
from mollab.core.atom import fullAtom
from mollab.plugins.input import InputBase
from mollab.core.world import World
from mollab.core.pbc import PBC
from mollab.core.bond import Bond
from mollab.core.angle import Angle
from mollab.core.dihedral import Dihedral
from mollab.core.improper import Improper
from mollab.core.molecule import Molecule
from tqdm import tqdm



class INlmpdat(InputBase):
    def __init__(self) -> None:
        super().__init__()

    def skipBlank(self, line, lines):
        while self.isBlank(line):
            line = next(lines)
        return line

    def isBlank(self, line):
        # line: str -> bool(line.strip())
        return not line.strip()

    def read(self, fname, option: dict = {}):

        raw = option

        atomStyle = option.get('atomStyle', None)
        bondStyle = option.get('bondStyle', None)
        angleStyle = option.get('angleStyle', None)
        dihedralStyle = option.get('dihedralStyle', None)
        improperStyle = option.get('improperStyle', None)
        pairStyle = option.get('pairStyle', None)

        pairCoeffs = dict()
        bondCoeffs = dict()
        angleCoeffs = dict()
        dihedralCoeffs = dict()
        improperCoeffs = dict()
        
        isTopoBond = option.get('isTopoBond', None)
        isTopoAngle = option.get('isTopoAngle', None)
        isTopoDihedral = option.get('isTopoDihedral', None)
        isTopoImproper = option.get('isTopoImproper', None)

        world = World(fname)
        f = open(fname, 'r')

        lines = f.readlines()

        world.comment = lines[0]

        lines = iter(lines[1:])

        for line in tqdm(lines):
            line = line.split()
            if 'atoms' in line:
                raw['atomCount'] = int(line[0])
                world.atomCount = int(line[0])

            elif 'bonds' in line:
                raw['bondCount'] = int(line[0])
                world.bondCount = int(line[0])

            elif 'angles' in line:
                raw['angleCount'] = int(line[0])
                world.angleCount = int(line[0])

            elif 'dihedrals' in line:
                raw['dihedralCount'] = int(line[0])
                world.dihedralCount = int(line[0])

            elif 'impropers' in line:
                raw['improperCount'] = int(line[0])
                world.improperCount = int(line[0])

            elif 'atom' in line and 'types' in line:
                raw['atomTypeCount'] = int(line[0])
                world.atomTypeCount = int(line[0])

            elif 'bond' in line and 'types' in line:
                raw['bondTypeCount'] = int(line[0])
                world.bondTypeCount = int(line[0])

            elif 'angle' in line and 'types' in line:
                raw['angleTypeCount'] = int(line[0])
                world.angleTypeCount = int(line[0])

            elif 'dihedral' in line and 'types' in line:
                raw['dihedralTypeCount'] = int(line[0])
                world.dihedralTypeCount = int(line[0])

            elif 'improper' in line and 'types' in line:
                raw['improperTypeCount'] = int(line[0])
                world.improperTypeCount = int(line[0])

            elif 'xlo' in line:
                world.xlo, world.xhi = float(line[0]), float(line[1])

            elif 'ylo' in line:
                world.ylo, world.yhi = float(line[0]), float(line[1])

            elif 'zlo' in line:
                world.zlo, world.zhi = float(line[0]), float(line[1])

            elif 'Masses' in line:
                line = next(lines)
                line = self.skipBlank(line, lines)
                # {atomType: mass}
                masses = dict()
                for m in range(raw['atomTypeCount']):
                    line = line.split()
                    masses[line[0]] = line[1]
                    line = next(lines)
                raw['masses'] = masses

            elif 'Coeffs' in line:
                if 'Pair' in line:
                    line = next(lines)
                    line = self.skipBlank(line, lines)
                    # {atomType: paircoeffs}
                    for p in range(raw['atomTypeCount']):
                        line = line.split()
                        pairCoeffs[line[0]] = line[1:]
                        line = next(lines)
                    raw['pairCoeffs'] = pairCoeffs


                elif 'Bond' in line:
                    line = next(lines)
                    line = self.skipBlank(line, lines)
                    # {bondType: bondCoeff}

                    for b in range(raw['bondTypeCount']):
                        line = line.split()
                        bondCoeffs[line[0]] = line[1:]
                        line = next(lines)


                elif 'Angle' in line:
                    line = next(lines)
                    line = self.skipBlank(line, lines)
                    for a in range(raw['angleTypeCount']):
                        line = line.split()
                        angleCoeffs[line[0]] = line[1:]
                        line = next(lines)


                elif 'Dihedral' in line:
                    line = next(lines)
                    line = self.skipBlank(line, lines)

                    for d in range(raw['dihedralTypeCount']):
                        line = line.split()
                        dihedralCoeffs[line[1]] = line[2:]
                        line = next(lines)


                elif 'Improper' in line:
                    line = next(lines)
                    line = self.skipBlank(line, lines)

                    for i in range(raw['improperTypeCount']):
                        line = line.split()
                        improperCoeffs[line[1]] = line[2:] 
                        line = next(lines)

            elif 'Atoms' in line:
                line = next(lines)
                line = self.skipBlank(line, lines)
                atoms = dict()
                pbc = PBC(world.xlo, world.xhi, world.ylo, world.yhi, world.zlo, world.zhi)
                if atomStyle == 'full':
                    if len(line.split()) == 7:
                    # atomId molId type q x y z
                        for a in range(raw['atomCount']):
                            l = line.split()
                            atom = fullAtom(l[0], l[1], l[2], l[3], x=l[4], y=l[5], z=l[6])
                            pbc.wrap(atom)
                            atoms[l[0]] = atom
                            line = next(lines)

                    elif len(line.split()) == 10:
                    # atomId molId type q wx wy wz ix iy iz
                        for a in range(world.atomCount):
                            l = line.split()
                            atom = fullAtom(l[0], l[1], l[2], l[3], wx=l[4], wy=l[5], wz=l[6], ix=l[7], iy=l[8], iz=l[9])
                            pbc.unwrap(atom)
                            atoms[l[0]] = atom
                            line = next(lines)

            elif 'Bonds' in line:
                line = next(lines)
                line = self.skipBlank(line, lines)
                bonds = defaultdict(list)
                # bonds = {typeId: [atom1, atom2]}
                for b in range(raw['bondCount']):
                    line = line.split()
                    bonds[line[1]].append([atoms[line[2]], atoms[line[3]]])
                    atoms[line[2]].add_linkedAtoms(atoms[line[3]])
                    line = next(lines)

            elif 'Angles' in line:
                line = next(lines)
                line = self.skipBlank(line, lines)
                angles = defaultdict(list)
                for a in range(raw['angleCount']):
                    line = line.split()
                    angles[l[1]].append([atoms[line[2]], atoms[line[3]], atoms[line[4]]])
                    line = next(lines)

            elif 'Dihedrals' in line:
                line = next(lines)
                line = self.skipBlank(line, lines)
                dihedrals = defaultdict(list)
                for d in range(raw['dihedralCount']):
                    line = line.split()
                    dihedrals[line[1]].append([atoms[line[2]], atoms[line[3]], atoms[line[4]], atoms[line[5]]])
                    line = next(lines)

            elif 'Impropers' in line:
                line = next(lines)
                line = self.skipBlank(line, lines)
                impropers = defaultdict(list)
                for i in range(raw['improperCount']):
                    line = line.split()
                    impropers[l[1]].append([atoms[line[2]], atoms[line[3]], atoms[line[4]], atoms[line[5]]])
                    line = next(lines)

        # post-process
        # group atoms to the molecules
        molecules = list()
        grouped_atoms = defaultdict(list)
        for atom in atoms.values():
            # set mass
            atom.mass = raw['masses'][atom.type]

            # 
            ref = getattr(atom, 'molId', 'UNDEFINED')
            grouped_atoms[ref].append(atom)
        for ref, gatom in grouped_atoms.items():
            mol = Molecule(label=ref)
            mol.add_items(*gatom)
            molecules.append(mol)

        world.add_items(*molecules, isUpdate=False)

        # set coeff
        if pairCoeffs and pairStyle:
            for pt, pc in pairCoeffs.items():
                world.set_pair(pairStyle, pt, pt, *pc, type=pt)

        bondPotential = dict()
        if bondCoeffs and bondStyle:
            for bt, bc in bondCoeffs.items():
                bondAtom = bonds[bt]
                atom1 = bondAtom[0]
                atom2 = bondAtom[1]
                bondPotential[bt] = world.set_bond(bondStyle, atom1.type, atom2.type, bc[1:], type=bc[0])
            if not isTopoBond:
                for btype, bond in bonds.items():
                    for bon in bond:
                        world.topo.bonds.append(Bond(bon[0], bon[1], bp=bondPotential[btype]))

        anglePotential = dict()
        if angleCoeffs and angleStyle:
            for at, ac in angleCoeffs.items():
                angle = angles[at]
                atom1 = angle[0]
                atom2 = angle[1]
                atom3 = angle[2]
                anglePotential[at] = world.set_angle(angleStyle, atom1.type, atom2.type, atom3.type, ac, type=at)
            if not isTopoAngle:
                for atype, angle in angles.items():

                    world.topo.angles.append(Angle(angle[0], angle[1], angle[2], ap=anglePotential[atype]))

        dihedralPotential = dict()
        if dihedralCoeffs and dihedralStyle:
            for dt, dc in dihedralCoeffs.items():
                dihedral = dihedrals[dt]
                dihedralPotential[dt] = world.set_dihedral(dihedralStyle, dihedral[0].type, dihedral[1].type, dihedral[2].type, dihedral[3].type, dc, type=dt)
            if not isTopoDihedral:
                for dtype, dihedral in dihedrals.items():
                    world.topo.dihedrals.append(Dihedral(dihedral[0], dihedral[1], dihedral[2], dihedral[3], dp=dihedralPotential[dtype]))

        improperPotential = dict()
        if improperCoeffs and improperStyle:
            for it, ic in improperCoeffs.items():
                improper = impropers[it]
                improperPotential[it] = world.set_improper(improperStyle, improper[0].type, improper[2].type, improper[3].type, improper[4].type, ic, type=it)
            if not isTopoImproper:
                for itype, improper in impropers.items():
                    world.topo.impropers.append(Improper(improper[0], improper[1], improper[2], improper[3], ip=improperPotential[itype]))

        world.update(isTopoBond, isTopoAngle, isTopoDihedral, isTopoImproper)
        return world