# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-16

from .molecule import Molecule
from .atom import Atom

class Topo:
    """ Topo类负责搜索拓扑结构, 包括bond, angle, dihedral和improper
        Topo类不应该负责去匹配力场参数, 这个工作应该又其他类来进行
    """

    def __init__(self, world) -> None:
        self.world = world

        self.world.topoBond = list()
        self.world.topoAngle = list()
        self.world.topoDihedral = list()

    def search_topo(self, item, isBond=True, isAngle=True, isDihedral=True, isFF=True):
        """ Topo类的主调方法, 开始搜索拓扑结构

        Args:
            item (Molecule|Atom): 待搜索的item
            isBond (bool, optional): 是否搜索bond. Defaults to True
            isAngle (bool, optional): 是否搜索angle. Defaults to True
            isDihedral (bool, optional): 是否搜索dihedral. Defaults to True
            isFF (bool, optional): 是否和力场比对. Defaults to True
        """
        self.isFF = True
        # 将item展开成atom的列表
        if isinstance(item, Molecule):
            self.atoms = item.flatten()  # <-molecule._flatten()
        elif isinstance(item, Atom):
            self.atoms = [item]
            self.world.topoBond.extend(self.search_bond(self.atoms))
        if isAngle:
            self.world.topoAngle.extend(self.search_angle(self.atoms))
        if isDihedral:
            self.world.topoDihedral.extend(self.search_dihedral(self.atoms))

    def search_bond(self, atoms):
        """ 生成bond的函数. 生成的时候会经过力场比对, 如果bond类型没有出现在已设定的力场中, 则会报错并终止程序运行. 

        Args:
            atoms (list): atom列表, 逐个搜索其neighbors

        Returns:
            list: [[atom1, atom2], ...]
        """
        # 在search_topo中的isFF级别高于局部
        isFF = self.isFF

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
            for ato in atom.get_neighbors():
                if ato.id in bond_id:
                    # warning: 似乎不太可能出现这种情况
                    # 如果自己和自己相连, 跳过
                    continue
                elif ato.id not in bond_id:

                    # 将键接的atom的id添加
                    bond_id.append(ato.id)
                    
                    # 排序以和bonds_id中已有的键比对
                    # 以防止A-B B-A情况
                    bond_id = sorted(bond_id)

                    # 实际键接关系
                    bond.append(ato)

                    # 如果现在拿到的bond没有出现过 (就是没有第二次被搜索) and
                    # 需要和力场比对:
                    if tuple(bond_id) not in bonds_id:
                        bond_type = [atom.type for atom in bond]
                        if isFF:
                            if self.world.forcefield.get_bond_coeff(bond_type):
                                # 把bond 添加到bonds
                                bonds.append(tuple(bond))
                                # 记录这个bond 的id
                                bonds_id.append(tuple(bond_id))
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
        isFF = self.isFF

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

            for ato in atom.get_neighbors():

                if ato.id not in angle_id:

                    angle.append(ato)
                    angle_id.append(ato.id)

                    for at in ato.get_neighbors():
                        
                        if at.id not in angle_id:
                            angle.append(at)
                            angle_id.append(at.id)

                            angle_id.sort()

                            if tuple(angle_id) not in angles_id:
                                angle_type = [atom.type for atom in angle]
                                if isFF:
                                    if self.world.forcefield.get_angle_ceff(angle_type):

                                        angles.append(tuple(angle))

                                        angles_id.append(tuple(angle_id))
                                    else:
                                        raise TypeError(f'angle:{angle_type} 没有匹配的力场参数')

                            angle_id.pop()
                            angle.pop()

                    angle_id.pop()
                    angle.pop()

            angle_id.pop()
            angle.pop()

        return angles

    def search_dihedral(self, atoms):
 
        isFF = self.isFF

        dihedrals_id = list()
        dihedrals = list()

        for atom in atoms:

            dihedral_id = [atom.id]
            dihedral = [atom]

            for ato in atom.get_neighbors():

                dihedral_id.append(ato.id)
                dihedral.append(ato)

                for at in ato.get_neighbors():

                    if at.id not in dihedral_id:
                        dihedral.append(at)
                        dihedral_id.append(at.id)

                        for a in at.get_neighbors():

                            if a.id not in dihedral_id:
                                dihedral.append(a)
                                dihedral_id.append(a.id)

                                dihedral_id.sort()

                                if tuple(dihedral_id) not in dihedrals_id:
                                    dihedral_type = [atom.type for atom in dihedral]
                                    if isFF:
                                        if self.world.forcefield.get_dihedral_coeff(dihedral_type):
                                            dihedrals.append(tuple(dihedral))
                                            dihedrals_id.append(tuple(dihedral_id))
                                        else:
                                            raise TypeError(f'dihedral:{dihedral_type} 没有匹配的力场')
                                
                                dihedral_id.pop()
                                dihedral.pop()

                        dihedral_id.pop()
                        dihedral.pop()
                
                dihedral_id.pop()
                dihedral.pop()

            dihedral_id.pop()
            dihedral.pop()
        
        return dihedrals