'''
Objects and methods for building lumped element mesh.

Author(s):
    Samuel Cieselski

'''


class Network:

    ### Constructor
    ### -----------
    def __init__(self, source):
        self.mesh(source)
  
    ### Meshing by breadth-first traversal
    ### ----------------------------------
    def mesh(self, source):
        ### Build network by BFS from source component
        self.elements = [source]
        self.nodes = []
        
        queue = [source]
        while queue:
            
            # Parse through neighbors of element at queue top
            for n, neighbor in enumerate(queue[0].neighbors):
                
                # Case 1: boundaries (no neighbor present)
                if neighbor is None: 
                    self.update_boundary(queue[0], n)
                    
                # Case 2: neighbor is unaccounted for
                elif neighbor not in self.elements:
                    self.update_connection(queue[0], neighbor, n)

                    # push component to network and queue for further BFS
                    self.elements.append(neighbor)
                    queue.append(neighbor)
                    
                # Case 3: neighbor is accounted-for, but missing connection
                elif queue[0].ports[n] is None: 
                    self.update_connection(queue[0], neighbor, n)

            queue.pop(0)
            
    ### Meshing helper funcs
    ### --------------------
    def update_boundary(self, top, n):
        self.nodes.append(Boundary())
        top.ports[n] = len(self.nodes) - 1

    def update_connection(self, top, neighbor, n):
        # Build connection to neighbor
        self.nodes.append(Connection())
        top.ports[n] = len(self.nodes) - 1

        # Build connection from neighbor
        for m, second_neighbor in enumerate(neighbor.neighbors):
            if second_neighbor is top:
                neighbor.ports[m] = len(self.nodes) - 1
                    
    ### Qualitative mesh checks
    ### -----------------------
    def mesh_checks(self):
        ### List all nodes by type
        connections = []
        boundaries = []
        for n, node in enumerate(self.nodes):
            if isinstance(node, Connection):
                connections.append(n)
            elif isinstance(node, Boundary): 
                boundaries.append(n)
                
        print("Bulk nodes: ", connections)
        print("Boundary nodes: ", boundaries)
              
        ### List all nodes by element
        print("\nNodes by element: ")
        print("-----------------")
        for i, element in enumerate(self.elements):
            print(element.name+":", element.ports) 
            
        ### List all neighbors of each element
        print("\nNeighbors by element: ")
        print("---------------------")
        for i, element in enumerate(self.elements):
            print(element.name+":")
            for n, neighbor in enumerate(element.neighbors): 
                if neighbor is None: name = "Boundary"
                else: name = neighbor.name
                print("   Port "+str(n)+":", name)



### ------------------------- ###
### Lumped Element Base Class ###
### ------------------------- ###
                        
class Element:    
    
    ### Base constructor
    def __init__(self, name, num_ports):
        self.name = name
        self.neighbors = [None]*num_ports
        self.ports = [None]*num_ports
          
    ### Connect two elements
    def tie_in(self, new_element, self_index, new_index):
        self.neighbors[self_index] = new_element
        new_element.neighbors[new_index] = self

    ### Remove component from network
    def remove(self):
        # Parsing through neighbors
        for n in range(len(self.neighbors)):
            
            # Removing self from neighbor's neighbors
            for i in range(len(self.neighbors[n].neighbors)):
                
                if self.neighbors[n].neighbors[i] == self:
                    self.neighbors[n].neighbors[i] = None
            
            # Removing neighbors
            self.neighbors[n] = None


            
### ------------------------------- ###
### Node Base Class and Sub-classes ###
### ------------------------------- ###

class Node:
    def __init__(self):
        ...
        
class Connection(Node):
    def __init__(self):
        ...

class Boundary(Node):
    def __init__(self):
        ...
        
        
    