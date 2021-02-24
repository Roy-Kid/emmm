# author: Roy Kid
class OutputBase:
    """ The parent class for all the input parser
    """
    pass

class Mapper(dict):

    def __init__(self, name, start=1) -> None:
        self.name = name
        self.counter = start

    def add(self, id):
        self[id] = self.counter
        self.counter += 1

    def retrieve(self, id):
        return self[id]