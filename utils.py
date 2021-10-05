import numpy as np 
import os
import math



def calculate_distance(node1,node2):
    dist=(node1.pos_x-node2.pos_x)**2+(node1.pos_y-node1.pos_y)**2
    return math.sqrt(dist)



def print_node_position(network):
    for node in network.my_nodes:
        print("Node %d is at (%d,%d)"%(node.id,node.pos_x,node.pos_y))



 def Jain_fairness(network):
    resource=[node.battery for node in network.my_nodes]
    #n=config.NB_NODES
    J=np.sum(resource)**2/n*(np.sum(resource*resource))
    return J

