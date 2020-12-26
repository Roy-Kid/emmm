# author: Roy Kid
# contact: lijichen365@126.com

from test.conftest import h2o
from emmm.core.create import Create
import pytest


# 构造测试数据
# field 为每一项的字段
# data 为字段对应的数据

raws = [
    {'label':'full', 'type':'full', 'q':0, 'x':0, 'y':0, 'z':0},
    {'label':'mol', 'type':'molecular', 'x':1, 'y':0, 'z':0}
]

# 测试部分
# 给出: [atom类型, atom字段, atom数据]
# 测试: 每新增一种atom的构造方法
# 预期: atom的属性和提供的数据一致

@pytest.fixture()
def setup_atom(request):
    param = request.param
    create = Create('atom', param['type'])
    if param['type'] == 'full':
        atom = create(param['label'], param['type'], param['q'], param['x'], param['y'], param['z'])
    elif param['type'] == 'molecular':
        atom = create(param['label'], param['type'], param['x'], param['y'], param['z'])
    
    return atom

@pytest.fixture()
def setup_field(request):
    return request.param


@pytest.mark.parametrize('setup_atom,setup_field', zip(raws, raws), indirect=True)
def test_full_atom(setup_atom, setup_field):
    for k,v in setup_field.items():
        assert getattr(setup_atom, k) == v





def test_h2o():
    create = Create('atom', 'molecular')
    h1 = create('h1', 'h', -1, 1, 0)
    o = create('o', 'o', 0, 0, 0)
    h2 = create('h2', 'h', 1, 1, 0)  
    create = Create('molecule', 'lmp')
    h2o = create('h2o', 'h2o', h1, o, h2)

    assert h2o['h1'].parent == 'h2o'
    assert h2o['h2'].parent == 'h2o'
    assert h2o['o'].parent == 'h2o'
    for atom in h2o.flatten():
        assert atom.path == 'h2o/'+ f'{atom.label}'
