import pytest

class TestMOLECULE:


    # create = Create('atom', 'molecular')
    # h1 = create('h1', 'h', -1, 1, 0)
    # o = create('o', 'o', 0, 0, 0)
    # h2 = create('h2', 'h', 1, 1, 0)  
    # create = Create('molecule', 'lmp')
    # h2o = create('h2o', 'h2o', h1, o, h2)

    def test_h2o_move(self, h2o):
        h2o.move(1,2,3)
        assert all(h2o['h1'].position == (0,3,3))
        assert all(h2o['o'].position == (1,2,3))
        assert all(h2o['h2'].position == (2,3,3))

    def test_h2o_centroid(self, h2o):
        assert all(h2o.position == (0, 2/3, 0))

    def test_h2o_coords(self, h2o):

        assert all(h2o.coords[0] == (-1, 1, 0))
        assert all(h2o.coords[1] == (0, 0, 0))
        assert all(h2o.coords[2] == (1, 1, 0))


    def test_h2o_distance(self, h2o, buoy000, buoy100):

        assert h2o.distance_to(buoy000) == 2/3
        assert h2o.distance_to(buoy100) == 13**0.5/3

    def test_h2o_rotate(self, h2o):


        h2o.rotate(1, 0, 0, 1, 0, 0, 0)

        # [[1, -1, 0],
        #  [0, 0, 0],
        #  [-1, -1, 0]]

        assert all( (0.99 < h2o.coords[0][0] < 1,
                    -1.01 < h2o.coords[0][1] < -0.99,
                     h2o.coords[0][2] == 0) )

        assert all( (-0.01 < h2o.coords[1][0] < 0.01,
                    -0.01 < h2o.coords[1][1] < 0.01,
                     -0.01 < h2o.coords[1][2] < 0.01) )

        assert all( (-1.01 < h2o.coords[2][0] < -0.99,
                    -1.01 < h2o.coords[2][1] < -0.99,
                    -0.01 < h2o.coords[2][2] < 0.01) )

    def test_h2o_get_replica(self, h2o):

        h2o0 = h2o.get_replica('h2o0')
        assert all(h2o['h1'].position == (-1, 1, 0))
        assert all(h2o0['h1'].position == (-1, 1, 0))       
        assert id(h2o['h1']) != id(h2o0['h1'])

        h2o0.move(1,1,1)
        assert all(h2o['h1'].position == (-1, 1, 0))
        assert all(h2o0['h1'].position == (0, 2, 1)) 


    def test_h2o_seperate_with(self, h2o):
        h2o0 = h2o.get_replica('h2o0').move(0,1,0)
       
        h2o0.seperate_with(h2o, 'abs', 3)

        assert h2o.position[1] == 2/3-3
        assert h2o['o'].position[1] == -3
        assert h2o0.position[1] == 2/3+4
        assert h2o0['o'].position[1] == 4

    def test_h2o_rotate_orth(self, h2o):
        h2o.rotate_orth(1, 0, 0, 0, 0, 0, 1)
        assert round(h2o['h1'].position[0]) == 1
        assert round(h2o['h1'].position[1]) == -1
        assert round(h2o['h1'].position[2]) == 0
        assert round(h2o['o'].position[0]) == 0
        assert round(h2o['o'].position[1]) == 0
        assert round(h2o['o'].position[2]) == 0
        assert round(h2o['h2'].position[0]) == -1
        assert round(h2o['h2'].position[1]) == -1
        assert round(h2o['h2'].position[2]) == 0

### end h2o test ###
### start poly test ###

    def test_pe_move(self, pe):

        pe.move(0,0,3)
        for atom in pe.flatten():
            assert atom.position[2] == 3

        for mol in pe:
            assert mol.position[2] == 3

    def test_pe_centroid(self, pe):
        for atom in pe.flatten():
            print(atom)

        assert pe.position[0] == 2.5

    def test_pe_distance(self, pe, buoy000):
        print(pe.distance_to(buoy000))
        assert pe.distance_to(buoy000) == 2.5

    def test_pe_get_replica(self, pe):
        pe0 = pe.get_replica('pe0')
        

    