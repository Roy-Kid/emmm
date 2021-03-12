# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-03-06
# version: 0.0.1

from mollab.core.atom import fullAtom
import mollab as ml
import pytest


@pytest.fixture()
def MEM():

    mem = ml.World('')
    c1 = ml.fullAtom(1, 1, 'cl', 0, 1, 1, 0, 12)
    c2 = ml.fullAtom(2, 1, 'co', 0, -0.395, 1, 0, 12)
    c3 = ml.fullAtom(3, 1, 'cl', 0, -1.091, 1, 1.208, 12)
    c4 = ml.fullAtom(4, 1, 'cl', 0, -0.392, 1, 2.41, 12)
    c5 = ml.fullAtom(5, 1, 'co', 0, 1, 1, 2.41, 12)
    c6 = ml.fullAtom(6, 1, 'cl', 0, 1.696, 1, 1.21, 12)
    o1 = ml.fullAtom(7, 1, 'o', -0.49, -1.07, 1, -1.17, 16)
    o2 = ml.fullAtom(8, 1, 'o', -0.49, 1.682, 1, 3.58, 16)

    c1.add_linkedAtoms(c2, c6)
    c2.add_linkedAtoms(o1)
    c5.add_linkedAtoms(o2)
    c3.add_linkedAtoms(c2, c4)
    c5.add_linkedAtoms(c6, c4)

    b2 = ml.Molecule(label='B2')  #TODO: Molecule class add comment
    b2.add_items(c1, c2, c3, c4, c5, c6, o1, o2)

    # A2
    n1 = ml.fullAtom(9, 2, 'nl', -0.152, -1, 1, 3.5, 14)
    n2 = ml.fullAtom(10, 2, 'n', -0.026, -0.17, 1, 4.4, 14)
    c7 = ml.fullAtom(11, 2, 'c', -0.0423, -0.806, 1, 5.5, 12)
    c8 = ml.fullAtom(12, 2, 'c', -0.131, -2.2, 1, 5.5, 12)
    c9 = ml.fullAtom(13, 2, 'c', -0.148, -2.89, 0.98, 6.72, 12)
    c10 = ml.fullAtom(14, 2, 'c', -0.029, -2.197, 1, 7.93, 12)
    c11 = ml.fullAtom(15, 2, 'c', -0.1499, -0.803, 0.989, 7.9, 12)
    c12 = ml.fullAtom(16, 2, 'c', -0.0955, -0.1, 0.99, 6.7, 12)
    c13 = ml.fullAtom(17, 2, 'c', 0.0003, -2.86, 0.97, 9.09, 12)
    c14 = ml.fullAtom(18, 2, 'c', -0.1631, -4.207, 0.59986, 9.12, 12)
    c15 = ml.fullAtom(19, 2, 'c', -0.0778, -4.903, 0.59, 10.329, 12)
    c16 = ml.fullAtom(20, 2, 'c', -0.0891, -4.256, 0.96, 11.5, 12)
    c17 = ml.fullAtom(21, 2, 'c', -0.107, -2.9, 1.34, 11.475, 12)
    c18 = ml.fullAtom(22, 2, 'c', -0.1606, -2.2, 1.35, 10.27, 12)
    n3 = ml.fullAtom(23, 2, 'n', 0.0578, -4.884, 0.955, 12.5995, 14)
    n4 = ml.fullAtom(24, 2, 'nl', -0.467, -4.9, 1.32, 13.49, 14)

    n2.add_linkedAtoms(n1, c7)
    c7.add_linkedAtoms(c8, c12)
    c9.add_linkedAtoms(c8, c10)
    c11.add_linkedAtoms(c10, c12)
    c13.add_linkedAtoms(c10, c14, c18)
    c15.add_linkedAtoms(c14, c16)
    c17.add_linkedAtoms(c16, c18)
    n3.add_linkedAtoms(n4, c16)
    # link A2 and B2
    n1.add_linkedAtoms(c4)

    a2 = ml.Molecule(label='A2')
    a2.add_items(n1, n2, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17,
                 c18, n3, n4)

    mem.xlo = mem.ylo = mem.zlo = 0
    mem.xhi = mem.yhi = mem.zhi = 10
    mem.set_pair('lj126', 'cl', 'cl', epsilon=0.07, sigma=3.55, type='cl-cl')
    mem.set_pair('lj126', 'co', 'co', epsilon=0.07, sigma=3.55, type='co-co')
    mem.set_pair('lj126', 'c', 'c', epsilon=0.07, sigma=3.55, type='c-c')
    mem.set_pair('lj126', 'n', 'n', epsilon=0.17, sigma=3.25, type='n-n')
    mem.set_pair('lj126', 'nl', 'nl', epsilon=0.17, sigma=3.25, type='nl-nl')
    mem.set_pair('lj126', 'o', 'o', epsilon=0.17, sigma=3.12, type='o-o')

    mem.set_bond('harmonic', 'c', 'c', k=410, r0=1.44, type='c-c')
    mem.set_bond('harmonic', 'c', 'co', k=410, r0=1.44, type='c-co')
    mem.set_bond('harmonic', 'co', 'o', k=450, r0=1.37, type='co-o')
    mem.set_bond('harmonic', 'nl', 'cl', k=457, r0=1.35, type='cl-nl')
    mem.set_bond('harmonic', 'n', 'nl', k=500, r0=1.32, type='n-nl')
    mem.set_bond('harmonic', 'n', 'c', k=457, r0=1.35, type='n-c')
    mem.set_bond('harmonic', 'cl', 'co', k=410, r0=1.44, type='cl-co')
    mem.set_bond('harmonic', 'cl', 'cl', k=410, r0=1.44, type='cl-cl')

    mem.set_angle('harmonic',
                  'o',
                  'co',
                  'cl',
                  k=60,
                  theta0=122,
                  type='o-co-cl')
    mem.set_angle('harmonic',
                  'cl',
                  'co',
                  'cl',
                  k=60,
                  theta0=122,
                  type='cl-co-cl')
    mem.set_angle('harmonic',
                  'cl',
                  'cl',
                  'co',
                  k=60,
                  theta0=122,
                  type='cl-cl-co')
    mem.set_angle('harmonic',
                  'n',
                  'c',
                  'c',
                  k=69.9,
                  theta0=118.18,
                  type='n-c-c')
    mem.set_angle('harmonic',
                  'cl',
                  'cl',
                  'nl',
                  k=69.9,
                  theta0=118.18,
                  type='nl-cl-cl')

    mem.set_angle('harmonic',
                  'co',
                  'cl',
                  'nl',
                  k=69.9,
                  theta0=118.18,
                  type='co-cl-nl')

    mem.set_angle('harmonic',
                  'cl',
                  'nl',
                  'n',
                  k=60.26,
                  theta0=116.57,
                  type='cl-nl-n')
    mem.set_angle('harmonic',
                  'nl',
                  'n',
                  'c',
                  k=60.26,
                  theta0=116.57,
                  type='nl-n-c')
    mem.set_angle('harmonic', 'c', 'c', 'c', k=85, theta0=120.7, type='c-c-c')


    mem.set_dihedral('opls',
                     'o',
                     'co',
                     'cl',
                     'cl',
                     k1=0,
                     k2=1.682,
                     k3=0,
                     k4=0,
                     type='o-co-cl-cl')
    mem.set_dihedral('opls',
                     'cl',
                     'co',
                     'cl',
                     'cl',
                     k1=0,
                     k2=0,
                     k3=0.3,
                     k4=0,
                     type='cl-co-cl-cl')
    mem.set_dihedral('opls',
                     'co',
                     'cl',
                     'cl',
                     'co',
                     k1=0,
                     k2=14,
                     k3=0,
                     k4=0,
                     type='co-cl-cl-co')
    mem.set_dihedral('opls',
                     'c',
                     'c',
                     'c',
                     'c',
                     k1=0,
                     k2=7.25,
                     k3=0,
                     k4=0,
                     type='c-c-c-c')
    mem.set_dihedral('opls',
                     'c',
                     'c',
                     'n',
                     'nl',
                     k1=2,
                     k2=14,
                     k3=0,
                     k4=0,
                     type='c-c-n-nl')  # 6
    mem.set_dihedral('opls',
                     'n',
                     'c',
                     'c',
                     'c',
                     k1=2,
                     k2=0,
                     k3=0,
                     k4=0,
                     type='n-c-c-c')  # 7
    mem.set_dihedral('opls',
                     'nl',
                     'cl',
                     'cl',
                     'co',
                     k1=0,
                     k2=7,
                     k3=0,
                     k4=0,
                     type='nl-cl-cl-co')
    mem.set_dihedral('opls',
                     'cl',
                     'nl',
                     'n',
                     'c',
                     k1=0,
                     k2=7.5,
                     k3=0,
                     k4=0,
                     type='cl-nl-n-c')  # 5

    mem.set_dihedral('opls',
                     'nl',
                     'cl',
                     'co',
                     'o',
                     k1=0,
                     k2=0,
                     k3=0,
                     k4=0,
                     type='nl-cl-co-o')
    mem.set_dihedral('opls',
                     'nl',
                     'cl',
                     'co',
                     'cl',
                     k1=2,
                     k2=0,
                     k3=0,
                     k4=0,
                     type='nl-cl-co-cl')
    mem.set_dihedral('opls',
                     'n',
                     'nl',
                     'cl',
                     'co',
                     k1=0,
                     k2=14,
                     k3=0,
                     k4=0,
                     type='n-nl-cl-co')
    mem.set_dihedral('opls',
                     'n',
                     'nl',
                     'cl',
                     'cl',
                     k1=0,
                     k2=14,
                     k3=0,
                     k4=0,
                     type='n-nl-cl-cl')
    # mem.set_dihedral('opls', 'nl', 'n', 'c', 'c', k1=0, k2=14, k3=0, k4=0, type='nl-n-c-c')

    # mem.set_improper('cvff',
    #                  'co',
    #                  'o',
    #                  'cl',
    #                  'cl',
    #                  k=2.5,
    #                  d=-1,
    #                  n=2,
    #                  type='co-o-cl-cl')
    # mem.set_improper('cvff', 'co', 'cl', 'o', 'cl', k=2.5, d=-1, n=2, type='co-cl-o-cl')
    # mem.set_improper('cvff',
    #                  'c',
    #                  'c',
    #                  'c',
    #                  'n',
    #                  k=10.5,
    #                  d=-1,
    #                  n=2,
    #                  type='c-c-c-n')
    # mem.set_improper('cvff',
    #                  'c',
    #                  'c',
    #                  'c',
    #                  'c',
    #                  k=2.5,
    #                  d=-1,
    #                  n=2,
    #                  type='c-c-c-c')
    # mem.set_improper('cvff', 'cl', 'cl', 'co', 'nl', k=10.5, d=-1, n=2, type='cl-cl-co-nl')
    # mem.set_improper()
    mem.add_items(b2, isUpdate=False)
    mem.add_items(a2)

    return mem


def test_MEM(MEM):
    writer = ml.plugins.OUTlmpdat(MEM)
    # writer.write_data('B2.data', MEM['B2'])
    # writer.write_data('A2.data', MEM['A2'])
    writer.write_data('A2B2.data')