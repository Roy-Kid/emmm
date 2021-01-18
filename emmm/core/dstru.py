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
        """ 递归函数, 从内层向外构建

        Args:
            depth ([type]): [description]

        Returns:
            [type]: [description]
        """
        if depth < self.ndim: 
            # 在没有探到最底层之前, 一直向下
            # 探到最底层之后: 
            # 首先先返回一个默认值ivalue
            # 从第二层开始返回list
            aix = self._dive( depth+1 ) # 顺序: 1| 递归

            aix = [deepcopy(aix) for i in range(self.shape[depth])] # 顺序: 3| 按照shape扩充到指定长度

            return aix
        # -- return --
        if depth == self.ndim:
            return self.ivalue # 顺序: 2| 探到最底层返回默认值

    def __getitem__(self, index):
        return self.ndarray[index]

    @property
    def inlist(self):
        return self.ndarray

    def symetry_assign(self, value, *keys):
        """以对称的方式向多位数组中赋值. e.g.:(a,b,c)==(b,c,a)==(c,a,b)==value


        Args:
            value (Any): 值

        Raises:
            KeyError: 键的数目与维度数量不相符时

        """
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

    def reshape(self, shape):
        """ 改变多维数组的形状

        Args:
            shape ([type]): [description]
        """
        pass

    def _grow(self):
        """TODO: 重要. 当数组大小不满足当前要求, 自动扩充数组大小. 例如(16, 16)的数组充满之后, 应该新建一个(32,32)的数组, 然后将原有数组复制到新数组中. 
        """