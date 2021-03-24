class PBC:
    def __init__(self, xlo, xhi, ylo, yhi, zlo, zhi) -> None:

        self.xlo = xlo
        self.xhi = xhi
        self.ylo = ylo
        self.yhi = yhi
        self.zlo = zlo
        self.zhi = zhi
        self.xl = self.xhi - self.xlo
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