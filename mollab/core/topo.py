# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-14
# version: 0.0.2

from itertools import combinations
from mollab.core.bond import Bond
from mollab.core.angle import Angle


class Topo:
    """ Topo类负责搜索拓扑结构, 包括bond, angle, dihedral和improper

    """
    def __init__(self, world) -> None:
        self.world = world

        self.bonds = list()
        self.angles = list()
        self.dihedrals = list()
        self.impropers = list()

    def search_topo(self,
                    isBond=True,
                    isAngle=True,
                    isDihedral=True,
                    isImproper=True,
                    isAbinitio=True):
        """ Topo类的主调方法, 开始搜索拓扑结构

        Args:
            item (Molecule|Atom): 待搜索的item
            isBond (bool, optional): 是否搜索bond. Defaults to True
            isAngle (bool, optional): 是否搜索angle. Defaults to True
            isDihedral (bool, optional): 是否搜索dihedral. Defaults to True
            isAbinitio (bool, optional): 是否从头搜索. Defaults to True
        """
        self.atoms = self.world.atoms
        self.isAbinitio = True
        # 将item展开成atom的列表
        # if item.itemType == 'Molecule':
        #     self.atoms = item.flatten()  # <-molecule._flatten()
        # elif item.itemType == 'Atom':
        #     self.atoms = [item]
        if isBond:
            self.bonds.extend(self.search_bond(self.atoms))
        if isAngle:
            self.angles.extend(self.search_angle(self.atoms))
        if isDihedral:
            self.dihedrals.extend(self.search_dihedral(self.atoms))
        if isImproper:
            self.impropers.extend(self.search_improper(self.atoms))

    def search_bond(self, atoms):
        """ 生成bond的函数. 生成的时候会经过力场比对, 如果bond类型没有出现在已设定的力场中, 则会报错并终止程序运行.

        Args:
            atoms (list): atom列表, 逐个搜索其linkedAtoms

        Returns:
            list: [[atom1, atom2], ...]
        """

        # bond_id -> bond_id
        bonds_id = list()

        # bonds -> bond
        bonds = list()

        for atom in atoms:
            # 取第一个atom, 然后内层for搜索所有键接的atom
            # bond -> [atom, atom]
            bond = [atom]
            bond_id = [atom.id]

            # 外层的atoms传入的已经是atom列表了
            for ato in atom.linkedAtoms:
                if ato.id in bond_id:
                    # warning: 似乎不太可能出现这种情况
                    # 如果自己和自己相连, 跳过
                    continue
                elif ato.id not in bond_id:

                    # 实际键接关系
                    bond.append(ato)
                    # 将键接的atom的id添加
                    bond_id.append(ato.id)

                    sorted_bond_id = tuple(sorted(bond_id))

                    # 排序以和bonds_id中已有的键比对
                    # 以防止A-B B-A情况

                    # 如果现在拿到的bond没有出现过 (就是没有第二次被搜索) and
                    # 需要和力场比对:
                    if sorted_bond_id not in bonds_id:
                        bond_type = [atom.type for atom in bond]
                        bp = self.world.forcefield.get_bond(*bond_type)
                        if bp:
                            # 把bond 添加到bonds
                            bonds.append(Bond(atom, ato, bp=bp))
                            # 记录这个bond 的id
                            bonds_id.append(sorted_bond_id)
                        else:
                            raise TypeError(f'bond:{bond_type} 没有相匹配的力场参数')

                    # 弹出键接atom, 准备检查下一个
                    bond.pop()
                    bond_id.pop()

            # 准备检查下一个
            bond.pop()
            bond_id.pop()

        return bonds

    def search_angle(self, atoms):
        """ 生成angle的函数. 生成的时候会经过力场比对, 如果angle类型没有出现在已设定的forcefield中, 则会警告.

        Args:
            atoms (list): atom的列表, 向下搜索两层neighbor

        Returns:
            list: [[atom1, atom2, atom3], ...] 
        """

        # angle_id -> angle_id
        angles_id = list()

        # bonds -> bond
        angles = list()

        for atom in atoms:
            # 取第一个atom, 然后内层for搜索所有键接的atom

            # angle_id -> [atom.id, atom.id, atom.id]
            angle_id = [atom.id]

            # angle -> [atom, atom, atom]
            angle = [atom]

            for ato in atom.linkedAtoms:

                if ato.id not in angle_id:

                    angle.append(ato)
                    angle_id.append(ato.id)

                    for at in ato.linkedAtoms:

                        if at.id not in angle_id:
                            angle.append(at)
                            angle_id.append(at.id)

                            sorted_angle_id = tuple(sorted(angle_id))

                            if sorted_angle_id not in angles_id:
                                angle_type = [atom.type for atom in angle]
                                ap = self.world.forcefield.get_angle(
                                        *angle_type)
                                if ap:

                                    angles.append(Angle(atom, ato, at, ap=ap))

                                    angles_id.append(sorted_angle_id)

                                else:
                                    # raise TypeError(f'angle:{angle_type} 没有匹配的力场参数')
                                    print(f'angle:{angle_type} 没有匹配的力场参数')
                            angle_id.pop()
                            angle.pop()

                    angle_id.pop()
                    angle.pop()

            angle_id.pop()
            angle.pop()
        return angles

    def search_dihedral(self, atoms):

        dihedrals_id = list()
        dihedrals = list()

        for atom in atoms:

            dihedral_id = [atom.id]
            dihedral = [atom]

            for ato in atom.linkedAtoms:

                dihedral_id.append(ato.id)
                dihedral.append(ato)

                for at in ato.linkedAtoms:

                    if at.id not in dihedral_id:
                        dihedral.append(at)
                        dihedral_id.append(at.id)

                        for a in at.linkedAtoms:

                            if a.id not in dihedral_id:
                                dihedral.append(a)
                                dihedral_id.append(a.id)

                                sorted_dihedral_id = tuple(sorted(dihedral_id))

                                if sorted_dihedral_id not in dihedrals_id:
                                    dihedral_type = [
                                        atom.type for atom in dihedral
                                    ]

                                    if self.world.forcefield.get_dihedral(
                                            *dihedral_type):
                                        dihedrals.append(tuple(dihedral))
                                        dihedrals_id.append(
                                            sorted_dihedral_id)
                                    else:
                                        # raise TypeError(f'dihedral:{dihedral_type} 没有匹配的力场')
                                        print(
                                            f'dihedral:{dihedral_type} 没有匹配的力场'
                                            )

                                dihedral_id.pop()
                                dihedral.pop()

                        dihedral_id.pop()
                        dihedral.pop()

                dihedral_id.pop()
                dihedral.pop()

            dihedral_id.pop()
            dihedral.pop()

        return dihedrals

    def search_improper(self, atoms):
        # defination of improper can refer to the manual of LAMMPS
        # in the section of improper style

        impropers_id = list()
        impropers = list()

        # I-atom
        for atom in atoms:

            all_improper = combinations(atom.linkedAtoms, 3)
            for improper in all_improper:
                improper = [atom] + list(improper)
                improper_id = [atom.id for atom in improper]
                sorted_improper_id = tuple(sorted(improper_id))

                if sorted_improper_id not in impropers_id:
                    improper_type = [atom.type for atom in improper]
                    if self.world.forcefield.get_improper(*improper_type):
                        impropers.append(tuple(improper))
                        impropers_id.append(sorted_improper_id)
                    else:
                        print(f'improper:{improper_type} 没有匹配力场')

        return impropers
