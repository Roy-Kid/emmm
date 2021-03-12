# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-24
# version: 0.0.1


class Mapper(dict):
    """
    {TypeName: id}
    """
    def __init__(self, name, start=1) -> None:
        self.name = name
        self.counter = start

    def map(self, typeName):
        if not self.get(typeName, False):
            self[typeName] = self.counter
            self.counter += 1

    def retrieve(self, TypeName):
        return self[TypeName]
