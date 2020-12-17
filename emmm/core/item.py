# author: Roy Kid

import numpy as np


class Item:

    def __init__(self, label=None, type=None, parent=None, path=None):

        self.label = label
        self.type = type
        self.parent = parent
        self.path = path

        self.container = list()
        self._coords = list()
        self._pos = 0

        # in the Atom, _coords = _position
        # in the mol, _coords contains all the atoms' coordinates, _position is the barycenter of the moleule

    def __lt__(self, o):
        return self.label < o.label

    def __eq__(self, o):
        return self.label == o.label

    def __iter__(self):
        return iter(self.container)

    def __next__(self):
        try:
            n = self.container[self._pos]
            self._pos += 1
        except IndexError:
            raise StopIteration
        return n

    def __getitem__(self, v):
        for i in self.container:
            if i.label == v:
                return i

    def append(self, o):
        self.container.append(o)

    def pop(self):
        return self.container.pop()

    def ls(self):
        print(self.container)

    @property
    def id(self):
        return self.id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if isinstance(value, list) and isinstance(value, tuple):
            value = np.array(value)
            self._position = np.array(value)
        elif isinstance(value, np.ndarray):
            self._position = value
        else:
            raise TypeError(_("传入的坐标格式错误"))

    @property
    def x(self):
        return float(self._position[0])

    @x.setter
    def x(self, x):
        self._position[0] = x

    @property
    def y(self):
        return float(self._position[1])

    @y.setter
    def y(self, y):
        self._position[1] = y

    @property
    def z(self):
        return float(self._position[2])

    @z.setter
    def z(self, z):
        self._position[2] = z

    def move(self, x, y, z):
        """[In-place]

        Args:
            x (Float): vector in x
            y (Float): vector in y
            z (Float): vector in z
        """

        vec = np.array([x, y, z], dtype=float)
        self.coords += vec

    def randmove(self, length):
        """[In-place]

        Args:
            length (Float): length to random move in any orientation vector
        """
        vec = np.random.random([3, 1])
        vec /= np.linalg.norm(vec)
        vec *= length
        self.coords += vec

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        """[summary]

        Args:
            theta (radian): theta:=theta*PI
            x (float): to
            y (float): to
            z (float): to
            x0 (float): from
            y0 (float): from
            z0 (float): from
        """
        # rotation axis
        x = float(x)
        y = float(y)
        z = float(z)
        x0 = float(x0)
        y0 = float(y0)
        z0 = float(z0)
        disVec = np.array([x0, y0, z0])
        rotAxis = np.array([x, y, z])

        rotAxis = rotAxis/np.linalg.norm(rotAxis)
        rotAxisX, rotAxisY, rotAxisZ = rotAxis

        # half theta = theta/2
        htheta = np.pi*theta/2
        # sin theta = sin(htheta)
        stheta = np.sin(htheta)

        a = np.cos(htheta)
        b = stheta*rotAxisX
        c = stheta*rotAxisY
        d = stheta*rotAxisZ
        b2 = b**2
        c2 = c**2
        d2 = d**2
        ab = a*b
        ac = a*c
        ad = a*d
        bc = b*c
        bd = b*d
        cd = c*d

        # rotation matrix
        rotm = np.array([[1-2*(c2+d2), 2*(bc-ad), 2*(ac+bd)],
                         [2*(bc+ad), 1-2*(b2+d2), 2*(cd-ab)],
                         [2*(bd-ac), 2*(ab+cd), 1-2*(b2+c2)]])

        self.coords -= disVec
        self.coords = np.dot(rotm, self.coords)
        self.coords += disVec

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):

        if (x, y, z) == (1, 0, 0) or\
           (x, y, z) == (0, 1, 0) or\
           (x, y, z) == (0, 0, 1):

            self.rotate(self, theta, x+xAxis, y+yAxis, z+zAxis, x, y, z)
        else:
            raise SyntaxError(
                'only one of *Axis can be 1 to indicate the orientation of rotation axis')

    def seperate_with(self, targetItem, type, value):
        """ [Bioperate] to seperate two items in opposite direction: (rel)ative distance is move EACH item in a distance under system unit; (abs)olute distance is the time of current distance of two items, e.g.: item+=unit_orientation_vector*rel; item+=orientation_vector*abs.

        Args:
            targetItem (Item): Atom|Molecule
            type (str): rel|abs
            value (Float): distance
        """
        coords1 = self.coords
        coords2 = targetItem.coords

        # orientation vector
        oriVec = coords2 - coords1
        uniVec = oriVec/np.linalg.norm(oriVec)

        if type == 'relative' or type == 'rel':
            coords2 += uniVec*value
            coords1 -= uniVec*value
        if type == 'abusolute' or type == 'abs':
            coords2 += oriVec*value
            coords1 -= oriVec*value

        self.coords = coords1
        targetItem.coords = coords2

    def distance_to(self, targetItem):
        """[Bioperate] return the distance to a target item

        Args:
            targetItem (Item): Atom|Molecule
        """
        coords1 = self.coords
        coords2 = targetItem.coords

        dist = np.linalg.norm(coords2-coords1)

        return dist

    @property
    def ls(self):
        print(self.container)

    @property
    def pwd(self):
        print(self.path)

    def get_replica(self, newLabal):
        pass

    def compute_bounding_box(self):
        pass

    def compute_bounding_sphere(self):
        pass
