# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1

from mollab.plugins.input.input_base import InputBase
from mollab.core.world import World
import xml.etree.ElementTree as ET


class INxml(InputBase):

    def read(self, fname, world=None):

        tree = ET.parse(fname)
        
        if world:
            self.world = World()

        else:
            self.world = world
            post_process = self._process_with_world

        root = tree.getroot()

        for child in root:

            executor = getattr(self, child.tag, self.status_error)

            executor(child)

        post_process()

    def _process_with_world(self):

        for atom in self.world.atoms:
            residue = self.Residues[atom.resName]
            for r in residue:
                if atom.name == r['name']:
                    for t in self.AtomTypes:
                        if r['type'] == t['name']:
                            atom.type = t['class']
                            atom.element = t['element']
                            atom.mass = t['mass']

        self.set_bond()
           

    def status_error(self, root):
        raise Exception(f'unknown tag {root.tag}')

    def AtomType(self, root):
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
            self.world.set_bond('harmonic', bc['class1'], bc['class2'], bc['length'], bc['k'])

    def HarmonicAngleForce(self, root):

        for ac in root:

            self.world.set_angle('harmonic', ac['class1'], ac['class2'], ac['class3'], ac['angle'], ac['k'])

    def PeriodicTorsionForce(self, root):
        pass
