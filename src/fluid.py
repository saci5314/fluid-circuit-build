'''
Functions and class object for pulling temperature-dependent 
heat transport properties of common propellants.

Author:
    Samuel Ciesielski

Sources:

    [1] L.E. Faith, G.H. Ackerman, H.T. Henderson, "Heat Sink Capabilites
        of Jet A Fuel: Heat Transfer and Coking Studies"

'''



class Fluid:
    
    ### Constructor
    ### -----------
    def __init__(self, name=None):
        if name is not None:
            self.name = name
            
            
        

### Helper for interpolating fluid props 
## 
def interp_props(fluid, prop, T):
    ### Import data for requested property
    ...
    
    ### Interpolate
    ...
    

### Density data
### ------------
def density(fluid, T=T_STP):
    return interp_props(fluid, T)


### Specific heat capacity
### ----------------------
def heat_capacity(fluid, T=T_STP):
    return interp_props(fluid, "cp", T)


### Conductivity
### ------------
def conductivity(fluid, T=T_STP):
    return interp_props(fluid, "k", T)


### Dymamic viscocity
### -----------------  
def viscocity(fluid, T=T_STP):
    return interp_props(fluid, "mu", T)


### Request all thermal transport props
### -----------------------------------
def transport_props(fluid, T=T_STP):
    cp = heat_capacity(fluid, T)
    k = conductivity(fluid, T)
    mu = viscocity(fluid, T)
    
    return cp, k, mu
    
    
### Plots all transport data for specific fluid
### -------------------------------------------
def plot_prop_data():
    ...