
class Item:

    def __init__(self, itemType) -> None:
        self.label = ''
        self.itemType = itemType or 'Item'
        self._id = id(self)
        self.properties = [
            'label', 'itemType', 'style'
        ]
        self._container = []

    def register_Properties(self, *args):
        for arg in args:
            self.properties.append(arg)

    def toJson(self):
        pass

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, i):
        self._id = i

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    def __lt__(self, o: object) -> bool:
        return self.id < o.id

    def __hash__(self) -> int:
        return self.id

    def __iter__(self):
        self.__pos = 0
        return iter(self._container)

    def __next__(self):
        try:
            n = self._container[self.__pos]
            self.__pos += 1
        except:
            raise StopIteration
        return n
    