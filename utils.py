import numpy as np 
import os
import glob
import math
import networkx as nx
from matplotlib import pyplot as plt
import config as cf


def calculate_distance(node1,node2):
    dist=((node1.pos_x-node2.pos_x)**2)+((node1.pos_y-node2.pos_y)**2)
    return math.sqrt(dist)



def print_node_position(network):
    for node in network.my_nodes:
        print("Node %d is at (%d,%d)"%(node.id,node.pos_x,node.pos_y))


def Jain_fairness(network):
    resource = []
    for node in network.my_nodes:
        if(node.id == cf.SINK_ID):
            continue
        resource.append(node.battery)
    #n=config.NB_NODES
    J=(np.sum(resource)**2)/((len(resource)*(np.sum(np.multiply(resource,resource)))))
    print(resource)
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
    labeldict={}
    for node in tree.nodes():
        if node is sink:
            labeldict[node]="S"
            continue
        labeldict[node]=node.id
        node_list.append(node)
    nx.draw_networkx_nodes(tree,pos,nodelist=[sink],node_color="Red",label=labeldict)
    nx.draw_networkx_nodes(tree,pos,nodelist=node_list,node_color="Blue",label=labeldict)
    nx.draw_networkx_labels(tree,pos=pos,labels=labeldict)
    nx.draw_networkx_edges(tree,pos=pos)
    #plt.show()
    if(type == 'r'):
        plt.savefig("random_plots/plot%d.png" % round_number)
    elif(type == 'd'):
        plt.savefig("dijikstra_plots/plot%d.png" % round_number)
    else:
        plt.savefig("maximum_plots/plot%d.png" % round_number)
    plt.close()

def visualize_graph(tree, round_number,pos,sink):
    node_list=[]
    labeldict={}
    for node in tree.nodes():
        if node is sink:
            labeldict[node]="S"
            continue
        labeldict[node]=node.id
        node_list.append(node)
    
    nx.draw_networkx_nodes(tree,pos,nodelist=[sink],node_color="Red",label=labeldict)
    nx.draw_networkx_nodes(tree,pos,nodelist=node_list,node_color="Blue",label=labeldict)
    nx.draw_networkx_labels(tree,pos=pos,labels=labeldict)
    nx.draw_networkx_edges(tree,pos=pos)
    #plt.show()
    #plt.show()
    plt.savefig("graph.png")


def generate_graph(nodes,position):
    graph=nx.generators.geometric.random_geometric_graph(nodes,30,pos=position)
    print(graph)
    edges=[edge for edge in graph.edges()]
    return graph,edges

def save_file(value_X,value_Y,file_path):
    Mat=np.zeros(shape=(len(value_X),2))
    for i in range(len(value_X)):
        Mat[i][0]=value_X[i]
        Mat[i][1]=value_Y[i]
    np.save(file_path,Mat)
