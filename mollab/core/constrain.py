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
        self.check_constrain(trial)

    def check_constrain(self, trial):
        if self.type == 'sphere':
            self.check_sphere(trial, self.radius, self.center)
        elif self.type == 'cube':
            self.check_cube(trial, self.max, self.min)

    def check_sphere(self, trial, radius, center):
        if np.linalg.norm(trial - center) < radius:
            return True
        else:
            return False

    def check_cube(self, trial, xlo, xhi, ylo, yhi, zlo, zhi):
        if xlo < trial[0] < xhi and ylo < trial[1] < yhi and zlo < trial[2] < zhi:
            return True
        else:
            return False
            