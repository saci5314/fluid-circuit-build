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

import pipe
from network import Element
from math import sqrt, log10, sin
import numpy as np
from scipy.constants import pi
import matplotlib.pyplot as plt



class Pipe(Element):

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
        
        
    ### Pull inertance
    ### --------------
    def I(self, rho):
        return rho * self.l/self.A 
    
    
    ### Pull quadratic damping load
    ### ---------------------------
    def dP_damping(self, mdot, rho, mu):
        ### Reynold's number at current flowrate
        Re = rho * mdot * self.Dh / (mu * self.A)

        ### Darcy friction factor
        f = self.f_colebrook_white(self.Dh, self.epsilon, Re)

        ### Friction/viscous resistance
        return f * self.l/self.Dh
    
    
    ### Plot Moody diagram curve
    ### ------------------------
    def moody_curve(self, rho):
        ### Logscaled Reynold's numbers
        Re = np.logspace(1, 10e8, 100)

        ### Calc friction factors
        f = np.array(len(Re))
        for i in range(len(Re)):
            f[i] = f_colebrook_white(Dh, epsilon, Re[i], N)
            
        ### Plotstuff
        ... # (TODO)
        
        
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

    ### Laminar case
    if Re < 2100: return 64/Re

    ### Initial guesss
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
    
    ### Laminar case
    if Re < 2100: return 64/Re

    return (2*log10(epsilon/(3.7*Dh) + (7/Re)**.9))**-2


### Generate Moody Diagram
### ----------------------
def moody(method="Colebrook-White", epsilon_vec=None):
    '''
    Generates fricton factor curves for various relative
    roughnesses (aka a Moody Diagram).
    
    Inputs:
        method      = (string) type of friction factor calculation
        epsilon_vec = (vector) relative roughnesses to evaluate
    '''
    
    ### Verify friction factor calculation method
    if method == "Colebrook-White": f_func = f_colebrook_white
    elif method == "Churchill": f_func = f_churchill
    
    ### Populate relative roughnesses if custom ones weren't provided
    if epsilon_vec == None:
        epsilon_vec = [5e-2, 4e-2, 3e-2, 2e-2, 1e-2, 5e-3, 2e-3, 1e-3, \
                       5e-4, 2e-4, 1e-4, 5e-5, 1e-5, 5e-6, 1e-6, 1e-7]

    ### Preallocate
    Re = np.logspace(2, 9, num=100)
    f = np.zeros(100)

    ### Reference diameter ratios by exit diameter
    
    ### Calculate loss coefficients and plot
    fig, ax = plt.subplots()
    for epsilon in epsilon_vec:  # skip do=0
        for i in range(100):
            f[i] = f_func(1, epsilon, Re[i])
                
        plt.plot(Re, f, label=f"$relative roughness$={epsilon}") 
    
    ### Decorate
    plt.title("Moody Diagram via " + method + " Formula")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(5e2, 1e9)
    plt.ylim(.005, .1)
    plt.xlabel("$Re$")
    plt.ylabel("$f$")
    plt.grid(True, which='both')

    plt.legend(fontsize=8, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


### -------------------------- ###
### Flow Resistance Estimation ###
### -------------------------- ###

### K-factor due to friction
### ------------------------
def calc_K_friction(f, l, d):
    '''
    Inputs:
        f = (scalar) friction factor
        l = (scalar) [m] pipe length
        d = (vector) [m] pipe diameter
    '''
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
        6.6*f*(sqrt(sin(a/2)) + sin(a/2))/(r/d)**(4*a/pi)

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