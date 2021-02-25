# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-14
# version: 0.0.2

import pytest
import mollab as ml


@pytest.fixture()
def a000():
    atom = ml.Atom()
    atom.position = (0, 0, 0)

    return atom


@pytest.fixture()
def a100():
    atom = ml.Atom()
    atom.position = (1, 0, 0)

    return atom

@pytest.fixture()
def a010():
    atom = ml.Atom()
    atom.position = (0, 1, 0)
    return atom

# # 构造测试数据
# # 默认为molecular型
# # field是字段
# # data 是数据

# @pytest.fixture()
# def atoms(request):
#     param = request.param

#     create = CreateAtom.genericAtom(param[2])

#     return create(*param)

# @pytest.fixture()
# def targetAtom(request):
#     param = request.param
#     create = CreateAtom.genericAtom(param[2])

#     return create(*param)

# @pytest.fixture()
# def atom000():
#     create = CreateAtom.molecularAtom
#     return create('atom', 'parent', 'molecular', 0, 0, 0)

# @pytest.fixture()
# def h2oWorld():
#     create = CreateAtom.molecularAtom
#     h1 = create('h1', 'parent','h', -1, 1, 0)
#     o = create('o', 'parent','o', 0, 0, 0)
#     h2 = create('h2', 'parent','h', 1, 1, 0)
#     o.add_linkedAtoms(h1, h2)
#     create = CreateMolecule.lmpMolecule
#     h2o = create('h2o', 'h2o', h1, o, h2)

#     world = World()
#     world.commet = 'h2o'
#     world.add_items(h2o)

#     world.set_bond('harmonic', 'h', 'o', k=1, r0=1)
#     world.set_angle('harmonic', 'h', 'o', 'h', k=1, theta=1)

#     world.update()

#     return world

# @pytest.fixture()
# def ch4World():
#     #          h1
#     #          |
#     #    h2----c----h4
#     #          |
#     #          h3
#     #
#     #   -1     0       1
#     #
#     #    centroid = (0, 0, 0)

#     create = CreateAtom.molecularAtom
#     h1 = create('h1', 'parent', 'h', 0, 1, 0)
#     h2 = create('h2', 'parent', 'h',-1, 0, 0)
#     h3 = create('h3', 'parent', 'h', 0,-1, 0)
#     h4 = create('h4', 'parent', 'h', 1, 0, 0)
#     c  = create('h1', 'parent', 'c', 0, 0, 0)
#     c.add_linkedAtoms(h1, h2, h3, h4)

#     create = CreateMolecule.lmpMolecule
#     ch4 = create('ch4', 'ch4', c, h1, h2, h3, h4)

#     world = World()
#     world.comment = ch4
#     world.add_items(ch4)
#     world.set_bond('harmonic', 'c', 'h', k=1, r0=1)
#     world.set_angle('harmonic', 'h', 'c', 'h', k=1, theta=1)
#     world.set_improper('harmonic', 'c', 'h', 'h', 'h', k=1, chi=1)
#     world.update()
#     return world

# @pytest.fixture()
# def c4World():

#     #        ch3h1   ch2h1   ch2h2   ch3h1
#     #          |       |       |       |
#     # ch3h2--ch3c----ch2c----ch2c----ch3c--ch3h2
#     #          |       |       |       |
#     #        ch3h3   ch2h2   ch2h2   ch3h3
#     #
#     #   -1     0       1       2       3     4
#     #
#     #    centroid = (1.5, 0, 0)

#     create = CreateAtom.molecularAtom
#     ch3h1 = create('ch3h1', 'parent','h', 0, 1, 0)
#     ch3h2 = create('ch3h2', 'parent','h', -1, 0, 0)
#     ch3h3 = create('ch3h3', 'parent','h', 0, -1, 0)
#     ch3c = create('ch3c', 'parent','c', 0, 0, 0)
#     ch3c.add_linkedAtoms(ch3h1, ch3h2, ch3h3)

#     ch2h1 = create('ch2h1', 'parent','h', 1, 1, 0)
#     ch2h2 = create('ch2h2', 'parent','h', 1, -1, 0)
#     ch2c = create('ch2c', 'parent','c', 1, 0, 0)
#     ch2c.add_linkedAtoms(ch2h1, ch2h2)

#     create = CreateMolecule.lmpMolecule
#     ch3head = create('ch3head', 'ch3', ch3h1, ch3h2, ch3h3, ch3c)
#     ch21 = create('ch2','ch2', ch2h1, ch2h2, ch2c)

#     ch3end = ch3head.get_replica('ch3end').rotate(1, 0,0,1).move(3,0, 0)
#     ch22 = ch21.get_replica('ch22').move(1,0,0)

#     ch3head['ch3c'].add_linkedAtoms(ch21['ch2c'])
#     ch21['ch2c'].add_linkedAtoms(ch22['ch2c'])
#     ch22['ch2c'].add_linkedAtoms(ch3end['ch3c'])

#     ch3ch2ch2ch3 = create('ch3ch2ch2ch3', 'pe', ch3head, ch21, ch22, ch3end)

#     world = World()
#     world.commet = 'CCCC'
#     world.add_items(ch3ch2ch2ch3)

#     world.set_bond('harmonic', 'c', 'c', k=1, r0=1)
#     world.set_bond('harmonic', 'c', 'h', k=1, r0=1)
#     world.set_angle('harmonic', 'c', 'c', 'c', k=1, theta=1)
#     world.set_angle('harmonic', 'h', 'c', 'c', k=1, theta=1)
#     world.set_angle('harmonic', 'h', 'c', 'h', k=1, theta=1)
#     world.set_dihedral('opls', 'c', 'c', 'c', 'c', k1=1,k2=2,k3=3,k4=4)
#     world.set_dihedral('opls', 'c', 'c', 'c', 'h', k1=1,k2=2,k3=3,k4=4)
#     world.set_dihedral('opls', 'h', 'c', 'c', 'h', k1=1,k2=2,k3=3,k4=4)
#     world.set_improper('cvff', 'c', 'c', 'c', 'h', k=1, d=1, n=1)
#     world.set_improper('cvff', 'c', 'c', 'h', 'h', k=1, d=1, n=1)
#     world.set_improper('cvff', 'c', 'h', 'h', 'h', k=1, d=1, n=1)

#     world.update()

#     return world

# @pytest.fixture()
# def buoy000():
#     create = CreateAtom.molecularAtom
#     return create('buoy000', 'parent','buoy', 0, 0, 0)

# @pytest.fixture()
# def buoy100():
#     create = CreateAtom.molecularAtom
#     return create('buoy000', 'parent', 'buoy', 1, 0, 0)
