'''
Manifold object for lumped element modeling.

Author:
    Samuel Ciesielski

'''

from network import element

class manifold(element):
    
    ### CONSTRUCTOR
    ### -----------
    def __init__(self, name, N_ports):
        super().__init__(name, N_ports)