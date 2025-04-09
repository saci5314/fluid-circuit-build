'''
Supersonic converging-diverging nozzle lumped element object.

Author(s):
    Samuel Ciesielski
'''

from network import element

import math
import numpy as np
from scipy.constants import pi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator



class thrust_chamber(element):

    ### CONSTRUCTOR
    ### -----------
    def __init__(self, name):
        super().__init__(name) # call parent class constructor

        ### Ideal operating conditions
        self.of = None # ox/fuel mass ratio

        ### Propellants 
        self.ox = None # string indicating oxidizer type
        self.fuel = None # string indicating fuel type

        ### Geometry 
        self.l_c = None # [m] chamber length
        self.d_c = None # [m] chamber diamteter
        self.d_t = None # [m] throat diameter
        self.d_e = None # [m] exit diameter
        self.theta_c = None # [deg] converging angle
        self.theta_d = None # [deg] converging angle, if applicable

        ### Internal mesh data
        self.x = [] # [m] axial nozzle spline points
        self.r = [] # [m] inner mold line (IML) radii



### -------------------------------- ###
### Combustin Gas Thermochem Methods ###
### -------------------------------- ###

### Import CEA data as dictionary
### -----------------------------
def import_cea_data(cea_file_path, N_locs=2):
    '''
    Input:
        cea_file_path = (string) path to cea tabulated output
                                 accepts .txt or .csv files
        N_locs = (int) number of stations in CEA output
                       1 = chamber
                       2 = throat
                       3 = exit

    Output:
        cea_dict = (dictonary) gas property data
    '''
    
    ### Preallocate dictionary to store data
    cea_data = dict()
    
    ### Open file path
    with open(cea_file_path, "r") as cea_file:
        lines = cea_file.readlines() # getlines
        pull = False # indicator to pull character
        new_value = ""
        loc = 0
        ent = 0
        
        # Getline
        for i in range(0, len(lines)):
            key = 0
            
            # Parse through characters in line
            J = len(lines[i])
            for j in range(J):
                
                # Detect if character should be pulled
                if pull == False and lines[i][j] != " ":
                    pull = True
                    
                # Detect if character shouldn't be pulled
                elif pull == True and (lines[i][j] == " " or j == J-1):
                    pull = False
                    
                    # Allocate space for data
                    if i == 0:
                        cea_data[new_value] = np.zeros([int((len(lines)-1)/N_locs), N_locs])
                    
                    # Pull entry 
                    else:
                        cea_data[list(cea_dict.keys())[key]][ent][loc] = float(new_value)
                        key += 1
                    
                    # Reset
                    new_value = ""
                    
                # Add character to value being pulled
                if pull == True:
                    new_value += lines[i][j]
                    
            # Indexing pain
            if i > 0:
                loc += 1
                if loc == N_locs: 
                    loc = 0
                    ent += 1
                    
    return cea_data


                            
### Trade CEA gas props across operating conditions
### -----------------------------------------------
def propellant_trade_space(cea_data, P_c_range, of_range):
    '''
    Generates 3d surface plots for Isp and chamber stag temp
    at various pressures and mixture ratios.
    
    Inputs:
        cea_data  = (dictionary) gas property data
        P_c_range = (vector) desired chamber pressure range
        of_range  = (vector) desired mixture ratio range 
    '''
    
    ### Preallocate
    P_c, of = np.meshgrid(P_c_range, of_range)
    z_data = np.zeros([len(of_range), len(P_c_range)])
    

    ### Pull data from supplied fields and plot
    ### Right now just consdering stag temp and specific impulse
    n = 0 # sublot indicator
    for field in cea_data.keys():
        # Detect parameter to plot
        match field:
            case "isp":
                title = "Specific Impulse (s)"
                loc_ind = 1
            case "t":
                title = "Chamber Temperature (K)"
                loc_ind = 0
                
        # Pull data for detected parameter across requested 
        # operating conditions
        k = 0
        for i in range(len(of_range)):
            for j in range(len(P_c_range)):
                z_data[i][j] = cea_data[field][k][loc_ind]
                k += 1
        
        # Plotstuff
        n += 1
        fig = plt.figure(figsize=plt.figaspect(1/len(cea_dict.keys())))
        ax = fig.add_subplot(1, 2, n, projection='3d')
        ax.plot_surface(P_c, of, z_data)
        ax.set_xlabel("Chamber Pressure (psi)")
        ax.set_ylabel("O/F Ratio")
        ax.set_zlabel(title)
        ax.set_zlim(0, z_data.max()*1.2)
        plt.show()



### TRADE CEA PROPELLANT PROPS ACROSS OPERATING CONDITIONS
### ------------------------------------------------------
def ideal_mdot(F_t, gamma, R, T_c):
    '''
    Inputs:
        F_t = (scalar) [N] target thrust
        gamma
    '''

    return F_t/nozzle.ideal_exit_vel()

def ideal_exit_vel(a_t, P_i, P_e, gamma):
    '''
    Inputs:
        a_t = (scalar) [m/s] flow velocity at sonic conditions
        P_i = (scalar) [Pa] nozzle inlet pressure
        P_e = (scalar) [Pa] ideal exit pressure
        gamma = (scalar) specific heat ratio at sonic conditions

    Outputs:
        v_e = (scalar) [m/s] ideal exit velocity
    '''
    return a_t*math.sqrt((gamma+1)/(gamma-1) * (1 - (P_e/P_i))**((gamma-1)/gamma))