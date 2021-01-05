上手
########

生成
********
整个软件的核心是 ``Atom`` 和 ``Molecule`` 两个类. 这两个类中储存了所有的数据, 其他一切的模块都是对这两个类的读取和操作.

``Atom`` 和 ``Molecule`` 统称为 ``Item``. 一个 ``Molecule`` 可以储存多个 ``Atom`` 形成一个初级结构, 可以储存多个 ``Molecule`` 形成更高一级的结构, 也可以混合储存这两种 ``Item`` . ``Item`` 可以看作空间中的一个实体, 都可以进行 ``move`` 平移, ``rotate`` 旋转等单元操作, 也可以使用 ``seperate_with`` 和其他 ``Item`` 相分离, ``distance_to`` 测量距离这样的二元操作. 

这个软件的使用思路应该是自下向上, 我们先生成 `Atom`, 再将其储存在 `Molecule` 中, 层层向上.

`Atom` 储存每个原子单元的信息. 生成每个 `Atom` 应该使 `Create` 类, 这样就可以免去数据类型校验等一系列细节:

.. code-block:: python

import emmm as em    # 首先导入emmm包

create = em.Create('atom', 'molecular') # 实例化一个创建方法
# 创建三个原子, 原子类型是 molecular
# 参数从左到右: label, type, x, y, z
h1 = create('h1', 'h', -1, 1, 0) 
o = create('o', 'o', 0, 0, 0)
h2 = create('h2', 'h', 1, 1, 0)  

`label` 是每个原子的标签, 可以重复, 其中一个作用是从 `Molecule` 中索引这个原子. `type` 和坐标都是LAMMPS中的标准, 而 `id` 等会在导出的时候自动生成. 然后我们需要把原子连接起来: 

.. code-block:: python
o.add_neighbors(h1, h2)
### 等价于 ###
h1.add_neighbors(o)
h2.add_neighbors(o)

只需要在一个方向上添加链接即可, 内部会对称地在另一侧生成链接. 下一步我们需要把原子组装成一个分子:

.. code-block:: 

create = em.Create('molecule', 'lmp')
h2o = create('h2o', 'h2o', h1, o, h2)

我们再得到一个生成方法, 这次它是用来生成 ``lmp`` 中 ``molecule`` 的. 接下来生成一个水分子, ``label`` 是 ``h2o``, ``type`` 是 ``h2o``. 没错, 因为 ``Molecule`` 和 ``Atom`` 都是 ``Item`` 所以有着很多相同的属性.  

对于每一个 ``Item`` , 我们需要手动将其添加到体系中. 这一步操作的意义是, 我们可能读取不同的文件, 从中提取我们需要的 ``Item``加入体系中, 而不是一股脑全部加进去. 此外, 在加入系统之前, 我们需要对 ``item`` 进行空间操作. 我们称这个系统为 ``world``, 其中储存了模型的所有细节:

.. code-block:: python

import emmm as em

world = em.World()
world.add_items(h2o)
world.xlo = 38.8
world.xhi = 38.8


操作
************

对于`Item`, 我们可以在空间中操作它们

* move() 在空间中移动
* rotate() 旋转
* rotate_orth() 在某个平面内旋转
* seperate_with() 和另一个 `Item` 分离
* get_replica() 复制自己
* duplicate() 批量复制自己



