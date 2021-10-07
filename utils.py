import numpy as np 
import os
import glob
import math
import networkx as nx
from matplotlib import pyplot as plt


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


def visualize_Tree(tree, round_number,pos,sink,type):
    #delete preexisting files in respective folders
    if(type == 'r' and round_number == 1):
        files = glob.glob('random_plots/*')
        for f in files:
            os.remove(f)
    elif(type == 'd' and round_number == 1):
        files = glob.glob('dijikstra_plots/*')
        for f in files:
            os.remove(f)
    elif(type == 'm' and round_number == 1):
        files = glob.glob('maximum_plots/*')
        for f in files:
            os.remove(f)
    node_list=[]
    for node in tree.nodes():
        if node is sink:
            continue
        node_list.append(node)
    nx.draw_networkx_nodes(tree,pos,nodelist=[sink],node_color="Red")
    nx.draw_networkx_nodes(tree,pos,nodelist=node_list,node_color="Blue")
    nx.draw_networkx_edges(tree,pos=pos)
    plt.show()
    if(type == 'r'):
        plt.savefig("random_plots/plot%d.png" % round_number)
    elif(type == 'd'):
        plt.savefig("dijikstra_plots/plot%d.png" % round_number)
    else:
        plt.savefig("maximum_plots/plot%d.png" % round_number)
    plt.close()

def visualize_graph(network):
    g=nx.Graph()
    Tree=nx.Graph()
    sink=network.get_sink()
    nodes=network.get_alive_nodes()
    edges=network.communication_link()
    g.add_edges_from(edges)
    nx.draw(g)
    plt.show()
    plt.savefig("graph.png")

    



