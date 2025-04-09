'''
Concentric reducer object for lumped element modeling.

Author:
    Samuel Ciesielski

'''

from network import element

class reducer(element):
    
    ### CONSTRUCTOR
    ### -----------
    def __init__(self, name, D1, D2, L, a, epsilon):
        '''
        Inputs:
            name    = (string) component ID, part number, etc.
            d1      = (scalar) [m] inlet (larger) diameter
            d2      = (scalar) [m] outlet (smaller) diameter
            L       = (scalar) [m] length
            a       = (scalar) [deg] reducer angle
            epsilon = (scalar) [m] surface roughness
        '''

        ### Call parent constructor
        super().__init__(name, 2)

        ### Geometry
        self.D1 = D1      
        self.D2 = D2     
        self.L = L
        self.a = a
        self.epsilon = epsilon
