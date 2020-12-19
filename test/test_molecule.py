from emmm.core.create import Create
import numpy as np
import emmm as em
import pytest
import os
import sys
# # set the source code path

BASEPATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASEPATH)

class TestMOLECULE:

    @pytest.fixture
    def molecule(self):
        atom0 = Create.create_full_atom('atom')