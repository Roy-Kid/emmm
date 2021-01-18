from copy import deepcopy

from itertools import permutations

class ndarray:

    def __init__(self, shape, ivalue=0) -> None:
        self.shape = shape
        self.ndim = len(shape)
        self.ivalue = ivalue

        self.ndarray = self._dive( depth=0 )

        self._str = str()

    def __repr__(self) -> str:
        return f"<ndarray with shape {self.shape}>"

    def __str__(self) -> str:
        return str(self.ndarray)

    def _dive(self, depth):

        if depth < self.ndim: # depth==1 aix==ivalue
            aix = self._dive( depth+1 )
            aix = [deepcopy(aix) for i in range(self.shape[depth])]

            return aix
        # -- return --
        if depth == self.ndim:
            return self.ivalue

    def __getitem__(self, index):
        return self.ndarray[index]

    @property
    def inlist(self):
        return self.ndarray

    def symetry_assign(self, value, *keys):
        if len(keys) != self.ndim:
            raise KeyError('key的数目与维数不符, 无法对称添加')
        
        def _symetry_assign(value, key, ndarray):
            if not isinstance(ndarray[key], list):
                ndarray[key] = value
            else:
                return ndarray[key]

        for key in permutations(keys):
            ndarray = self.ndarray
            for ke in key:
                ndarray = _symetry_assign(value, ke, ndarray)

    def assign(self, value, *keys):

        def _assign(value, key, ndarray):
            if not isinstance(ndarray[key], list):
                ndarray[key] = value
            else:
                return ndarray[key]

        ndarray = self.ndarray
        for key in keys:
            ndarray = _assign(value, key, ndarray)
