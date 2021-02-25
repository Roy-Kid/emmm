# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-25
# version: 0.0.1


import numpy as np



class Constrain:
    def __init__(self, constrain) -> None:
        self.type = constrain['type']

        if self.type == 'sphere':
            self.radius = constrain['radius']
            self.center = constrain['center']
        elif self.type == 'cube':
            self.xlo = constrain['xlo']
            self.xhi = constrain['xhi']
            self.ylo = constrain['ylo']
            self.yhi = constrain['yhi']
            self.zlo = constrain['zlo']
            self.zhi = constrain['zhi']

    def __call__(self, trial):
        return self.check_constrain(trial)

    def check_constrain(self, trial):
        if self.type == 'sphere':
            return self.check_sphere(trial, self.radius, self.center)
        elif self.type == 'cube':
            return self.check_cube(trial, self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi)

    def check_sphere(self, trial, radius, center):
        if np.linalg.norm(trial - center) < radius:
            return True
        else:
            return False

    def check_cube(self, trial, xlo, xhi, ylo, yhi, zlo, zhi):
        if xlo < trial[0] < xhi and ylo < trial[1] < yhi and zlo < trial[
                2] < zhi:
            return True
        else:
            return False


class PolymerBase:
    def __init__(self) -> None:
        pass

    def rw(self, start, steps, length: int, constrain: dict):

        tolerance = 10

        cursor = np.array(start)

        trace = list()

        check_constrain = Constrain(constrain)

        i = 0
        while i < steps:
            error_times = 0
            rv = self.gen_vec(length)
            trial = cursor + rv
            if check_constrain(trial):

                trace.append(trial)
                cursor = trial
            else:
                error_times += 1
                if error_times < tolerance:
                    continue
                else:
                    print('cursor ', cursor)
                    raise Exception('尝试次数过多')

            i += 1

        return np.array(trace)

    def gen_vec(self, length):
        rv = np.random.rand(3) - 0.5
        rv = rv / np.linalg.norm(rv)
        rv = rv * length

        return rv

        # http://leandro.iqm.unicamp.br/m3g/packmol/userguide.shtml


p = PolymerBase()
constrain = {'type': 'sphere', 'center': np.array([0, 0, 0]), 'radius': 3}
constrain = {'type': 'cube', 'xlo': 0, 'ylo': 0, 'zlo':0, 'xhi': 10, 'yhi': 10, 'zhi': 10}
trace = p.rw((0, 0, 0), 10000, 1, constrain)

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection='3d')
ax.grid()
x = trace[:, 0]
y = trace[:, 1]
z = trace[:, 2]
ax.plot3D(x, y, z)

plt.show()