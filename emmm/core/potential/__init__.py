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

def bond_potential_interface(style:str, coeffs:dict):

    module_name = 'bond_'+style

    bond_potential = import_module(module_name)