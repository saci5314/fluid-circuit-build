'''
Qualitative tests of loss coefficients for orifices of various
geometric configurations. All formulas and plots are from [1].

Sources:
    [1] D. C. Rennels, H. M. Hudson, "Pipe Flow: A Comprehensive and 
        Practical Guide," John Wiley & Sons, 2012.
    
'''

import sys
import os
sys.path.append(os.path.abspath("../src"))

import orifice
import numpy as np
import matplotlib.pyplot as plt




### Thin, sharp-edged orifices in transition section
### ------------------------------------------------
def test_K_sharp():
    ### Preallocate
    B = np.linspace(0.01, 1, 100)
    K = np.zeros(100)

    ### Reference diameter ratios by exit diameter
    d2 = 1
    
    ### Calculate loss coefficients and plot
    for do in np.linspace(0.1, d2, 10):  # skip do=0
        for i in range(100):
            K[i], _ = orifice.calc_K_sharp(1, do, do/B[i], d2, -1)
        plt.plot(B, K, label=f"$d_o$/$d_2$={do:.2f}") 
    
    ### Decorate
    plt.title("Thin, Sharp-edged Orifice Loss Coefficients in Transition Section",)
    plt.suptitle('Compare to Rennels & Hudson Diagram 13.1', fontsize=10, x=.45, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([0, 1])
    plt.ylim([0, 3])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    
### Thin, rounded-edge orifices ins straight pipe
### ---------------------------------------------
def test_K_rounded():
    ### Preallocate
    B = np.linspace(0.01, 1, 100)
    K = np.zeros(100)

    ### Reference geometry from orifice diameter
    do = 1
    r_vec = do*np.array([.001, .01, .03, .05, .08, .12, .20, .30, .50, 1.00])

    ### Calculate loss coefficients for various r/do ratios and plot
    for r in r_vec:
        for i in range(100):
            K[i], _ = orifice.calc_K_rounded(1, do, do/B[i], do/B[i], r)
        plt.plot(B, K, label=f"$r$/$d_o$={r/do:.2f}") 
    
    ### Calculate loss coefficients at rounding limit and plot
    for i in range(100):
        r = (do/B[i] - 1)/2 # limit radius
        K[i], _ = orifice.calc_K_rounded(1, do, do/B[i], do/B[i], r)
    plt.plot(B, K, 'k--', label=f"Rounding Limit") 
        
    ### Decorate
    plt.title("Thin, Rounded-edged Orifice Loss Coefficients in Straight Pipe Section",)
    plt.suptitle('Compare to Rennels & Hudson Diagram 13.2', fontsize=10, x=.45, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([0, 1])
    plt.ylim([0, 3])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    
### Thin, beveled-edge orifices ins straight pipe
### ---------------------------------------------
def test_K_beveled():
    ### Preallocate
    B = np.linspace(0.01, 1, 100)
    K = np.zeros(100)

    ### Reference geometry from orifice diameter
    do = 1
    l_vec = do*np.array([.001, .02, .05, .10, .20, .50, 1.00])

    ### Calculate loss coefficients for a 15 degree bevel at various l/do ratios
    alpha = 15
    for l in l_vec:
        for i in range(100):
            K[i], _ = orifice.calc_K_beveled(1, do, do/B[i], do/B[i], l, alpha)
        plt.plot(B, K, label=f"$l$/$d_o$={l/do:.2f}") 
    
    ### Calculate loss coefficients at bevel limit and plot
    for i in range(100):
        l = (do/B[i] - do)/(2*np.tan(alpha*(2*np.pi/360))) # limit length
        K[i], _ = orifice.calc_K_beveled(1, do, do/B[i], do/B[i], l, alpha)
    plt.plot(B, K, 'k--', label=f"Bevel Limit") 
        
    ### Decorate
    plt.title("Thin, " + str(alpha) + "$^o$ Beveled-edge Orifice Loss Coefficient in Straight Pipe Section")
    plt.suptitle('Compare to Rennels & Hudson Diagram 13.4', fontsize=10, x=.45, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([0, 1])
    plt.ylim([0, 3])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    
    ### Calculate loss coefficients for a 45 degree bevel at various l/do ratios
    alpha = 45
    for l in l_vec:
        for i in range(100):
            K[i], _ = orifice.calc_K_beveled(1, do, do/B[i], do/B[i], l, alpha)
        plt.plot(B, K, label=f"$l$/$d_o$={l/do:.2f}") 
    
    ### Calculate loss coefficients at bevel limit and plot
    for i in range(100):
        l = (do/B[i] - do)/(2*np.tan(alpha*(2*np.pi/360))) # limit length
        K[i], _ = orifice.calc_K_beveled(1, do, do/B[i], do/B[i], l, alpha)
    plt.plot(B, K, 'k--', label=f"Bevel Limit") 
        
    ### Decorate
    plt.title("Thin, " + str(alpha) + "$^o$ Beveled-edge Orifice Loss Coefficient in Straight Pipe Section")
    plt.suptitle('Compare to Rennels & Hudson Diagram 13.6', fontsize=10, x=.45, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([0, 1])
    plt.ylim([0, 3])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    
    ### Calculate loss coefficients for a 45 degree bevel at various l/do ratios
    alpha = 75
    for l in l_vec:
        for i in range(100):
            K[i], _ = orifice.calc_K_beveled(1, do, do/B[i], do/B[i], l, alpha)
        plt.plot(B, K, label=f"$l$/$d_o$={l/do:.2f}") 
    
    ### Calculate loss coefficients at bevel limit and plot
    for i in range(100):
        l = (do/B[i] - do)/(2*np.tan(alpha*(2*np.pi/360))) # limit length
        K[i], _ = orifice.calc_K_beveled(1, do, do/B[i], do/B[i], l, alpha)
    plt.plot(B, K, 'k--', label=f"Bevel Limit") 
        
    ### Decorate
    plt.title("Thin, " + str(alpha) + "$^o$ Beveled-edge Orifice Loss Coefficient in Straight Pipe Section")
    plt.suptitle('Compare to Rennels & Hudson Diagram 13.8', fontsize=10, x=.45, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d_1$")
    plt.xlim([0, 1])
    plt.ylim([0, 3])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()
    
    
### Thick, sharp-edged orifice in straight pipe
### -------------------------------------------
def test_K_thick():
    ### Preallocate
    B = np.linspace(0.01, 1, 100)
    K = np.zeros(100)

    ### Reference geometry from orifice diameter
    do = 1
    t_vec = do*np.linspace(.1, 1.4, 14)

    ### Calculate loss coefficients and plot
    for t in t_vec:
        for i in range(100):
            K[i], _ = orifice.calc_K_sharp(1, do, do/B[i], do/B[i], t)
        plt.plot(B, K, label=f"$t$/$d_o$={t/do:.2f}") 
    
    ### Decorate
    plt.title("Thick, Sharp-edged Orifice Loss Coefficient in Straight Pipe Section",)
    plt.suptitle('Compare to Rennels & Hudson Diagram 13.1', fontsize=10, x=.45, y=.15)  
    plt.ylabel("$K_o$")
    plt.xlabel("$d_o$/$d$")
    plt.xlim([0, 1])
    plt.ylim([0, 3])
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()