'''
Orifice plate object for lumped element modeling and straight-orifice 
resistance/discharge coefficient estimation formulas for hand calculations.

Relations provided here should be restricted to incompressible flows, or 
compressible flows for where the pressure drop incurred across the orifice
plate is << the upstream pressure.

Author:
    Samuel Ciesielski

Sources:
    [1] D. C. Rennels, H. M. Hudson, "Pipe Flow: A Comprehensive and 
        Practical Guide," John Wiley & Sons, 2012.

'''

from network import Element
import numpy as np
from math import sqrt
from scipy.constants import pi



class Orifice(Element):

    ### CONSTRUCTOR
    ### -----------
    def __init__(self, name, do, lo=0, N=1):
        '''
        Inputs:
            name    = (string) component ID, part number, etc.
            do      = (scalar) [m] orifice dimaeter
            lo      = (scalar) [m] orifice length
            N       = (scalar) number of orifices in orifce plate
        '''
        ### Call p
        super().__init__(name, 2)

        ### Geometry
        self.do = do         
        self.Ao = pi*do**2/4 
        self.lo = lo
        self.N = N



    ### ------------- ###
    ### Dynamics Data ###
    ### ------------- ###

    ### Assign custom K-factors
    ### -----------------------
    def set_Ko(self, Ko):
        self.Ko = Ko
        self.Knet = Ko/self.N**2

    def set_Knet(self, Knet):
        self.Ko = Knet*self.N**2
        self.Knet = Knet

    ### Fit K-factor from test data
    ### ---------------------------
    def fit_K(self, mdot_test, dP_test, rho_test):
        '''
        Inputs:
            mdot_vec    = (vector) [kg/s] massflow data points
            deltaP_vec  = (vector) [Pa] (vector) pressure drop data points
            rho_vec     = (vector) [kg/m^3] test fluid density data points
        '''
        
        ### Calc avg orifice plate resistance from each datapoint
        Knet_datapoints = np.zeros(len(mdot_test))
        for i in range(0, len(mdot_test)):
            Knet_datapoints[i] = (2*self.Ao**2 * rho_test[i]) * \
                                 (dP_test[i]/mdot_test[i])
            
        ### Assign total average orifice plate resistance from all datapoints
        self.set_Knet(np.mean(Knet_datapoints),self.N, self.do)

    ### Pull inertance
    ### --------------
    def I(self, rho):
        return rho * self.lo/self.Ao # [kg/m^4]

    ### Pull quadratic damping load
    ### ---------------------------
    def dP_damping(self, mdot_tot, rho):
        return self.Ko * (mdot_tot/self.N)**2 / (2*self.Ao**2 * rho) # [Pa]

    ### Pull volume load
    ### ----------------
    def dP_body(self):
        return 0

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
            P_2 - P_1 - self.dP_damping(mdot_1, rho),
            
            # Mass continuity equation
            mdot_2 - mdot_1
        ]

### -------------------------- ###
### Flow resistance estimation ###
### -------------------------- ###
### aka "K-factor"
### aka "flow coefficient"
### aka "loss factor"

### Sharp-edged geometry cases
### --------------------------
def calc_K_sharp(N, lo, do, d1, d2):
    '''
    Calculates K-factor for orifice with shap edge per [1].

    Inputs:
        N  = (scalar) number of orifices in orifice plate
        lo = (scalar) orifice length
        do = (scalar) orificie diameter
        d1 = (scalar) upstream pipe diameter
        d2 = (scalar) downstream pipe diameter
    '''

    ### Diameter ratio
    beta = do/d1

    ### Jet velocity ratio
    lamb = 1 + 0.622*(1 - .215*beta**2 + .785*beta**5)

    ### Thin plate case
    if lo/do < .2:
        # single orifice resistance
        Ko = .0696*(1 - beta**5)*lamb**2 + (lamb - (do/d2)**2)**2

    ### Thick plate case
    elif .2 <= lo/do < 1.4:
        # thick-edge correction coefficient
        Cth = (1 - .5*(lo/(1.4*do))**2.5 - .5*(lo/(1.4*do))**3)**4.5

        # single orifice resistance
        Ko = .0696*(1 - beta**5)*lamb**2 + Cth*(lamb - (do/d2)**2)**2 + \
                (1 - Cth)*((1 - lamb)**2 + (1 - (do/d2)**2)**2)

    elif lo/do >= 1.4:
        warnings.warn("Orifices with an l/d >= 1.4 are not supported yet. \
                      Need to add friction estimation onboard orifice object.")

    ### Orifice plate total resistance
    Knet = Ko/N**2

    return Ko, Knet

### Filleted geometry cases
### -----------------------
def calc_K_rounded(N, do, d1, d2, r):
    '''
    Calculates K-factor for orifice with filleted edge per [1].

    Inputs:
        N  = (scalar) number of orifices in orifice plate
        lo = (scalar) orifice length
        do = (scalar) orifice diameter
        d1 = (scalar) upstream pipe diameter
        d2 = (scalar) downstream pipe diameter
        r  = (scalar) fillet radius      
    '''

    ### Diameter ratio
    beta = do/d1

    ### Jet contraction ratio for small radius case
    if r/do <= 1:
        lamb = 1 + .622*(1 - .3*sqrt(r/do) - .70*(r/do))**4 * \
                   (1 - .215*beta**2 - .785*beta**5)

    ### Jet contraction ratio for large radius case
    elif r/do > 1: 
        lamb = 1

    ### Single orifice resistance 
    Ko = .0696*(1 - .569*(r/do))*(1 - sqrt(r/do)*beta) * \
            (1 - beta**5)*lamb**2 + (lamb**2 - (do/d2)**2)**2

    ### Orifice plate total resistance
    Knet = Ko/N**2

    return Ko, Knet

### Beveled geometry cases
### ----------------------
def calc_K_beveled(N, lo, do, d1, d2, theta):
    '''
    Calculates K-factor for orifice with beveled edge per [1].

    Inputs:
        N     = (scalar) number of orifices in orifice plate
        lo    = (scalar) orifice length
        do    = (scalar) orifice diameter
        d1    = (scalar) upstream pipe diameter
        d2    = (scalar) downstream pipe diameter
        theta = (scalar) [deg] bevel angle relative to flow direction
    '''

    ### Diameter ratio
    beta = do/d1

    ### Bevel coefficient
    Cb = (1 - theta/90) * (theta/90)**(1/(2 + lo/do))

    ### Jet velocity ratio
    lamb = 1 + .622*(1 - Cb*(lo/do)**((1 - (lo/do)**.25)/2))

    ### Single orifice resistance
    Ko = .0696*(1 - Cb*(lo/do))*(1 - .42*sqrt(lo/do)*beta**2) * \
            (1 - lamb**5)*lamb**2 + (lamb - (do/d2)**2)**2

    ### Orifice plate total resistance
    Knet = Ko/N^2

    return Ko, Knet



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