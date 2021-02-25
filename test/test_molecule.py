# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-25
# version: 0.0.1

from mollab.core.molecule import Molecule
import pytest

@pytest.fixture()
def mol(a000, a100, a010):
    molecule = Molecule()
    molecule.add_items(a000, a010, a100)
    return molecule

class TestMolecule:

    def test_save_dict(self, mol):
        print(mol.save_dict())
