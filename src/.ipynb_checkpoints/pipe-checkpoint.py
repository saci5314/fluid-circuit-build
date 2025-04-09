'''
Constant-area pipe/duct object for lumped element modeling
and general purpose friction factor estimation formulas.

Relations provided here should be restricted to incompressible flows, or 
compressible flows for where the pressure drop incurred is << the upstream pressure.

Author:
    Samuel Ciesielski

Sources:
    [1] D. C. Rennels, H. M. Hudson, "Pipe Flow: A Comprehensive and 
        Practical Guide," John Wiley & Sons, 2012.

'''

from network import element
from math import sqrt, log10, sin
import numpy as np
from scipy.constants import pi
import matplotlib.pyplot as plt



class pipe(element):

    ### Constructor
    ### -----------
    def __init__(self, name, l, Dh, epsilon, r_bend=None, a_bend=None, model="analytical"):
        '''
        Inputs:
            name    = (string) component ID, part number, etc.
            l       = (scalar) [m] total pipe length
            Dh      = (scalar) [m] hydraulic diameter
            epsilon = (scalar) [m] absolute pipe wall roughness
            r_bend  = (vector) [m] pipe bend radii
            a_bend  = (vector) [deg] pipe bend angles
            A       = (scalar) [m^2] cross-sectional flow area
        '''

        super().__init__(name, 2) # call parent class constructor
        
        ### Geometry
        self.l = l
        self.Dh = Dh
        self.epsilon = epsilon
        self.r_bend = r_bend
        self.a_bend = a_bend
        self.A = pi*Dh**2/4
        
        ### Data for empirical flow resistance estimation
        self.Re_data = None
        self.K_data = None
        
        ### Model type indicator
        self.model = model

    ### ------------- ###
    ### Dynamics Data ###
    ### ------------- ###

    ### Set custom resistance by friction factor
    ### ----------------------------------------
    def set_custom_K_curve(self, f_data, Re_data):
        self.model = "empirical"
        self.Re_data = Re_vec # Reynold's number
        self.K_data = f_vec # Friction factor
        
    ### Pull component inertance
    ### ------------------------
    def I(self, rho):
        return rho * self.l/self.A 
    
    ### Pull component damping loads
    ### ----------------------------
    def dP_damping(self, mdot, rho, mu):
        ### Reynold's number at current flowrate
        Re = rho * mdot * self.Dh / (mu * self.A)

        ### Darcy friction factor
        f = self.f_colebrook_white(self.Dh, self.epsilon, Re)

        ### Friction/viscous resistance
        return f * self.l/self.Dh

    ### Plot Moody diagram curve
    ### ------------------------
    def moody(self, rho):
        ### Logscaled Reynold's numbers
        Re = np.logspace(1, 10e8, 100)

        ### Calc friction factors
        f = np.array(len(Re))
        for i in range(len(Re)):
            f[i] = f_colebrook_white(Dh, epsilon, Re[i], N)
            
        ### Plotstuff



### ------------------------- ###
### Fricton Factor Estimation ###
### ------------------------- ###

### Colebrook-White formula (iterative)
### -----------------------------------
def f_colebrook_white(Dh, epsilon, Re, N=4):
    '''
    Inputs:
        Dh = [m] pipe equivalent/hydralic diameter
        epsilon = [m] surface roughness
        Re = Reynold's number
        N = number of iterations
    '''

    ### Initial guess
    f = .05

    ### Colebrook-White equation with N iterations
    for _ in range(N): 
        f = (2*log10(epsilon/(3.7*Dh) + 2.51/(Re*sqrt(f))))**-2 
    
    return f

### Churchill's formula (explicit)
### ------------------------------
def f_churchill(Dh, epsilon, Re):
    '''
    Inputs:
        dh      = [m] pipe equivalent/hydralic diameter
        epsilon = [m] surface roughness
        Re      = Reynold's number
    '''

    return (2*log10(epsilon/(3.7*Dh) + (7/Re)**.9))**-2

### Curvefitting
### ------------
def f_fit():
    ...

### -------------------------- ###
### Flow Resistance Estimation ###
### -------------------------- ###

### K-factor due to friction
### ------------------------
def calc_K_friction(f, l, d):
    return f * (l/d)

### K-factor due to circular pipe bends
### -----------------------------------
def calc_K_bend(f, d, r, a):
    '''
    Inputs:
        f = (scalar) friction factor
        d = (scalar) [m] pipe diameter
        r = (vector) [m] bend radius
        a = (vector) [deg] bend angle
    '''

    ### Convert bend angle to radians
    a = a * pi/180

    ### Calculate K factor
    K = f*a*(r/d) + (.1 + 2.4*f)*sin(a/2) + \
        6.6*f*(sqrt(sin(a/2)) + sin(a/2))/(r/d)/(4*a/pi)

    return K



### ----------- ###
### Handy Calcs ###
### ----------- ###

### Convert between K-factor and discharge coefficient
### --------------------------------------------------
def Cd_from_K(K):
    return sqrt(1/K)

def K_from_Cd(Cd):
    return 1/Cd**2

### Calc pressure drop from mass flow rate
### --------------------------------------
def dP_from_K(K, mdot, d, rho):
    return K * mdot**2 / (2*(pi*d**2/4)**2 * rho)

def dP_from_Cd(Cd, mdot, d, rho):
    return mdot**2 / (2*(Cd * pi*d**2/4)**2 * rho)

### Calc mass flow rate from pressure drop
### --------------------------------------
def mdot_from_K(K, dP, d, rho):
    return pi*d**2/4 * sqrt(2*dP*rho/K)

def mdot_from_Cd(Cd, dP, d, rho):
    return Cd * pi*d**2/4 * sqrt(2*dP*rho)