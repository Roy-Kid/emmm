from emmm.core.forcefield import ForceField
from emmm.core.world import World

w = World()
f = ForceField(w)
f.set_bond_coeffs('harmonic', 'C', 'H', 1, 2, 3)
print(f.get_bond_coeffs('C', 'H'))