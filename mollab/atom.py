from mollab.particle import Particle

class Atom(Particle):

    def __init__(self) -> None:
        super().__init__(style='Atom')
        self.register_Properties('q', 'type')
        self.type = None
        self.q = None

    def toJson(self):

        properties = {

        }

        return super().toJson(properties)
    
    def __str__(self) -> str:
        return f' < atom {self.label} > '

    __repr__ = __str__

    def duplicate(self):
        return Atom().fromJson(self.toJson())
