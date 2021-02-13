# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

import mollab as ml
import pytest


@pytest.fixture(scope='module')
def lmpWorld():
    reader = ml.active_plugin('INlmpdat')
    reader.atomStyle = 'full'
    reader.bondStyle = 'harmonic'
    reader.angleStyle = 'harmonic'
    reader.dihedralStyle = 'opls'
    reader.improperStyle = 'cvff'
    return reader.read('test/benezen/lmp')


class TestINlmpdat:

    def test_system(self, lmpWorld):

        assert lmpWorld.atomCount == 12
        assert lmpWorld.bondCount == 12
        assert lmpWorld.angleCount == 18
        assert lmpWorld.dihedralCount == 24
        assert lmpWorld.improperCount == 6

        assert lmpWorld.atomTypeCount == 12
        assert lmpWorld.bondTypeCount == 12
        assert lmpWorld.angleTypeCount == 18
        assert lmpWorld.dihedralTypeCount == 24
        assert lmpWorld.improperTypeCount == 6

        assert lmpWorld.xlo == -2.177870
        assert lmpWorld.xhi == 47.822130
        assert lmpWorld.ylo == 0.998810
        assert lmpWorld.yhi == 50.998810
        assert lmpWorld.zlo == -0.941580
        assert lmpWorld.zhi == 49.058420

    def test_mass(self, lmpWorld):

        assert len(lmpWorld.massRaw) == 12

    def test_pair_coeffs(self, lmpWorld):

        assert len(lmpWorld.pairCoeffs) == 12

    def test_bond_coeffs(self, lmpWorld):

        assert len(lmpWorld.bondCoeffRaw) == 12
        assert lmpWorld.bondCoeffRaw[0][0] == '1'
        assert lmpWorld.bondCoeffRaw[-1][0] == '12'

    def test_angle_coeffs(self, lmpWorld):

        assert len(lmpWorld.angleCoeffs) == 18

    def test_dihedral_coeffs(self, lmpWorld):

        assert len(lmpWorld.dihedralCoeffs) == 24

    def test_improper_coeffs(self, lmpWorld):

        assert len(lmpWorld.improperCoeffs) == 6

    def test_Atoms(self, lmpWorld):

        assert len(lmpWorld.atomRaw) == 12
        assert len(lmpWorld.atoms) == 12

    def test_Bonds(self, lmpWorld):

        assert len(lmpWorld.bondRaw) == 12

    def test_Angles(self, lmpWorld):
        assert len(lmpWorld.angleRaw) == 18

    def test_Dihedral(self, lmpWorld):
        assert len(lmpWorld.dihedralRaw) == 24

    def test_Impropers(self, lmpWorld):
        assert len(lmpWorld.improperRaw) == 6

    def test_set_bond(self, lmpWorld, world):
        for bc in lmpWorld.bondCoeffs:
            bp = world.forcefield.get_bond(bc[0], bc[1])
            assert bp.k == 469.0 or bp.k == 367.0
            assert bp.r0 == 1.4 or bp.r0 == 1.08

    def test_set_angle(self, lmpWorld, world):
        for ac in lmpWorld.angleCoeffs:
            ap = world.forcefield.get_angle(ac[0], ac[1], ac[2])
            assert ap.k == 63 or ap.k == 35
            assert ap.theta0 == 120

    def test_set_dihedral(self, lmpWorld, world):
        for dc in lmpWorld.dihedralCoeffs:
            dp = world.forcefield.get_dihedral(*dc[:4])
            assert dp.k1 == 0
            assert dp.k2 == 7.25
            assert dp.k3 == 0
            assert dp.k4 == 0

    def test_set_improper(self, lmpWorld, world):
        for ic in lmpWorld.improperCoeffs:
            ip = world.forcefield.get_improper(*ic[:4])
            assert ip.k == 2.5
            assert ip.d == -1
            assert ip.n == 2


class TestOUTlmpdat:
    def test_commet(self, writer):
        assert writer.comment() == 'LAMMPS data from world1 Created by \n\n'

    def test_atomCount(self, writer):
        assert writer.atomCount() == '\t  12  atoms\n'

    def test_bondCount(self, writer, world):
        assert writer.bondCount() == '\t  12  bonds\n'

    def test_angleCount(self, writer, world):
        assert writer.angleCount() == '\t  18  angles\n'

    def test_dihedralCount(self, writer, world):
        assert writer.dihedralCount() == '\t  24  dihedrals\n\n'

    def test_improperCount(self, writer, world):
        assert writer.improperCount() == '\t  6  impropers\n\n'

    def test_atomTypeCount(self, writer, world):
        assert writer.atomTypeCount() == '\t  12  atom types\n'

    def test_bondTypeCount(self, writer, world):
        assert writer.bondTypeCount() == '\t  12  bond types\n'

    def test_angleTypeCount(self, writer, world):
        assert writer.angleTypeCount() == '\t  18  angle types\n'

    def test_boundary(self, writer):
        bd = writer.boundary()
        assert bd[0] == '\t  -2.17787\t47.82213\txlo\txhi\n'
        assert bd[1] == '\t  0.99881\t50.99881\tylo\tyhi\n'
        assert bd[2] == '\t  -0.94158\t49.05842\tzlo\tzhi\n\n'

    def test_masses(self, writer):
        m = writer.masses()

        assert m[0] == f'Masses\n\n'
        assert m[-1] == f'\t{12}\t{1.008}\n'

    def test_pair_coeffs(self, writer):
        
        line = writer.pair_coeffs()
        assert line[0] == 'Pair Coeffs\n\n'
        assert line[1] == '\t\t1\t0.07\t3.55\n'
        assert line[2] == '\t\t2\t0.07\t3.55\n'
        assert line[-1] == '\t\t12\t0.03\t2.42\n'

    def test_bond_coeffs(self, writer):

        line = writer.bond_coeffs()
        assert line[0] == 'Bond Coeffs\n\n'
        assert line[1] == '\t\t1\t469.0\t1.4\n'
        assert line[2] == '\t\t2\t469.0\t1.4\n'
        assert line[-1] == '\t\t12\t469.0\t1.4\n'

    def test_angle_coeffs(self, writer):

        line = writer.angle_coeffs()
        assert line[0] == 'Angle Coeffs\n\n'
        assert line[1] == '\t\t1\t63.0\t120.0\n'
        assert line[-1]== '\t\t18\t35.0\t120.0\n'

    def test_dihedral_coeffs(self, writer):

        line = writer.dihedral_coeffs()
        assert line[0] == 'Dihedral Coeffs\n\n'
        assert line[1] == '\t\t1\t0.0\t7.25\t0.0\t0.0\n'
        assert line[-1]== '\t\t24\t0.0\t7.25\t0.0\t0.0\n'

    def test_improper_coeffs(self, writer):
        line = writer.improper_coeffs()
        assert line[0] == 'Improper Coeffs\n\n'
        assert line[1] == '\t\t1\t2.5\t-1\t2.0\n'
        assert line[-1] == '\t\t6\t2.5\t-1\t2.0\n'

    def test_Atoms(self, writer):
        line = writer.Atoms()
