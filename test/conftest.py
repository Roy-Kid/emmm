# author: Roy Kid
# contact: lijichen365@126.com
from _pytest.config import exceptions
from _pytest.mark import param
from attr import field
from emmm.core.create import Create, CreateAtomFull
import pytest


# 构造测试数据
# 默认为molecular型
# field是字段
# data 是数据

@pytest.fixture()
def atoms(request):
    param = request.param
    create = Create('atom', param[1])

    return create(*param)

@pytest.fixture()
def targetAtom(request):
    param = request.param
    create = Create('atom', param[1])

    return create(*param)

@pytest.fixture()
def h2o():
    create = Create('atom', 'molecular')
    h1 = create('h1', 'h', -1, 1, 0)
    o = create('o', 'o', 0, 0, 0)
    h2 = create('h2', 'h', 1, 1, 0)  
    create = Create('molecule', 'lmp')
    h2o = create('h2o', 'h2o', h1, o, h2)

    return h2o

@pytest.fixture()
def buoy000():
    create = Create('atom', 'molecular')
    return create('buoy000', 'buoy', 0, 0, 0)

@pytest.fixture()
def buoy100():
    create = Create('atom', 'molecular')
    return create('buoy000', 'buoy', 1, 0, 0)
