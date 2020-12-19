from emmm.core.create import Create
import numpy as np
import emmm as em
import pytest
import os
import sys
# # set the source code path

BASEPATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASEPATH)


class TestATOM:

    @pytest.fixture
    def atom000(self):
        return Create.create_full_atom('atom000', None, 'test', 0, 0, 0, 0)

    @pytest.fixture
    def atom111(self):
        return Create.create_full_atom('atom111', None, 'test', 0, 1, 1, 1)

    @pytest.fixture
    def atom100(self):
        return Create.create_full_atom('atom100', None, 'test', 0, 1, 0, 0)

    def test_atom_properties(self, atom000):

        # create 将以下三个转换为str
        assert atom000.label == 'atom000'
        assert atom000.parent == 'None'
        assert atom000.type == 'test'

        # create 将一下三个转换为float
        assert atom000.q == 0
        assert atom000.x == 0
        assert atom000.y == 0
        assert atom000.z == 0

    def test_move(self, atom000):

        atom000.move(1, 2, 3)
        assert all(atom000.position == [1, 2, 3])

    def test_add_neighbors(self, atom000, atom111):

        ## atom1 = Create.create_full_atom('neighbor', None, 'neigh', 0, 1, 2, 3)

        atom000.add_neighbors(atom111)

        assert atom000.get_neighbors()[0].label == 'atom111'
        assert atom111.get_neighbors()[0].label == 'atom000'

        # with

    def test_distance(self, atom000, atom111):

        assert 1.73 < atom000.distance_to(atom111) < 1.74  # sqrt(3)

    def test_get_replica(self, atom000):
        atom00 = atom000.get_replica('atom00')

        assert atom00.id != atom000.id

        del atom000.__dict__['_Item__id']
        del atom00.__dict__['_Item__id']
        assert atom00.__dict__ == atom000.__dict__

    def test_seperate_abs(self, atom000, atom100):
        atom000.seperate_with(atom100, 'abs', 3)
        assert all(atom000.position == [-3, 0, 0])
        assert all(atom100.position == [4, 0, 0])

    def test_seperate_rel(self, atom000, atom100):
        atom000.seperate_with(atom100, 'rel', 3)
        assert all(atom000.position == [-3, 0, 0])
        assert all(atom100.position == [4, 0, 0])

    def test_randmove(self, atom000):
        o = atom000.position

        atom000.randmove(5)
        p = atom000.position

        print(o, p)
        assert round(np.linalg.norm(o-p)) == 5

    @pytest.fixture
    def atom(self, request):
        request = request.param
        return Create.create_full_atom('atom'+str(request), None, 'test', 0, int(request[0]), int(request[1]), int(request[2]))

    @pytest.fixture
    def ex(self, request):
        request = request.param
        return request
    # 000是坐标, [0,0,0]是预期值. 照着抄就完事了
    data = [('000', [0, 0, 0]), ('100', [0, 1, 0]), ('111', [-1, 1, 1])]

    @pytest.mark.parametrize('atom, ex', data, indirect=True)
    def test_rotate(self, atom, ex):
        atom.rotate(0.5, 0, 0, 1)
        assert round(atom.position[0], 2) == ex[0]
        assert round(atom.position[1], 2) == ex[1]
        assert round(atom.position[2], 2) == ex[2]


# # 一个装饰器+多个fixture
# @pytest.fixture(scope="module")
# def getusername(request):
#     username = request.param
#     print(f" username is {username}")
#     return username

# @pytest.fixture(scope="module")
# def getpassword(request):
#     password = request.param
#     print(f" password is {password}")
#     return password

# data = [("jojo", "1"), ("lilei", "123654")]

# @pytest.mark.parametrize("getusername,getpassword", data, indirect=True)
# def test_getUserinfo(getusername, getpassword):
#     print(f"用户名：{getusername} 密码：{getpassword}")
