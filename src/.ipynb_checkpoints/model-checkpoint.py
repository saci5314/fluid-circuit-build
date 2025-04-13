'''
The Model object contains methods for solving steady-state
and frequency domain (chugging) incompressible fluid flow problems.

Author(s):
    Samuel Ciesielski
    
Source(s):
    [1] B. W. Oppenheim, S. Rubin, "Advanced POGO Stability Analysis for
        Liquid Rockets," The Aerospace Corporation, AIAA-92-2454-CP.

'''

from network import Network, Element, Node, Boundary
from pipe import Pipe
from 
import numpy as np
from scipy.optimize import root



class Model:
    
    ### Base Constructor
    ### ----------------
    def __init__(self, circuit):
        ### Fluid system network, circuit, mesh, etc.
        if not isinstance(circuit, Network):
            raise TypeError("Model must be initalized with a network object.")
        self.circuit = circuit
        
        ### Qty elements, nodes, and state variables
        self.N_el = len(circuit.elements)
        self.N_nodes = len(circuit.nodes)
        self.N_sv = 2*self.N_nodes 
        
        ### Boundary conditions
        self.P_bc = np.array([None]*self.N_nodes)
        self.mdot_bc = np.array([None]*self.N_nodes)
        
        ### Steady-state solution data
        self.P_steady = np.array([None]*self.N_nodes)
        self.mdot_steady = np.array([None]*self.N_nodes)
        
        ### Linearized system dynamics matricies
        self.M = np.zeros((self.N_sv, self.N_sv))
        self.C = np.zeros((self.N_sv, self.N_sv))
        self.K = np.zeros((self.N_sv, self.N_sv))
        
        ### Frequency domain solution data
        self.f_n = ... # natural frequencies
        self.omega_n = ... # circular f_n (system eigenvalues) 


        
    ### ---------------- ###
    ### Model Definition ###
    ### ---------------- ###
        
    ### Assign boundary conditions
    ### --------------------------
    def add_BC(self, BC_type, node, value):
        ### Check that node is boundary node
        if isinstance(self.circuit.nodes[node], Boundary):
            print("Requested node" + str(node) + "is not a boundary node.")
            return
        
        ### Assign boundary condition
        if BC_type == "pressure":
            self.P_bc[node] = value
        elif BC_type == "flowrate":
            self.mdot_bc[node] = value
        else:
            print("Invalid boundary condition. Must specify either" \
                  "\"pressure\" or \"flowrate\".")        
        
        
    ### View configured boundary conditions
    ### -----------------------------------
    def view_BCs(self):
        for i, node in enumerate(self.circuit.nodes):
            if isinstance(node, Boundary):
                print("Boundary conditions at node" + str(i) + ":")
                
                # Pressure BCs
                if self.P_bc[i] is not None:
                    print("   P = ", self.P_bc, "Pa")
                    
                # Flowrate BCs
                if self.mdot_bc[i] is not None:
                    print("   mdot = ", self.mdot_bc, "Pa")
                    
                # No BCs present
                if self.P_bc[i] is None and self.mdot_bc[i] is None:
                    print("No conditions defined.")

                    
        
    ### -------------------- ###
    ### Steady-state Methods ###
    ### -------------------- ###
    
    
    ### Construct nonlinear system
    ### --------------------------
    def build_steady_system(self, statevars):
        ### Build system of nonlinear equations
        ### constraining each element in fluid circuit
        eqns = []
        for i, element in enumerate(self.circuit.elements):
            eqns.extend(element.steady_flow_eqns(statevars, \
                                                 self.N_sv, \
                                                 self.fluids[i].rho()))
        
        ### Model checks
        if len(eqns) < self.N_sv:
            raise Exception("Number of equations in steady-state problem" \
                            "is less than the number of state variables.")
        elif len(eqns) > self.N_sv:
            raise Exception("Number of equations in steady-state problem" \
                            "is greater than the number of state variables.")   
        
        ### Nominal qty of equations have been added
        else:
            return np.array(eqns)
    
    
    ### Steady-state solver
    ### -------------------
    def steady_solve(self):
        ### Build nonlinear system of equations
        eqns = self.build_steady_system 
        
        ### Develop initial guess
        sol_0 = np.ones(self.N_sv)
        
        ### Rootfinding
        steady_sol = root(eqns, sol_0)
        
        ### Pull variables
        self.P_steady = steady_sol[0:self.N_nodes-1]
        self.mdot_steady = steady_sol[self.N_nodes:self.N_sv-1]
        
    
    ### Solution View Options
    ### ---------------------
    def print_steady_data(self):
        ### Steady pressures
        print("Steady state pressures: ")
        for i in range(self.N_nodes):
            print("   Node " + str(i) + ": " + str(self.P_steady[i]) + " Pa")
            
        ### Steady flowrates
        print("Steady state flow rates: ")
        for i in range(self.N_nodes):
            print("   Node " + str(i) + ": " + str(self.mdot_steady[i]) + " kg/s")
            
    def plot_steady_data(self):
        ... # (TODO)
        
    
    
    ### ------------------------ ###
    ### Frequency Domain Methods ###
    ### ------------------------ ###
    
    
    ### Construct linearized dynamics matricies
    ### ---------------------------------------
    def build_dynamics_mats(self):
        ... # (TODO)
        
        
    ### Natural frequency eignesolver
    ### -----------------------------
    def eigen_solve(self):
        ... # (TODO)
        
        
    ### Solution View Options
    ### ---------------------
    def print_freq_domain_data(self):
        ... # (TODO)
        
    def plot_freq_domain_data(self):
        ... # (TODO)