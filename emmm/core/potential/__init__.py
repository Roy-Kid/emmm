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

# how to import https://blog.csdn.net/edward_zcl/article/details/88809212
def bond_potential_interface(style:str, typeName1, typeName2, coeffs:dict):
    
    module_name = 'emmm.core.potential.'+'bond_'+style
    class_name = 'Bond'+style.capitalize()

    bp = getattr(import_module(module_name), class_name)
    return bp(typeName1, typeName2, coeffs)

def angle_potential_interface(style:str, typeName1, typeName2, typeName3, coeffs):

    module_name = 'emmm.core.potential.'+'angle_'+style
    class_name = 'Angle'+style.capitalize()
    ap = getattr(import_module(module_name), class_name)
    return ap(typeName1, typeName2, coeffs)

def dihedral_potential_interface(style:str, typeName1, typeName2, typeName3, typeName4, coeffs):

    module_name = 'emmm.core.potential.'+'dihedral_'+style
    class_name = 'Dihedral'+style.capitalize()
    dp = getattr(import_module(module_name), class_name)
    return dp(typeName1, typeName2, coeffs)

def improper_potential_interface(style:str, typeName1, typeName2, typeName3, typeName4, coeffs):

    module_name = 'emmm.core.potential.'+'improper_'+style
    class_name = 'Improper'+style.capitalize()
    ip = getattr(import_module(module_name), class_name)
    return ip(typeName1, typeName2, coeffs)

def pair_potential_interface(style:str, typeName1, typeName2, coeffs):

    module_name = 'emmm.core.potential.'+'pair_'+style
    class_name = 'Pair'+style.capitalize()
    pp = getattr(import_module(module_name), class_name)
    return pp(typeName1, typeName2, coeffs)