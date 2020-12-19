
import os,sys
# # set the source code path
print(sys.path) # /home/roy/Work/emmm/test
print(__file__) # /home/roy/Work/emmm/test/test_h2o.py
print(os.path.dirname(os.path.dirname(__file__))) # /home/roy/Work/emmm

BASEPATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASEPATH)

import pytest


import emmm as em
world = em.World('real')

input = world.active_plugin('INlmpdat')


h2os = input.read_data(BASEPATH+'/test/h2o.lmpdat')