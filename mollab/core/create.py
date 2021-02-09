# author: Roy Kid

from mollab.core.atom import Atom
from mollab.core.molecule import Molecule

import numpy as np

class CreateAtom:

# class NodeVisitor(object):
#     def visit(self, node):
#         method_name = 'visit_' + type(node).__name__
#         visitor = getattr(self, method_name, self.generic_visit)
#         return visitor(node)

#     def generic_visit(self, node):
#         raise Exception('No visit_{} method'.format(type(node).__name__))

    @staticmethod
    def genericAtom(type):
        method_name = type+'Atom'
        create_method = getattr(CreateAtom, method_name, CreateAtom.errorRaise)
        return create_method

    @staticmethod
    def genericAtoms(type):
        method_name = type+'Atoms'
        create_method = getattr(CreateAtom, method_name, CreateAtom.errorRaise)
        return create_method

    def errorRaise():
        raise Exception('')

    @staticmethod
    def _create_atom(**kwargs):
        atom = Atom()
        for k,v in kwargs.items():
            setattr(atom, k, v)
        return atom

    @staticmethod
    def fullAtom(label, parent, type, q, x, y, z, *args):
        label = str(label)
        parent = str(parent)
        type = str(type)
        q = float(q)
        x, y, z = float(x), float(y), float(z)
        return CreateAtom._create_atom(label=label, parent=parent, type=type, q=q, x=x, y=y, z=z)       

    @staticmethod
    def fullAtoms(atoms):

        atom_list = list()
    
        for atom in atoms:

            label = atom[0]
            parent = atom[1]
            type = atom[2]
            q = atom[3]
            x, y, z = atom[4], atom[5], atom[6]

            atom_list.append(CreateAtom.fullAtom(label, parent, type, q, x, y, z))
        return atom_list
  

    @staticmethod
    def molecularAtom(label, parent, type, x, y, z, *args):
        label = str(label)
        parent = str(parent)
        type = str(type)

        x, y, z = float(x), float(y), float(z)

        return CreateAtom._create_atom(label=label, parent=parent,type=type,  x=x, y=y, z=z)


    @staticmethod
    def molecularAtoms(atoms):
        atom_list = list()
    
        for atom in atoms:
            label = atom[0]
            parent = atom[1]
            type = atom[2]
            q = atom[3]
            x, y, z = atom[4], atom[5], atom[6]

            atom_list.append(CreateAtom.fullAtom(label, parent, type, q, x, y, z))
        return atom_list

class CreateMolecule:

    @staticmethod
    def _create_molecule(label, type, atoms, isAdhere):
        mol = Molecule()
        mol.label = label
        mol.type = type

        mol.add_items(*atoms)
        mol.isAdhere = isAdhere

        return mol

    @staticmethod
    def lmpMolecule(label, type, *atoms, isAdhere=False):
        return CreateMolecule._create_molecule(label, type, atoms, isAdhere)

# class CreateAtomFull(_Create):

#     def __call__(self, label, type, q, x, y, z, **kwargs):

#         if kwargs['Atoms']:
#             return self.atoms(label, type, q, x, y, z)

#         else: 
#             return self.atom(label, type, q, x, y, z)


#     def atom(self, label, type, q, x, y, z, *args):
#         label = str(label)

#         type = str(type)
#         q = float(q)
#         x, y, z = float(x), float(y), float(z)
#         return self._create_atom(label=label, type=type, q=q, x=x, y=y, z=z)

#     def atoms(self, labels, molLabels, types, qs, xs, ys, zs, *args):
#         if len(labels) == len(types) == len(qs) == len(xs) == len(ys) == len(zs):
#             atoms = list()
#             for i in range(len(labels)):
#                 atoms.append(self._create_atom(label=labels[i], type=types[i], q=qs[i], x=xs[i], y=ys[i], z=zs[i]))
#             return atoms
#         else:
#             raise ValueError(_('传入的列表长度不相等'))

# class CreateMolecularAtom(_Create):
#     def __call__(self, label,type, x, y, z):
        
#         if isinstance(label, str):
#             return self.atom(label,type, x, y, z)
#         else:
#             return self.atoms(label,type, x, y, z)

#     def atom(self, label, type, x, y, z, *args):
#         label = str(label)

#         type = str(type)

#         x, y, z = float(x), float(y), float(z)
#         return self._create_atom(label=label, type=type,  x=x, y=y, z=z)

#     def atoms(self, labels,types,  xs, ys, zs, *args):
#         if len(labels)== len(types) == len(xs) == len(ys) == len(zs):
#             atoms = list()
#             for i in range(len(labels)):
#                 atoms.append(self._create_atom(label=labels[i], type=types[i], x=xs[i], y=ys[i], z=zs[i]))
#             return atoms
#         else:
#             raise ValueError(_('传入的列表长度不相等'))

# class CreateAtom:

#     def __call__(self, type):
#         self._atomType = {
#             'full': CreateAtomFull(),
#             'molecular': CreateMolecularAtom()
#         }
#         return self._atomType[type]

# class CreateLmpMolecule(_Create):
    
#     def __call__(self, label, type, *atoms, isAdhere=False):
        
#         return self._create_molecule(label, type, atoms, isAdhere)


# class CreateMolecule:

#     def __call__(self, type):
#         self._molType = {
#             'lmp': CreateLmpMolecule()
#         }
#         return self._molType[type]


# def Create(*type):
#     if type[0] == 'atom':
#         return CreateAtom()(type[1])
#     elif type[0] == 'molecule':
#         return CreateMolecule()(type[1])


# class Create:


