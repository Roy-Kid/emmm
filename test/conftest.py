# author: Roy Kid
# contact: lijichen365@126.com

from emmm.core.create import CreateAtom, CreateMolecule
import emmm as em
import pytest


# 构造测试数据
# 默认为molecular型
# field是字段
# data 是数据

@pytest.fixture()
def atoms(request):
    param = request.param

    create = CreateAtom.genericAtom(param[1])

    return create(*param)

@pytest.fixture()
def targetAtom(request):
    param = request.param
    create = CreateAtom.genericAtom(param[1])

    return create(*param)

@pytest.fixture()
def atom000():
    create = CreateAtom.molecularAtom
    return create('atom', 'molecular', 0, 0, 0)

@pytest.fixture()
def h2o():
    create = CreateAtom.molecularAtom
    h1 = create('h1', 'h', -1, 1, 0)
    o = create('o', 'o', 0, 0, 0)
    h2 = create('h2', 'h', 1, 1, 0)  
    create = CreateMolecule.lmpMolecule
    h2o = create('h2o', 'h2o', h1, o, h2)

    return h2o

@pytest.fixture()
def pe():

    #        ch3h1   ch2h1   ch2h2   ch3h1
    #          |       |       |       |
    # ch3h2--ch3c----ch2c----ch2c----ch3c--ch3h2
    #          |       |       |       |
    #        ch3h3   ch2h2   ch2h2   ch3h3

    create = CreateAtom.molecularAtom
    ch3h1 = create('ch3h1', 'h', 0, 1, 0)
    ch3h2 = create('ch3h2', 'h', -1, 0, 0)
    ch3h3 = create('ch3h3', 'h', 0, -1, 0)
    ch3c = create('ch3c', 'c', 0, 0, 0)

    ch2h1 = create('ch2h1', 'h', 1, 1, 0)
    ch2h2 = create('ch2h2', 'h', 1, -1, 0)
    ch2c = create('ch2c', 'c', 1, 0, 0)

    create = CreateMolecule.lmpMolecule
    ch3head = create('ch3head', 'ch3', ch3h1, ch3h2, ch3h3, ch3c)
    ch21 = create('ch2', 'ch2', ch2h1, ch2h2, ch2c)

    ch3end = ch3head.get_replica('ch3end').rotate(180, 0,0,1).move(3,0, 0)
    ch22 = ch21.get_replica('ch22').move(1,0,0)

    ch3ch2ch2ch3 = create('ch3ch2ch2ch3', 'pe', ch3head, ch21, ch22, ch3end)

    return ch3ch2ch2ch3
    

@pytest.fixture()
def buoy000():
    create = CreateAtom.molecularAtom
    return create('buoy000', 'buoy', 0, 0, 0)

@pytest.fixture()
def buoy100():
    create = CreateAtom.molecularAtom
    return create('buoy000', 'buoy', 1, 0, 0)
