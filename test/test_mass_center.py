import mollab as ml
import pytest

@pytest.fixture()
def initWorld():
    reader = ml.plugins.INlmpdat()

    world = reader.read('test/scripts/data.lmps', {'atomStyle': 'full'})
    return world

def test_mass_center(initWorld):

    for mol in initWorld.molecules:
        print(mol.position)

    writer = ml.plugins.OUTlmpdat()
    writer.write_data('test.lmp', initWorld)
