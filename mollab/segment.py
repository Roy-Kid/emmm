from mollab.item import Item
from mollab.particle import Particle

class Segment(Item):

    def __init__(self, style=None) -> None:
        super().__init__('Segment')
        self.style = style or 'Segment'
        self.subs = {}

    def toJson(self):

        # segment properties
        mjson = {}
        for p in self.properties:
            mjson[p] = getattr(self, p)

        # sub segment
        subs = {}
        for id, sub in self.subs.items():
            subs[id] = sub.toJson()
        mjson['subs'] = subs

        # topo

        return mjson

    def updateTopo(self):

        self.getBonds()

    def getBonds(self):

        self._bonds = []
        for id, sub in self.subs.items():
            self._bonds.extend(sub.getBonds())

        # duplicate removal

        for i in range(len(self._bonds)):
            bond = self._bonds[i]
            for j in range(i):
                if self._bonds[j] is not None and ((bond[0].id == self._bonds[j][0].id and bond[1].id == self._bonds[j][1].id ) or (bond[1].id == self._bonds[j][0].id and bond[0].id == self._bonds[j][1].id)): 
                    self._bonds[i] = None

        self._bonds = list(filter(lambda x: True if x is not None else False, self._bonds))

        # idlist = [sorted([b.id for b in bond]) for bond in self._bonds]
        # for i in range(1, len(idlist)-1):
        #     if idlist[i] in idlist[:i]:
        #         idlist[i] = None

        return self._bonds

    def fromJson(self, molecule: dict):

        for k, v in molecule.items():
            if k != 'subs':
                setattr(self, k, v)
            else:
                for id, sub in v.items():
                    if sub['itemType'] == 'Segment':
                        self.subs[id] = Segment().fromJson(sub)
                        self.subs[id].id = id
                    else:
                        self.subs[id] = Particle().fromJson(sub)
                        self.subs[id].id = id
        
        return self

    def append(self, *items):
        for item in items:
            self.subs[item.id] = item
            item.parent = self.label
