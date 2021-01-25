# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

class BondBase:
    
    def __init__(self) -> None:
        self.r0 = float()

    def _grid(self, rmin=10, rmax=10, bin=100):

        rmin = -1*rmin*self.r0
        rmax =  1*rmax*self.r0

        dr = int(rmax - rmin)/bin
        rlist = [ rmin+i*dr for i in range(bin) ]
        return rlist
        
    def energy(self, r):
        return r


    def plot_energy(self, rmin=10, rmax=10, bin=100):

        rlist = self._grid(rmin, rmax, bin)
        elist = [self.energy(r) for r in rlist]

        return (rlist, elist)

    def force(self, r):
        return r

    def plot_force(self, rmin=10, rmax=10, bin=100):

        rlist = self._grid(rmin, rmax, bin)
        flist = [self.force(r) for r in rlist]

        return (rlist, flist)

    def lmpformat(self):
        pass