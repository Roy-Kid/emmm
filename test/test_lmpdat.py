# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from emmm.core.world import World
import pytest

class TestLMPDAT:

    @pytest.fixture(scope='class')
    def reader(self):

        world = World()
        reader = world.active_plugin('INlmpdat')
        yield reader.read_data('test/benezen/lmp')

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