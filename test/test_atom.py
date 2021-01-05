
import pytest


class TestAtom:

    data = [
        ['atom000', 'full', 0, 0, 1, 0],
        ['atom100', 'molecular', 1, 0, 0],
    ]

    @pytest.mark.parametrize('atoms', data, indirect=True)
    def test_atom_move(self, atoms):

        atom = atoms
        x = atom.x+1
        y = atom.y+1
        z = atom.z+1

        atom.move(1,1,1)
        position = (x, y, z)
        assert all(atom.position == position)

    tData = [
        ['atom100', 'molecular', 1, 0, 0],        
        ['atom000', 'full', 0, 0, 1, 0],
    ]
    exception = [1.414, 1.414]

    @pytest.mark.parametrize('atoms, targetAtom, exception', zip(data,tData,exception) , indirect=['atoms', 'targetAtom'])
    def test_distance(self, atoms, targetAtom, exception):


        assert round(atoms.distance_to(targetAtom), 3) == exception


    @pytest.mark.parametrize('atoms', data, indirect=True)
    def test_get_replica(self, atoms):

        aa = atoms.get_replica('aa')
        assert all(aa.position == atoms.position)
        assert id(aa.position) != id(atoms.position)

        assert aa.id != atoms.id

    data = [
        ['atom000', 'full', 0, 0, 0, 0]
    ]

    tData = [
        ['atom100', 'full', 0, 2, 0, 0]
    ]


    exception = [
        ([-3, 0, 0], [5, 0, 0])
    ]

    @pytest.mark.parametrize('atoms, targetAtom, exception', zip(data, tData, exception), indirect=['atoms', 'targetAtom'])
    def test_seperate_abs(self, atoms, targetAtom, exception):



        if all(atoms.position == targetAtom.position):
            with pytest.raises(ValueError):
                atoms.seperate_with(targetAtom, 'abs', 3)
        else:
            atoms.seperate_with(targetAtom, 'abs', 3)

            assert all(atoms.position == exception[0])
            assert all(targetAtom.position == exception[1])


    data = [
        ['atom000', 'full', 0, 0, 0, 0]
    ]

    tData = [
        ['atom100', 'full', 0, 2, 0, 0]
    ]


    exception = [
        ([-2, 0, 0], [4, 0, 0])
    ]


    @pytest.mark.parametrize('atoms, targetAtom, exception', zip(data, tData, exception), indirect=['atoms', 'targetAtom'])
    def test_seperate_rel(self, atoms, targetAtom, exception):
        if all(atoms.position == targetAtom.position):
            with pytest.raises(ValueError):
                atoms.seperate_with(targetAtom, 'rel', 3)
        else:
            atoms.seperate_with(targetAtom, 'rel', 3)

            assert all(atoms.position == exception[0])
            assert all(targetAtom.position == exception[1])


    data = [
        ['atom-110', 'full', 0, -1, 1, 0],
        ['atom000', 'molecular', 0, 0, 0],
        ['atom110', 'molecular', 1, 1, 0]
    ]

    rotate = [
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ]

    exception = [
        [1, -1, 0],
        [0, 0, 0],
        [-1, -1, 0]
    ]

    @pytest.mark.parametrize('atoms, rotate, exception', zip(data, rotate, exception), indirect=['atoms'])
    def test_rotate(self, atoms, rotate, exception):
        atoms.rotate(1, *rotate)
        print(atoms.position)
        assert round(atoms.position[0])==exception[0]
        assert round(atoms.position[1])==exception[1]
        assert round(atoms.position[2])==exception[2]



    data = [
        ['atom010', 'molecular', 0, 1, 0], 

    ]
    exception = [
        [0, 3, 0],

    ]

    @pytest.mark.parametrize('atoms, exception', zip(data, exception), indirect=['atoms'])
    def test_rotate_orth(self, atoms, exception):
        atoms.rotate_orth(1, 0, 2, 0, 0, 0, 1)
        print(atoms.position)
        assert round(atoms.position[0])==exception[0]
        assert round(atoms.position[1])==exception[1]
        assert round(atoms.position[2])==exception[2]        

    
    data = [
        ['atom000', 'molecular', 0, 0, 0],
        ['atom100', 'molecular', 1, 0, 0],
        ['atom110', 'molecular', 1, 1, 0]  
    ]

    targetAtom = [
        ['atom000', 'molecular', 0, 0, 0],
        ['atom010', 'molecular', 0, 1, 0],
        ['atom111', 'molecular', 1, 1, 1]          
    ]

    exception = [0, 2**0.5, 1]

    @pytest.mark.parametrize('atoms, targetAtom, exception', zip(data, targetAtom, exception), indirect=['atoms', 'targetAtom'])
    def test_distance(self, atoms, targetAtom, exception):
        dist = atoms.distance_to(targetAtom)
        assert dist == exception

    def test_duplicate(self, atom000):
        atoms = atom000.duplicate(3, 1, 0, 0).duplicate(3, 0, 1, 0)
