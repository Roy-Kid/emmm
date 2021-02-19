# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1

from collections import defaultdict
from mollab.core.atom import pdbAtom
from mollab.core.molecule import pdbMolecule
from mollab.plugins.input.input_base import InputBase
from mollab.core.world import World
import xml.etree.ElementTree as ET


class INxml(InputBase):
    def __init__(self) -> None:
        super().__init__()

    def read(self, fname, world=None):

        tree = ET.parse(fname)

        if world is None:
            self.world = World()

        else:
            self.world = world
            post_process = self._process_with_world

        root = tree.getroot()

        for child in root:

            executor = getattr(self, child.tag, self.status_error)

            executor(child)

        # post_process()
        return self.world

    def _process_with_world(self):

        if getattr(self.world, 'atoms', None):
            for atom in self.world.atoms:
                residue = self.Residues[atom.resName]
                for r in residue:
                    if atom.name == r['name']:
                        for t in self.AtomTypes:
                            if r['type'] == t['name']:
                                atom.type = t['class']
                                atom.element = t['element']
                                atom.mass = t['mass']

        else:
            atoms = list()
            for at in self.AtomTypes:
                for resName, resAtom in self.Residues.items():
                    if at['name'] == resAtom['type']:
                        atom = pdbAtom(0, at['name'], 0, resName, 0, 0, 0, 0, 0, 0, 0, at['element'], 0)
                        atom.mass = at['mass']
                        atoms.append(atom)

            molecules = list()
            grouped_atoms = defaultdict(list)
            for atom in atoms:
                ref = getattr(atom, 'resSeq', 'UNDEFINED')
                grouped_atoms[ref].append(atom)
            for ref, gatom in grouped_atoms.items():
                mol = pdbMolecule(ref)
                mol.add_items(*gatom)
                molecules.append(mol)
            self.world.add_items(*molecules)


    def status_error(self, root):
        raise Exception(f'unknown tag {root.tag}')

    def AtomTypes(self, root):
        self.AtomTypes = list()
        for i in root:
            self.AtomTypes.append(i.attrib)

    def Residues(self, root):
        self.Residues = dict()
        for Residue in root:
            res = self.Residues[Residue.attrib['name']] = list()
            for r in Residue:
                res.append(r.attrib)

    def HarmonicBondForce(self, root):

        
        for bc in root:
            bc = bc.attrib
            self.world.set_bond('harmonic', bc['class1'], bc['class2'],
                                bc['length'], bc['k'])

    def HarmonicAngleForce(self, root):

        for ac in root:
            ac = ac.attrib
            self.world.set_angle('harmonic', ac['class1'], ac['class2'],
                                 ac['class3'], ac['angle'], ac['k'])

    def PeriodicTorsionForce(self, root):
        pass

    def NonbondedForce(self, root):
        pass