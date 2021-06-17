
class Domain:

    def __init__(self) -> None:

        # 0 - non-periodic
        # 1 - periodic
        self.periodicity = [1, 1, 1]
        
        self.xlo = 0
        self.xhi = 0
        self.ylo = 0
        self.yhi = 0
        self.zlo = 0
        self.zhi = 0

        self.set_global_box()

    def set_global_box(self):

        self.xl = self.xhi - self.xlo # xl = xprd in lammps
        self.yl = self.yhi - self.ylo
        self.zl = self.zhi - self.zlo

    def _wrap(self, x, y, z):

        ix = int(x // self.xl)
        wx = x % self.xl

        iy = int(y // self.yl)
        wy = y % self.yl

        iz = int(z // self.zl)
        wz = z % self.zl

        return (ix, wx, iy, wy, iz, wz)

    def wrap(self, atom):

        atom.ix, atom.wx, atom.iy, atom.wy, atom.iz, atom.wz = self._wrap(
            atom.x, atom.y, atom.z)

    def _unwrap(self, ix, wx, iy, wy, iz, wz):

        x = ix * self.xl + wx
        y = iy * self.yl + wy
        z = iz * self.zl + wz
        return x, y, z

    def unwrap(self, atom):
        atom.x, atom.y, atom.z = self._unwrap(atom.ix, atom.wx, atom.iy, atom.wy, atom.iz, atom.wz)
