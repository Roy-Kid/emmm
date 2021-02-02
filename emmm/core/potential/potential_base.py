# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

class PotentialBase:

    def __init__(self) -> None:
        self._style = str()

    @property
    def style(self):
        return self._style

    def compair(self) -> bool:
        pass

    def energy(self):
        pass

    def force(self):
        pass

    def _grid(self, rmin, rmax, bin):
        rmin = -1*rmin*self.r0
        rmax =  1*rmax*self.r0

        dr = int(rmax - rmin)/bin
        rlist = [ rmin+i*dr for i in range(bin) ]
        return rlist

    def plot_energy(self, rmin=10, rmax=10, bin=100):

        rlist = self._grid(rmin, rmax, bin)
        elist = [self.energy(r) for r in rlist]

        return (rlist, elist)

    def plot_force(self, rmin=10, rmax=10, bin=100):

        rlist = self._grid(rmin, rmax, bin)
        flist = [self.force(r) for r in rlist]

        return (rlist, flist)

class BondBase(PotentialBase):
    
    def __init__(self, typeName1, typeName2) -> None:
        super().__init__()
        self.typeName1 = typeName1
        self.typeName2 = typeName2

    def compare(self, t1, t2):
        if (t1==self.typeName1 and t2==self.typeName2) or (t1==self.typeName2 and t2==self.typeName1):
            return True
        else:
            return False

class AngleBase:
    
    def __init__(self, typeName1, typeName2, typeName3) -> None:
        self.r0 = float()
        self.typeName1 = typeName1
        self.typeName2 = typeName2
        self.typeName3 = typeName3

    def compare(self, t1, t2, t3):
        if [t1,t2,t3]==[self.typeName1,self.typeName2,self.typeName3] or\
           [t3,t2,t1]==[self.typeName1,self.typeName2,self.typeName3] :
            return True
        else:
            return False


class DihedralBase:

    def __init__(self, typeName1, typeName2, typeName3, typeName4) -> None:
        super().__init__()
        self.typeName1 = typeName1
        self.typeName2 = typeName2
        self.typeName3 = typeName3       
        self.typeName4 = typeName4

    def compare(self, t1, t2, t3, t4):
        if [t1, t2, t3, t4] == [self.typeName1, self.typeName2, self.typeName3, self.typeName4] or [t4, t3, t2, t1] == [self.typeName1, self.typeName2, self.typeName3, self.typeName4]:
            return True
        else:
            return False

class ImproperBase(PotentialBase):

    def __init__(self, typeName1, typeName2, typeName3, typeName4) -> None:
        super().__init__()
        self.typeName1 = typeName1
        self.typeName2 = typeName2
        self.typeName3 = typeName3       
        self.typeName4 = typeName4

    def __str__(self) -> str:
        return f'improper style:{self._style} def by {self.typeName1} {self.typeName2} {self.typeName3} {self.typeName4}'

    def compare(self, t1, t2, t3, t4):
        if t1 == self.typeName1 and sorted([t2, t3, t4]) == sorted([self.typeName2, self.typeName3, self.typeName4]):
            return True
        else:
            return False

class PairBase(PotentialBase):

    def __init__(self, typeName1, typeName2) -> None:
        super().__init__()
        self.typeName1 = typeName1
        self.typeName2 = typeName2

    def compare(self, t1, t2):
        if (t1==self.typeName1 and t2==self.typeName2) or (t1==self.typeName2 and t2==self.typeName1):
            return True
        else:
            return False