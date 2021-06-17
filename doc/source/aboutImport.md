#! https://zhuanlan.zhihu.com/p/351546825
# 关于python包管理的那些事

python的import, 是一个巨尼玛头疼的事. 网上有大量的解析, 非常详尽, 唯一的缺点是看完之后还是报错. 我写mollab的时候最绝望的事就是自己写得代码之间相互引用的问题, 每次都是求着别人帮我. 事实证明, 他们给我写得也是乱得一批, 还不如自己专门找个时间解决一下. 

## 基本概念

第一个需要知道的概念是`package`, 就是有`__init__.py`的文件夹; 

第二个需要知道的就是`module`. `package`下所有的`.py`都叫做`module`; 

第三个相关的是`sys.path`, python会根据这个list的顺序向下查找要导入的模块. 如果你import的包不在这个路径中, 需要用append加进去.

## 层次架构

有两种import情景, 第一种是import 通过pip或者什么的安装的第三方包. 这常简单, 因为是单向的, 就是从`lib/site-packages`引入到你写的代码之中, 而这个路径就在`sys.path`中, 因此直接导入即可. 第二种是最麻烦的, 是自己引用自己写得`module`. 首先项目的位置并不在`sys.path`中, 其次会发生各种莫名其妙的错误. 出现了任何一个问题, 根源都是项目结构设计的不合理. 

![Image](https://pic4.zhimg.com/80/v2-f5bdefe316ae4de3f9b44d8f074f1b03.png)

首先最左边的是mollab项目的跟文件夹, 同时也是git的仓库. 下面有一个同名的mollab, 装文档的doc和测试的test, 其他零零碎碎的如LICENSE, setup.py等等. 其中子mollab是打包上传到pypi的文件夹, 也是mollab这个package的顶层包. 这样做的好处是, 上传到pypi的时候可以不把doc和test这些跟开发有关的文件封进去. 在mollab中是三个子包, core是核心代码, plugins是插件系统, i18n是本土化相关. 

在设计结构的时候, 我觉得应该把它想像成一个圆葱, 最内层就是最核心的组件, 其他外层都是需要引用和依赖于核心组件, 而核心组件不应该引用和依赖于外层组件. 比如我的core中最核心的是`Item`类, `Atom`, `Molecule`和`World`是继承这个类, 其他的`forcefield`则是引用了这些类, 保证了信息流动总是单向的, 都是从最内层传到外面. 

## 引用形式

import有两种形式: 

1. import xxx [as xx]

    * 我不是很建议使用这个语句, 在我的感觉中, 通常都是import一个包. import某个包的时候, python将会读取`__init__.py`下的内容. 因此在mollab中, 别人使用这个包的时候是用得跟numpy一样的语法`import mollab as ml`. 

2. from xxx import xx

    * 我认为这个才是导入一个模块的标准做法. xxx是某一个包. 首先python会读取这个包的`__init__.py`, 读取其中的import语句, 递归处理这些import语句所有的包中的代码. 当`__init__.py`执行完之后, 再import xx模块. 这不是想象中的从xxx中挑出xx导入, 这也是出错的大头.

导入的时候一种是相对导入, 一种是绝对导入. 

1. 相对导入

    * 比如我的plugins需要导入 core中的模块, 就跟linux这种操作系统一样, 我需要写`from ..core.atom import Atom`. 但SO上的人都不推荐使用相对导入, 因为如果写有这个导入语句的模块的位置发生变动, 需要重写这个导入语句. 

2. 绝对导入

    * 绝对导入就是从最顶成的包出发, 去导入子包中的子模块. 刚刚那个例子中, 就应该写成`from mollab.core.atom import Atom`. 即便我这个模块的位置发生了变动, 只要`atom`不变, 那就不需要改. 

## 导入原则

我们可以看到, 这个导入是和项目结构息息相关的. 因此只有在一个合适的架构下, 才有解决导入问题的可能. 如果本身项目设计的混乱不堪, 就没法通过只修改导入语句的方式解决问题. 

第一个原则是, 项目内部统统都用`from xxx import xx`的语法, 都用绝对导入. 这样的好处是, 都是从上到下去查找. 这样可以避免`no module named xxx` 和 `relative import 啥啥啥` 等问题. (我属实不想去回忆到底是怎么造成的了)

第二个原则是, `__init__.py`中只写对外暴露的模块或者类的导入语句. 例如我想让core外的代码导入`Atom`类, 那我就在`__init__.py`中写`from .atom import Atom`. 这样我plugins里的代码需要导入`Atom`, 只需要写`from mollab.core import Atom`即可. 

第三个原则是, 一层层把所有需要暴露出来的类, 函数, 模块都写在`__init__.py`中, 这样就可以通过最简单的语法去导入. 

## 循环导入

一个很严重的问题是循环导入, 这里想以他为例子解释一下导入的时候发生了什么. 

首先, 假如core的`__init__.py`中写`from .atom import Atom`和`from .molecule import Molecule`, `atom.py`中写`from mollab.core import Molecule`, `molecule.py`中写`from mollab.core import Atom`. 
猛地一看这样写没毛病啊, `__init__.py`中向外暴露`Atom`类, `molecule.py`从core中导入暴露出来的`Atom`类, `atom.py`中导入`Molecule`类. 这种写法从项目之外写没有问题, 甚至可以说很好, 但是: 

![Image](https://pic4.zhimg.com/80/v2-efc60688df79639c3a2a0086889fa569.png)!

从`molecule.py`出发, `from mollab.core import Atom`先去找`__init__.py`, 逐行读其中的导入语句. 其中的`from .atom import Atom` 又去读`atom.py`, 其中的`from mollab.core import Molecule`再次指回了`molecule.py`, 再处理`from mollab.core import Atom`... 造成了循环

这时候可以说组织结构没有问题, 只是语法有问题. 如果采用`from mollab.core.atom import Atom`的话, 似乎直接跳过了`__init__.py`. 这也就是为什么让所有的都采用原则一+原则二

## 总结
有人说python的import系统非常烂, 其实我觉得是因为它不单单是一个语法问题, 而是暗含的跟项目结构挂钩. 因此如果只是在调整语句, 很难解决问题. 所以我的建议是不破不立, 遇到了解决不了的import问题, 不妨跳出来想想, 你的代码是不是做到了高内聚, 低耦合, 代码间的依赖是不是比你兜里的耳机线都绕. 如果是的话, 换一个AirPods Pro吧... 这东西真的, 直接提高生活质量.