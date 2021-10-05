# from network import *
import config 
import networkx as nx
import math


'''
Attributes:
network 

make_Lifetime_Tree()
time synchronize()
initial_setup()
broadcast_datacollection()

while adding edge follow the convention of
'''

def calculate_score(node1,node2,weight):
    if node1.visited:
        u=node1.battery/(node1.hop*config.C_AVG*math.ceil((node1.payload+2)*config.l/config.beta)+(node1.payload+1)*config.E_ELEC+node1.energy)
        v=node2.battery/weight+node2.energy+node1.hop*config.C_AVG    
    else:
        u=node2.battery/(node2.hop*config.C_AVG*math.ceil((node2.payload+2)*config.l/config.beta)+(node2.payload+1)*config.E_ELEC+node2.energy)
        v=node1.battery/weight+node1.energy+node2.hop*config.C_AVG
    return min(u,v)




class Routing:

    def __init__(self,network):
        self.network=network
        self.initial_setup()

    def initial_setup(self):
        if self.network.is_any_dead==1:
            print("No Routing can be done, Lifetime is over")
            #exit
        else:
            print("Initial Setting up Routing")
            self.make_Lifetime_Tree()
    
    def show_network(self):
        print(self.network)

    def make_Lifetime_Tree(self):
        Tree=nx.Graph()
        sink=self.network.get_sink()
        nodes=self.network.get_alive_nodes()
        edges=self.network.communication_link()
        ST=[]
        VT=[]
        result=[]
        sink.visited=1
        ST.append((sink.id,sink.hop))
        for edge in edges:
            if sink in edge:
                VT.append(edge)
        mapping={}
        while not self.network.all_visited_nodes():
            for e in VT:
                mapping[e]=calculate_score(e[0],e[1],e[-1]['weight'])
            temp = min(mapping.values())
            res = [key for key in mapping if mapping[key] == temp]
            result.append((res))
            res[0].visited=1
            res[1].visited=1
            res[0].parent=res[1]
            res[1].payload+=1
            res[0].hop=res[1].hop+1
            ST.append((res[1].id,res[1].hop))
            ET.remove(res)
            for edge in edges:
                if edge not in VT and res[0] in edge and edge not in result:
                    ET.append(edge)
        self.tree_nodes=[]
        for node in ST:
            Tree.add_node(node[0])
            tree_nodes.append(node[0])
        Tree.add_edges_from(result)
        Tree.nodes[sink.id]['color']="Red"
        print(Tree.edges())

        return Tree
    
    def time_synchronize(self):
        sink=self.network.get_sink()
        for nodes in self.tree_nodes:
            nodes.timer=sink.timer
    def wakeup(self):
        pass
    def sleep(self):
        for nodes in self.tree_nodes:
            nodes.sleep=1
    
    def start_convergecast(self):
        for nodes in self.tree_nodes:
            nodes.sense()
            nodes.transmit(nodes.parent)
            
            
        

            
        








        
        

