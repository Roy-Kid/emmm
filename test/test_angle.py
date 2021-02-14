# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-14
# version: 0.0.1

import pytest
import mollab as ml
import numpy as np


@pytest.fixture()
def angle(a100, a000, a010):
    angle = ml.Angle(a100, a000, a010)
    return angle


class TestAngle:
    def test_angle(self, angle):
        assert angle.angle == 90