'''
Functions and class for pulling temperature-dependent 
heat transport properties of common propellants.

Author:
    Samuel Ciesielski

Sources:

    [1] L.E. Faith, G.H. Ackerman, H.T. Henderson, "Heat Sink Capabilites 
        of Jet A Fuel: Heat Transfer and Coking Studies", Shell Development
        Company, 1971.
        
    [2] ...
        
'''

import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt



# Available fluid models
fluids = ["JetA"]

# STP Temperature
T_STP = 273.15 # [K]



class Fluid:
    
    ### Constructor
    ### -----------
    def __init__(self, fluid=None):
        if fluid is not None: self.assign(fluid)

        
    ### Assign specific fluid
    ### ---------------------
    def assign(self, fluid):
        self.T_data, \
        self.rho_data, \
        self.cp_data, \
        self.k_data, \
        self.mu_data = import_data(fluid)
        
        self.fluid = fluid
        
        
    ### Pull specific property at specific temperature
    ### ----------------------------------------------
    def rho(self, T=T_STP):
        return interp1d(self.T_data, self.rho_data, kind='cubic')(T)
    
    def cp(self, T=T_STP):
        return interp1d(self.T_data, self.cp_data, kind='cubic')(T)
    
    def k(self, T=T_STP):
        return interp1d(self.T_data, self.k_data, kind='cubic')(T)
        
    def mu(self, T=T_STP):
        return interp1d(self.T_data, self.mu_data, kind='cubic')(T)

        
        
### Import raw data for specific fluid
### ----------------------------------
def import_data(fluid_name):
    # Check if fluid is valid
    if fluid_name not in fluids:
        raise Exception("Invalid fluid:" + fluid_name)
        
    # Get fluid.py directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    # Build path to file containing property data
    data_path = os.path.join(module_dir, '..', \
                                         'src', \
                                         'fluid_data', \
                                         str(fluid_name)+"_data.csv")

    # Pull into dataframe
    data = pd.read_csv(os.path.abspath(data_path))
    
    # Return as numpy arrays
    T_data = np.array(data["T"])
    rho_data = np.array(data["rho"])
    cp_data = np.array(data["cp"])
    k_data = np.array(data["k"])
    mu_data = np.array(data["mu"])

    return T_data, rho_data, cp_data, k_data, mu_data
    
    
### Interpolate data for specific properties
### ----------------------------------------
def interp_rho(fluid, T):
    T_data, rho_data, _, _, _ = import_data(fluid)
    return interp1d(T_data, rho_data, kind='cubic')(T)
    
def interp_cp(fluid, T):
    T_data, _, cp_data, _, _ = import_data(fluid)
    return interp1d(T_data, cp_data, kind='cubic')(T)

def interp_k(fluid, T):
    T_data, _, _, k_data, _ = import_data(fluid)
    return interp1d(T_data, k_data, kind='cubic')(T)

def interp_mu(fluid, T):
    T_data, _, _, _, mu_data = import_data(fluid)
    return interp1d(T_data, mu_data, kind='cubic')(T)



