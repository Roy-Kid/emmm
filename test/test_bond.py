# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-14
# version: 0.0.1

import pytest
import mollab as ml
import numpy as np

@pytest.fixture()
def b100(a000, a100):
    bond = ml.Bond(a000, a100)
    return bond

class TestBond:


    def test_length(self, b100):
        assert b100.length == 1

    def test_orient_vec(self, b100):
        assert (b100.orient_vec == np.array([-1, 0, 0])).all()

    def test_position(self, b100):
        assert (b100.position == np.array([0.5, 0, 0])).all()

    def test_bp(self, b100):
        assert 1

