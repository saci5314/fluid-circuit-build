'''
Concentric reducer object for lumped element modeling. 

Author:
    Samuel Ciesielski

Sources:
    [1] D. C. Rennels, H. M. Hudson, "Pipe Flow: A Comprehensive and 
        Practical Guide," John Wiley & Sons, 2012.

'''

from network import Element
import pipe
from math import sqrt, log10, sin
import numpy as np
from scipy.constants import pi
import matplotlib.pyplot as plt


class Reducer(Element):
    
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
        
        
        
    ### ------------- ###
    ### Dynamics Data ###
    ### ------------- ###
    
    
    ### Set custom resistance by friction factor
    ### ----------------------------------------
    def set_custom_K_curve(self, f_data, Re_data):
        self.model = "empirical"
        self.Re_data = Re_vec # Reynold's number
        self.K_data = f_vec # Friction factor
        
        
    ### Pull inertance
    ### --------------
    def I(self, rho):
        A = pi*((self.D2 + self.D1)/2)**2/4 # midpoint area
        return rho * self.L/A
    
    
    ### Pull quadratic damping load
    ### ---------------------------
    def dP_damping(self, mdot, rho, mu):
        ### Reynold's number at current flowrate
        Re = rho * mdot * self.Dh / (mu * self.A)
        
        ### Darcy friction factor
        f = self.f_colebrook_white(self.Dh, self.epsilon, Re)

        ### Friction/viscous resistance
        return f * self.L/self.Dh
    
        
    ### Pull body load
    ### --------------
    def dP_body(self, rho):
        return 0 # (TODO)
        
        
    ### Pull steady flow equations
    ### --------------------------
    def steady_flow_eqns(self, statevars, N_sv, rho):
        ### Relevant state variables
        P_1 = statevars[self.ports[0]]
        P_2 = statevars[self.ports[1]]
        mdot_1 = statevars[N_sv/2 + self.ports[0]]
        mdot_2 = statevars[N_sv/2 + self.ports[1]]
        
        return [
            # Steady-state momentum equation
            P_2 - P_1 - self.dP_damping(mdot_1, rho) - self.dP_body(rho),
            
            # Mass continuity equation
            mdot_2 - mdot_1
        ]