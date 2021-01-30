# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from emmm.core.utils import assignId
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
    world.comment = reader.comment
    world.atomCount = reader.atomCount
    world.bondCount = reader.bondCount
    world.angleCount = reader.angleCount
    world.dihedralCount = reader.dihedralCount
    world.improperCount = reader.improperCount
    world.atomTypeCount = reader.atomTypeCount
    world.bondTypeCount = reader.bondTypeCount
    world.angleTypeCount = reader.angleTypeCount
    world.dihedralTypeCount = reader.dihedralTypeCount
    world.improperTypeCount = reader.improperTypeCount
    world.xlo = reader.xlo
    world.xhi = reader.xhi
    world.ylo = reader.ylo
    world.yhi = reader.yhi
    world.zlo = reader.zlo
    world.zhi = reader.zhi

    world.masses = reader.masses

    writer.world = world

    yield writer


class TestINlmpdat:

    def test_system(self, reader):

        assert reader.atomCount == 12
        assert reader.bondCount == 12
        assert reader.angleCount == 18
        assert reader.dihedralCount == 24
        assert reader.improperCount == 6

        assert reader.atomTypeCount == 12
        assert reader.bondTypeCount == 12
        assert reader.angleTypeCount == 18
        assert reader.dihedralTypeCount == 24
        assert reader.improperTypeCount == 6

        assert reader.xlo == -2.177870
        assert reader.xhi == 47.822130
        assert reader.ylo== 0.998810
        assert reader.yhi == 50.998810
        assert reader.zlo == -0.941580
        assert reader.zhi == 49.058420

    def test_mass(self, reader):

        assert len(reader.massRaw) == 12

    def test_pair_coeffs(self, reader):

        assert len(reader.pairCoeffs) == 12


    def test_bond_coeffs(self, reader):

        assert len(reader.bondCoeffRaw) == 12
        assert reader.bondCoeffRaw[0][0] == '1'
        assert reader.bondCoeffRaw[-1][0] == '12'

    def test_angle_coeffs(self, reader):

        assert len(reader.angleCoeffs) == 18

    def test_dihedral_coeffs(self, reader):

        assert len(reader.dihedralCoeffs) == 24

    def test_improper_coeffs(self, reader):

        assert len(reader.improperCoeffs) == 6

    def test_Atoms(self, reader):

        assert len(reader.atomRaw) == 12
        assert len(reader.atoms) == 12

    def test_Bonds(self, reader):

        assert len(reader.bondRaw) == 12

    def test_Angles(self, reader):
        assert len(reader.angleRaw) == 18

    def test_Dihedral(self, reader):
        assert len(reader.dihedralRaw) == 24

    def test_Impropers(self, reader):
        assert len(reader.improperRaw) == 6

class TestOUTlmpdat:

    def test_commet(self, writer, reader):
        assert writer.comment() == f'LAMMPS data from {reader.comment} Created by \n\n'

