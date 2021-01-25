# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from emmm.core.world import World
import pytest

@pytest.fixture(scope='module')
def reader():

    world = World()
    reader = world.active_plugin('INlmpdat')
    yield reader.read_data('test/benezen/lmp')

@pytest.fixture(scope='module')
def writer(reader):

    world = World()
    writer = world.active_plugin('OUTlmpdat')
    world.comment = reader['comment']
    world.atomCount = reader['atoms']
    world.bondCount = reader['bonds']
    world.angleCount = reader['angles']
    world.dihedralCount = reader['dihedrals']
    world.improperCount = reader['impropers']
    world.atomTypeCount = reader['atom types']
    world.bondTypeCount = reader['bond types']
    world.angleTypeCount = reader['angle types']
    world.dihedralTypeCount = reader['dihedral types']
    world.improperTypeCount = reader['improper types']
    world.xlo = reader['xlo']
    world.xhi = reader['xhi'] 
    world.ylo = reader['ylo']
    world.yhi = reader['yhi']
    world.zlo = reader['zlo']
    world.zhi = reader['zhi'] 

    world.masses = reader['Masses']


    yield (world, writer)


class TestINlmpdat:

    def test_system(self, reader):

        assert reader['atoms'] == 12
        assert reader['bonds'] == 12
        assert reader['angles'] == 18
        assert reader['dihedrals'] == 24
        assert reader['impropers'] == 6

        assert reader['atom types'] == 12
        assert reader['bond types'] == 12
        assert reader['angle types'] == 18
        assert reader['dihedral types'] == 24
        assert reader['improper types'] == 6

        assert reader['xlo'] == -2.177870
        assert reader['xhi'] == 47.822130
        assert reader['ylo'] == 0.998810
        assert reader['yhi'] == 50.998810
        assert reader['zlo'] == -0.941580
        assert reader['zhi'] == 49.058420

    def test_masses(self, reader):

        assert len(reader['Masses']) == 12

    def test_pair_coeffs(self, reader):

        assert len(reader['pair_coeffs']) == 12

    def test_bond_coeffs(self, reader):

        assert len(reader['bond_coeffs']) == 12
        assert reader['bond_coeffs'][0][0] == '1'
        assert reader['bond_coeffs'][-1][0] == '12'

    def test_angle_coeffs(self, reader):

        assert len(reader['angle_coeffs']) == 18

    def test_dihedral_coeffs(self, reader):

        assert len(reader['dihedral_coeffs']) == 24

    def test_improper_coeffs(self, reader):

        assert len(reader['improper_coeffs']) == 6

    def test_Atoms(self, reader):

        assert len(reader['Atoms']) == 12

    def test_Bonds(self, reader):

        assert len(reader['Bonds']) == 12

    def test_Angles(self, reader):
        assert len(reader['Angles']) == 18

    def test_Dihedral(self, reader):
        assert len(reader['Dihedrals']) == 24

    def test_Impropers(self, reader):
        assert len(reader['Impropers']) == 6

class TestOUTlmpdat:

    def test_commet(self, writer):
        assert writer[1].comment() == f'LAMMPS data from {writer[0].comment} Created by \n\n'

