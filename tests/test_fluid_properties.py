'''
Qualitative tests for thermalfluid property models.

'''

import sys
import os
sys.path.append(os.path.abspath("../src"))



import fluid
import numpy as np
import matplotlib.pyplot as plt



### Plot raw and interpolated data for specific fluid
### -------------------------------------------------
def test_interp_data(fluid_name):
    ### Raw data
    T_data, rho_data, cp_data, k_data, mu_data = fluid.import_data(fluid_name)
   
    ### Interpolation
    T = np.linspace(min(T_data), max(T_data), 1000)
    rho = fluid.interp_rho(fluid_name, T)
    cp = fluid.interp_cp(fluid_name, T)
    k = fluid.interp_k(fluid_name, T)
    mu = fluid.interp_mu(fluid_name, T)
    
    ### Plotstuff
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.plot(T_data, rho_data, marker='.', linestyle='')
    plt.plot(T, rho)
    plt.title("Density")
    plt.legend(["Raw Data", "Interpolation"])
    plt.xlabel("Temperature [K]")
    plt.ylabel("kg/m^3")

    plt.subplot(2, 2, 2)
    plt.plot(T_data, cp_data, marker='.', linestyle='')
    plt.plot(T, cp)
    plt.title("Specific Heat Capacity")
    plt.legend(["Raw Data", "Interpolation"])
    plt.xlabel("Temperature [K]")
    plt.ylabel("J/(kg*K)")
    
    plt.subplot(2, 2, 3)
    plt.plot(T_data, k_data, marker='.', linestyle='')
    plt.plot(T, k)
    plt.title("Conductivity")
    plt.legend(["Raw Data", "Interpolation"])
    plt.xlabel("Temperature [K]")
    plt.ylabel("W/(m*K)")

    plt.subplot(2, 2, 4)
    plt.plot(T_data, mu_data, marker='.', linestyle='')
    plt.plot(T, mu)
    plt.title("Dynamic Viscocity")
    plt.legend(["Raw Data", "Interpolation"])
    plt.xlabel("Temperature [K]")
    plt.ylabel("Pa*s")
    
    plt.tight_layout()
    plt.show()