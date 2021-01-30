# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-29
# version: 0.0.1

import pytest

from emmm.core.potential import bond_potential_interface

def test_init():
    bp = bond_potential_interface('harmonic', typeName1=1, typeName2=2, coeffs={'k':1, 'r0':1})

    print(bp.energy(3)) 
    assert 0