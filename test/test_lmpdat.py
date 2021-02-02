# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from os import write
from emmm.core.world import World
import pytest

@pytest.fixture(scope='module')
def world():
    return World()

@pytest.fixture(scope='module')
def reader(world):
    print('init reader')
    reader = world.active_plugin('INlmpdat')
    reader = reader.read_data('test/benezen/lmp')

    world.masses = reader.massRaw
    # set bond coefficients
    for bc in reader.bondCoeffs:
        world.set_bond('harmonic', bc[0], bc[1], k=bc[2], r0=bc[3])

    for ac in reader.angleCoeffs:
        world.set_angle('harmonic', ac[0], ac[1], ac[2], k=ac[3], theta=ac[4])

    for dc in reader.dihedralCoeffs:
        world.set_dihedral('opls', *dc[:4], k1=dc[4], k2=dc[5], k3=dc[6], k4=dc[7])

    for ic in reader.improperCoeffs:
        world.set_improper('cvff', *ic[:4], k=ic[4], d=ic[5], n=ic[6])

    for pc in reader.pairCoeffs:
        world.set_pair('ljcut', pc[0], pc[1], epsilon=pc[2], sigma=pc[3])

    # add molecules
    world.add_items(reader.molecules)

    yield reader

@pytest.fixture(scope='module')
def writer(world, reader):
    writer = world.active_plugin('OUTlmpdat')
    world.update()
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

    def test_set_bond(self, reader, world):
        for bc in reader.bondCoeffs:
            bp = world.forcefield.get_bond(bc[0], bc[1])
            assert bp.k == 469.0 or bp.k == 367.0
            assert bp.r0 == 1.4 or bp.r0 == 1.08

    def test_set_angle(self, reader, world):
        for ac in reader.angleCoeffs:
            ap = world.forcefield.get_angle(ac[0], ac[1], ac[2])
            assert ap.k == 63 or ap.k == 35
            assert ap.theta0 == 120

    def test_set_dihedral(self, reader, world):
        for dc in reader.dihedralCoeffs:
            dp = world.forcefield.get_dihedral(*dc[:4])
            assert dp.k1 == 0
            assert dp.k2 == 7.25
            assert dp.k3 == 0
            assert dp.k4 == 0

    def test_set_improper(self, reader, world):
        for ic in reader.improperCoeffs:
            ip = world.forcefield.get_improper(*ic[:4])
            assert ip.k == 2.5
            assert ip.d == -1
            assert ip.n == 2

class TestOUTlmpdat:

    def test_commet(self, writer):
        assert writer.comment() == f'LAMMPS data from world1 Created by \n\n'

    def test_atomCount(self, writer):
        assert writer.atomCount() == f'\t  12  atoms\n'

    def test_bondCount(self, writer, world):
        assert writer.bondCount() == f'\t  12  bonds\n'

    def test_angleCount(self, writer, world):
        assert writer.angleCount() == f'\t  18  angles\n'

    def test_dihedralCount(self, writer, world):
        assert writer.dihedralCount() == f'\t  24  dihedrals\n\n'

    def test_improperCount(self, writer, world):
        assert writer.improperCount() == f'\t  6  impropers\n\n'

    def test_atomTypeCount(self, writer, world):
        assert writer.atomTypeCount() == f'\t  12  atom types\n'

    def test_bondTypeCount(self, writer, world):
        assert writer.bondTypeCount() == f'\t  12  bond types\n'

    def test_angleTypeCount(self, writer, world):
        assert writer.angleTypeCount() == f'\t  18  angle types\n'

    