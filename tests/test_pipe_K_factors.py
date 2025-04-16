'''
Qualitative tests of friction factors and loss coefficients for pipes
of various geometric configurations. All formulas and plots are from [1].

Sources:
    [1] D. C. Rennels, H. M. Hudson, "Pipe Flow: A Comprehensive and 
        Practical Guide," John Wiley & Sons, 2012.
    
'''

import sys
import os
sys.path.append(os.path.abspath("../src"))

import numpy as np
import matplotlib.pyplot as plt



### Moody diagram for Colebrook-White formula
### -----------------------------------------
def test_f_colebrook_white():
    pipe.moody()
    
    
### Moody diagram for Churchill's formula
### -------------------------------------
def test_f_churchill():
    pipe.moody("Churchill")
    
    
### Moody diagram for Colebrook-White formula
### -----------------------------------------
def test_K_bend():
    ### Test for data at Re=20,000
    Re = 20000
    f = .0259
    alpha_vec = [45, 90, 135, 180]
    r = np.linspace(.5, 15, 100)
    K = np.zeros(100)

    # Calc loss coefficients for all relevant angles and plot
    for alpha in alpha_vec:
        for i in range(100):
            K[i] = pipe.calc_K_bend(f, 1, r[i], alpha)
        plt.plot(r, K, label=f"Bend angle={alpha:.2f}") 
    
    # Decorate
    plt.title("Pipe Bend Loss Coefficients @ Re=20,000, f=.0259",)
    plt.suptitle('Compare to Rennels & Hudson Figure 15.5', fontsize=10, x=.37, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([.5, 15])
    plt.ylim([0, 1])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    ### Test for data at Re=200,000
    Re = 200000
    f = .0158
    alpha_vec = [45, 90, 135, 180]
    r = np.linspace(.5, 15, 100)
    K = np.zeros(100)

    # Calc loss coefficients for all relevant angles and plot
    for alpha in alpha_vec:
        for i in range(100):
            K[i] = pipe.calc_K_bend(f, 1, r[i], alpha)
        plt.plot(r, K, label=f"Bend angle={alpha:.2f}") 
    
    # Decorate
    plt.title("Pipe Bend Loss Coefficients @ Re=200,000, f=.0158",)
    plt.suptitle('Compare to Rennels & Hudson Figure 15.6', fontsize=10, x=.37, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([.5, 15])
    plt.ylim([0, 1])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    ### Test for data @ Re=1,000,000
    Re = 1000000
    f = .0120
    alpha_vec = [30, 45, 75, 90]
    r = np.linspace(.5, 5, 100)
    K = np.zeros(100)

    # Calc loss coefficients for all relevant angles and plot
    for alpha in alpha_vec:
        for i in range(100):
            K[i] = pipe.calc_K_bend(f, 1, r[i], alpha)
        plt.plot(r, K, label=f"Bend angle={alpha:.2f}") 
    
    # Decorate
    plt.title("Pipe Bend Loss Coefficients @ Re=1,000,000, f=.0120",)
    plt.suptitle('Compare to Rennels & Hudson Figure 15.7', fontsize=10, x=.37, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([.5, 5])
    plt.ylim([0, .8])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()