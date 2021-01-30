universe 和 world

当我们同时读入多个文件时, 会出现一个问题, 就是各个文件中的各种名字会出现重名的问题. 例如, type可能都是C或者12, 但是却指代的不同环境中的C; 这样的话就会导致与其相匹配的力场也会发生混乱. 因此为了防止这种冲突, 我又引入了universe的概念. 

每一个world都有着一套独立的映射关系, 在这一套关系中都是一对一的. 而不同的world之间则没有联系. 所有的world都储存在universe中, universe也会有一套自己的映射关系. universe也是world, 是有很多个world组成的. 当生成topo的时候, 每个world首先进行扫描, 然后universe在扫描world之间的层级关系. 