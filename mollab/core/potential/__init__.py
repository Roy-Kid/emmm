# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-24
# version:
""" This module is used to link core and potential file. 
    The reason that why i dont put these modules in the plugin is that:
        1. they are invoked by the core not users;
        2. they are the essential part of core running.
"""

from importlib import import_module

__all__ = [
    'bond_potential_interface', 'angle_potential_interface',
    'dihedral_potential_interface', 'improper_potential_interface',
    'pair_potential_interface'
]


# how to import https://blog.csdn.net/edward_zcl/article/details/88809212
def bond_potential_interface(style: str, typeName1, typeName2, coeffs, id=None, type=None):

    module_name = 'mollab.core.potential.' + 'bond_' + style
    class_name = 'Bond' + style.capitalize()

    bp = getattr(import_module(module_name), class_name)(typeName1, typeName2, coeffs)
    bp.id = id
    bp.type = type
    return bp


def angle_potential_interface(style: str, typeName1, typeName2, typeName3,
                              coeffs, id=None, type=None):

    module_name = 'mollab.core.potential.' + 'angle_' + style
    class_name = 'Angle' + style.capitalize()
    ap = getattr(import_module(module_name), class_name)(typeName1, typeName2, typeName3, coeffs)
    ap.id = id
    ap.type = type
    return ap


def dihedral_potential_interface(style: str, typeName1, typeName2, typeName3,
                                 typeName4, coeffs, id=None, type=None):

    module_name = 'mollab.core.potential.' + 'dihedral_' + style
    class_name = 'Dihedral' + style.capitalize()
    dp = getattr(import_module(module_name), class_name)(typeName1, typeName2, typeName3, typeName4, coeffs)
    dp.id = id
    dp.type = type
    return dp


def improper_potential_interface(style: str,  typeName1, typeName2, typeName3,
                                 typeName4, coeffs, id=None, type=None):

    module_name = 'mollab.core.potential.' + 'improper_' + style
    class_name = 'Improper' + style.capitalize()
    ip = getattr(import_module(module_name), class_name)(typeName1, typeName2, typeName3, typeName4, coeffs)
    ip.id = id
    ip.type = type
    return ip


def pair_potential_interface(style: str,  typeName1, typeName2, coeffs, id=None, type=None):

    module_name = 'mollab.core.potential.' + 'pair_' + style
    class_name = 'Pair' + style.capitalize()
    pp = getattr(import_module(module_name), class_name)(typeName1, typeName2, coeffs)
    pp.type = type
    pp.id = id
    return pp
