# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-13
# version: 0.0.1
import numpy as np
# class A(ndarray):

#     def __new__(cls, *shape):
        
#         return super().__new__(cls, shape, np.int64)

#     def __init__(self, *shape) -> None:
#         self.point = dict()
#         for i in range(self.size):
#             l = list()
#             self.point[id(l)] = l
#         self[::] = np.array(list(self.point.keys())).reshape(shape)

#     def __getitem__(self, key):
#         temp = super().__getitem__(key)
#         if isinstance(temp, np.int64):
#             return self.point[temp]
#         else:
#             return temp
       

# n = A(2,2)
# print(n[0][1], type(n[0][1]))

# from copy import deepcopy
# class ndlist(list):

#     def __init__(self, *dim):
        
#         self._ndlist = list()
#         self.dim = dim
#         self.ndim = len(dim)
#         d = 0
#         self._append_list(0, [self._ndlist])

#     def _append_list(self, d, ls):
        
#         lss = [list() for i in range(self.dim[d])]
#         for l in ls:
#             lsss = deepcopy(lss)
#             l.extend(lsss)
#             if d+1 < self.ndim:
#                 self._append_list(d+1, lsss)

#     @property
#     def shape(self):
#         if not getattr(self, '_shape', None):
#             shape = list()
#             ndlist = self._ndlist
#             d = 0
#             while d < self.ndim:
#                 shape.append(len(ndlist))
#                 ndlist = ndlist[0]
#                 d += 1
#             self._shape = tuple(shape)
#         return self._shape

#     def __str__(self):
#         return f'< ndlist with {1}x{1} shape>'

class ndarray:

    def __init__(self, x, y, z):

        self.d = dict()
        
        for i in range(x*y*z):
            l = list()
            idl = id(l)
            self.d[idl] = l
        
        self.a = np.fromiter(self.d.keys(), dtype=np.int64).reshape((x, y, z))

    def get(self, x, y, z):
        return self.d[self.a[x][y][z]]