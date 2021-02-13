# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-13
# version: 0.0.1

import pytest
import mollab as ml

@pytest.fixture(scope='module')
def xmlWorld():
    reader = ml.active_plugin('INxml')

    return reader.read('test/benezen/xml')