# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

import mollab as ml
import pytest


@pytest.fixture(scope='module')
def lmpWorld():
    reader = ml.plugins.INlmpdat()
    reader.atomStyle = 'full'
    reader.bondStyle = 'harmonic'
    reader.angleStyle = 'harmonic'
    reader.pairStyle = 'lj126'
    reader.dihedralStyle = 'opls'
    reader.improperStyle = 'cvff'

    world = reader.read('test/benezen/lmp')

    world.topo.search_topo()

    return world

@pytest.fixture(scope='module')
def lmpOut(lmpWorld):
    writer = ml.plugins.OUTlmpdat()
    writer.world = lmpWorld

    return writer



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
        print(lmpWorld.atoms[0])
        assert lmpWorld.atoms[0].mass == 12.011

    def test_pair_coeffs(self, lmpWorld):

        assert len(lmpWorld.forcefield.pairPotentialList) == 12

    def test_bond_coeffs(self, lmpWorld):

        assert len(lmpWorld.forcefield.bondPotentialList) == 12

    def test_angle_coeffs(self, lmpWorld):

        assert len(lmpWorld.forcefield.anglePotentialList) == 18

    def test_dihedral_coeffs(self, lmpWorld):

        assert len(lmpWorld.forcefield.dihedralPotentialList) == 24

    def test_improper_coeffs(self, lmpWorld):

        assert len(lmpWorld.forcefield.improperPotentialList) == 6

    def test_Atoms(self, lmpWorld):

        assert len(lmpWorld.atoms) == 12

    def test_Bonds(self, lmpWorld):

        assert len(lmpWorld.topo.bonds) == 12

    def test_Angles(self, lmpWorld):
        assert len(lmpWorld.topo.angles) == 18

    def test_Dihedral(self, lmpWorld):
        assert len(lmpWorld.topo.dihedrals) == 24

    def test_Impropers(self, lmpWorld):
        assert len(lmpWorld.topo.impropers) == 6

    def test_set_bond(self, lmpWorld):
        for b in lmpWorld.topo.bonds:
            assert (b.bp.k == 469.0 or b.bp.k == 367.0) or (b.bp.r0 == 1.08
                                                            or b.bp.r0 == 1.40)

    def test_set_angle(self, lmpWorld):
        for a in lmpWorld.topo.angles:
            assert a.ap.lmp_format == [63.0, 120] or a.ap.lmp_format == [35.0, 120.0]

    # def test_set_dihedral(self, lmpWorld):
    #     for d in lmpWorld.topo.dihedrals:
    #         assert d.dp.lmp_format == [0.0, 7.25, 0.0, 0.0]

    # def test_set_improper(self, lmpWorld, world):
    #     for ic in lmpWorld.improperCoeffs:
    #         ip = world.forcefield.get_improper(*ic[:4])
    #         assert ip.k == 2.5
    #         assert ip.d == -1
    #         assert ip.n == 2


class TestOUTlmpdat:
    def test_commet(self, lmpOut):
        assert lmpOut.comment()

    def test_atomCount(self, lmpOut):
        assert lmpOut.atomCount() == '\t  12  atoms\n'

    def test_bondCount(self, lmpOut):
        assert lmpOut.bondCount() == '\t  12  bonds\n'

    def test_angleCount(self, lmpOut):
        assert lmpOut.angleCount() == '\t  18  angles\n'

    def test_dihedralCount(self, lmpOut):
        assert lmpOut.dihedralCount() == '\t  24  dihedrals\n\n'

    def test_improperCount(self, lmpOut):
        assert lmpOut.improperCount() == '\t  6  impropers\n\n'

    def test_atomTypeCount(self, lmpOut):
        assert lmpOut.atomTypeCount() == '\t  12  atom types\n'

    def test_bondTypeCount(self, lmpOut):
        assert lmpOut.bondTypeCount() == '\t  12  bond types\n'

    def test_angleTypeCount(self, lmpOut):
        assert lmpOut.angleTypeCount() == '\t  18  angle types\n'

    def test_boundary(self, lmpOut):
        bd = lmpOut.boundary()
        assert bd[0] == '\t  -2.17787\t47.82213\txlo\txhi\n'
        assert bd[1] == '\t  0.99881\t50.99881\tylo\tyhi\n'
        assert bd[2] == '\t  -0.94158\t49.05842\tzlo\tzhi\n\n'

    def test_masses(self, lmpOut):
        m = lmpOut.masses()

        assert m[0] == f'Masses\n\n'
        assert m[-1] == f'\t{12}\t{1.008}\n'

    def test_pair_coeffs(self, lmpOut):

        line = lmpOut.pair_coeffs()
        assert line[0] == 'Pair Coeffs\n\n'
        assert line[1] == '\t\t1\t0.07\t3.55\n'
        assert line[2] == '\t\t2\t0.07\t3.55\n'
        assert line[-1] == '\t\t12\t0.03\t2.42\n'

    def test_bond_coeffs(self, lmpOut):

        line = lmpOut.bond_coeffs()
        assert line[0] == 'Bond Coeffs\n\n'
        assert line[1] == '\t\t1\t469.0\t1.4\n'
        assert line[2] == '\t\t2\t469.0\t1.4\n'
        assert line[-1] == '\t\t12\t469.0\t1.4\n'

    def test_angle_coeffs(self, lmpOut):

        line = lmpOut.angle_coeffs()
        assert line[0] == 'Angle Coeffs\n\n'
        assert line[1] == '\t\t1\t63.0\t120.0\n'
        assert line[-1] == '\t\t18\t35.0\t120.0\n'

    def test_dihedral_coeffs(self, lmpOut):

        line = lmpOut.dihedral_coeffs()
        assert line[0] == 'Dihedral Coeffs\n\n'
        assert line[1] == '\t\t1\t0.0\t7.25\t0.0\t0.0\n'
        assert line[-1] == '\t\t24\t0.0\t7.25\t0.0\t0.0\n'

    def test_improper_coeffs(self, lmpOut):
        line = lmpOut.improper_coeffs()
        assert line[0] == 'Improper Coeffs\n\n'
        assert line[1] == '\t\t1\t2.5\t-1\t2.0\n'
        assert line[-1] == '\t\t6\t2.5\t-1\t2.0\n'

    def test_Atoms(self, lmpOut):
        line = lmpOut.Atoms()
        assert line[0] == 'Atoms\n\n'
        assert line[1] == f'\t{1}\t{1}\t{1}\t{-0.1474}\t{1.0}\t{1.0}\t{0.0}\n'

    def test_Bonds(self, lmpOut):
        line = lmpOut.Bonds()
        assert line[0] == 'Bonds\n\n'
        assert line[1] == '\t1\t1\t1\t2\n'
        assert line[2] == '\t2\t5\t1\t6\n'
        assert len(line) == 12 + 2
