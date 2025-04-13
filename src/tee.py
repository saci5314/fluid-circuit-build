'''
Manifold object for lumped element modeling.

Author:
    Samuel Ciesielski

Sources:
    [1] D. C. Rennels, H. M. Hudson, "Pipe Flow: A Comprehensive and 
        Practical Guide," John Wiley & Sons, 2012.
'''

from network import Element

class Tee(Element):
    
    ### CONSTRUCTOR
    ### -----------
    def __init__(self, name, config):
        super().__init__(name, 3)
        
        if config == "converging" or config == "diverging":
            self.config = config
        else:
            raise Exception("Tee must be either \"converging\" or \"diverging\".")
                            
            
            
    ### Pull steady flow equations
    ### --------------------------
    def steady_flow_eqns(self, statevars, N_sv, rho):
        ### Relevant state variables
        P_1 = statevars[self.ports[0]]
        P_2 = statevars[self.ports[1]]
        P_3 = statevars[self.ports[2]]
        mdot_1 = statevars[N_sv/2 + self.ports[0]]
        mdot_2 = statevars[N_sv/2 + self.ports[1]]
        mdot_3 = statevars[N_sv/2 + self.ports[2]]
        
        return [
            # Steady-state momentum equations
            P_1 - P_2,
            P_1 - P_3,
            
            # Mass continuity equation
            mdot_1 - mdot_2 - mdot_3
        ]
        