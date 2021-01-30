# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-30
# version: 0.0.1
from core.potential.potential_base import DihedralBase
import math

class DihedralOpls(DihedralBase):

    def __init__(self, typeName1, typeName2, typeName3, typeName4, coeffs) -> None:
        super().__init__(typeName1, typeName2, typeName3, typeName4)

        self.k1 = coeffs['k1']
        self.k2 = coeffs['k2']
        self.k3 = coeffs['k3']
        self.k4 = coeffs['k4']

    def energy(self, phi):

        return 0.5*( 
            self.k1*(1+math.cos(phi))+
            self.k2*(1+math.cos(2*phi))+
            self.k3*(1+math.cos(3*phi))+
            self.k4*(1+math.cos(4*phi))
         )

    def force(self, phi):

        return -0.5*(
            self.k1*math.sin(phi)+
            2*self.k2*math.sin(2*phi)+
            3*self.k3*math.sin(3*phi)+
            4*self.k4*math.sin(4*phi)
        )