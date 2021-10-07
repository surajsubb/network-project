# from network import *
import config 
import networkx as nx
import math
import random
import heapq

'''
Attributes:
network 

make_Lifetime_Tree()
time synchronize()
initial_setup()
broadcast_datacollection()

while adding edge follow the convention of
'''

def update_payload(node):
    if node is None:
        pass
    else:
        node.payload+=1
        update_payload(node.parent)

def calculate_score(node1,node2,weight):
    if node1.visited:
        u=node1.battery/(node1.hop*config.C_avg*math.ceil((node1.payload+2)*config.l/config.beta)+(node1.payload+1)*config.E_ELEC+node1.energy)
        v=node2.battery/weight+node2.energy+node1.hop*config.C_avg    
    else:
        u=node2.battery/(node2.hop*config.C_avg*math.ceil((node2.payload+2)*config.l/config.beta)+(node2.payload+1)*config.E_ELEC+node2.energy)
        v=node1.battery/weight+node1.energy+node2.hop*config.C_avg
    #print(u,v)
    return min(u,v)


def func(l):
        return l[-1]

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
            #self.make_Lifetime_Tree()
    
    def show_network(self):
        print(self.network)

    def make_Lifetime_Tree(self):
        Tree=nx.DiGraph()
        sink=self.network.get_sink()
        # print(sink)
        nodes=self.network.get_alive_nodes()
        if len(nodes) < config.NB_NODES:
            print("node dead cannot continue")
            return 0
        #print(nodes)
        edges=self.network.communication_link()
        #print("Edges",edges)
        ST=[]
        VT=[]
        result=[]
        inc=[]
        Inc=[]
        sink.visited=1
        ST.append((sink,sink.id,sink.hop))
        inc.append(sink)
        for edge in edges:
            if sink in edge:
                VT.append(edge)
                Inc.append((edge[0].id,edge[1].id))
        
        while not self.network.all_visited_nodes():
            i=0
            #print(ST)
            #print(Inc)
            mapping={}
            for e in VT:
                if e[0].visited and e[1].visited:
                    mapping[i]=-1
                else:
                    mapping[i]=calculate_score(e[0],e[1],e[-1]['weight'])
                #print(i)
                i+=1
            
            #for key in mapping:
            #    print(key,VT[key][0].id,VT[key][1].id,mapping[key])
            temp = max(mapping.values())
            #print(temp)
            res=None
            
            #print(mapping.keys())
            for key in mapping.keys():
                if mapping[key]==temp:
                    #print(key,len(VT))
                    print(mapping[key],VT[key][0].id,VT[key][1].id)
                    res=VT[key]
                    break
            #print(res[0].id,res[1].id,)
            if res[0].visited:
                res[0],res[1]=res[1],res[0]
            #print(res)
            result.append(res)
            res[0].visited=1
            res[1].visited=1
            res[0].parent=res[1]
            update_payload(res[1])
            res[0].hop=res[1].hop+1

            ST.append((res[0],res[0].id,res[0].hop))
            inc.append(res[0])
            VT.remove(res)
            for edge in edges:
                if edge not in VT and res[0] in edge and edge not in result :
                    if edge[0] in inc and edge[1] in inc:
                        continue
                    VT.append(edge)
                    Inc.append((edge[0].id,edge[1].id))
                    
        self.tree_nodes=[]
        ST.sort(key=func,reverse=True)
        print(ST)
        for edge in result:
            print(edge[0].id,edge[1].id)
        for node in ST:
            #Tree.add_node(node[0])
            self.tree_nodes.append(node)
        Tree.add_edges_from(result)
        ##Tree.nodes[sink.id]['color']="Red"
        for node in self.tree_nodes:
            #print(node)
            print(node[0].id,node[0].payload)
        return Tree
    
    
    def time_synchronize(self):
        sink=self.network.get_sink()
        i = 0
        for nodes in self.tree_nodes:
            if i == len(self.tree_nodes)-1:
                break
            i+=1
            nodes[0].timer=sink.timer
            # print(nodes)
    def wakeup(self):
        pass
    def sleep(self):
        i = 0
        for nodes in self.tree_nodes:
            if i == len(self.tree_nodes)-1:
                break
            i+=1
            nodes[0].sleep=1
    
    def start_convergecast(self):
        i = 0
        for nodes in self.tree_nodes:
            if i == len(self.tree_nodes)-1:
                break
            i+=1
            # print("Starting convergecast")
            nodes[0].sense()
            nodes[0].transmit(None, nodes[0].parent)

    def reactivate_nodes(self):
        i = 0
        for nodes in self.tree_nodes:
            if i == len(self.tree_nodes)-1:
                break
            i+=1
            nodes[0].reactivate()
            

    def random_spanning(self):
        Tree=nx.DiGraph()
        sink=self.network.get_sink()
        # print(sink)
        nodes=self.network.get_alive_nodes()
        if len(nodes) < config.NB_NODES:
            print("node dead cannot continue")
            return 0
        #print(nodes)
        edges=self.network.communication_link()
        ST=[]
        VT=[]
        result=[]
        inc=[]
        Inc=[]
        sink.visited=1
        ST.append((sink,sink.id,sink.hop))
        inc.append(sink)
        for edge in edges:
            if sink in edge:
                VT.append(edge)
                Inc.append((edge[0].id,edge[1]))

        while not self.network.all_visited_nodes():
            random_no=random.randint(0,len(VT)-1)
            print(random_no,len(VT))
            res=VT[random_no]
            if res[0].visited and res[1].visited:
                continue
            if res[0].visited:
                res[0],res[1]=res[1],res[0]
            result.append(res)
            res[0].visited=1
            res[1].visited=1
            res[0].parent=res[1]
            update_payload(res[1])
            res[0].hop=res[1].hop+1
            ST.append((res[0],res[0].id,res[0].hop))
            inc.append(res[0])
            VT.remove(res)
            for edge in edges:
                if edge not in VT and res[0] in edge and edge not in result :
                    if edge[0] in inc and edge[1] in inc:
                        continue
                    VT.append(edge)
                    Inc.append((edge[0].id,edge[1].id))
            
        #return ST
        self.tree_nodes=[]
        #print("hie")
        #print(result)
        #print(ST)
        ST.sort(key=func,reverse=True)
        print(ST)
        for edge in result:
            print(edge[0].id,edge[1].id)
        for node in ST:
            self.tree_nodes.append(node)
        Tree.add_edges_from(result)
        for node in self.tree_nodes:
            print(node[0].id,node[0].payload)
        return Tree

    
    def dijkstra(self):
        Tree=nx.DiGraph()
        sink=self.network.get_sink()
        # print(sink)
        nodes=self.network.get_alive_nodes()
        if len(nodes) < config.NB_NODES:
            print("node dead cannot continue")
            return 0
        #print(nodes)
        edges=self.network.communication_link()
        G=nx.Graph()
        G.add_edges_from(edges)
        print(G)
        no_nodes=len(nodes)
        dist=[1000000 for i in range(no_nodes)]
        dist[sink.id]=0
        print(G.adj[sink])
        for v in G.adj[sink]:
            print(v,G.adj[sink][v])
        PQ = []
        heapq.heappush(PQ, [dist[sink.id], sink])
        result=[]
        ST=[]
        ST.append((sink,sink.id,sink.hop))
        while PQ:
            u = heapq.heappop(PQ)  # u is a tuple [u_dist, u_id]
            u_dist = u[0]
            u_id = u[1]
            #if u_id == target:
            #    break
            for v in G.adj[u_id]:
               v_id = v
               w_uv = G.adj[u_id][v]['weight']
               if dist[u_id.id] +  w_uv < dist[v_id.id]:
                    dist[v_id.id] = dist[u_id.id] + w_uv
                    heapq.heappush(PQ, [dist[v_id.id], v_id])
                    #pred[v_id] = u_id
                    #result.append([v_id,u_id,{'weight':w_uv}])
                    v_id.parent=u_id
                    #update_payload(u_id)
                    #v_id.hop=u_id.hop+1
                    
        self.tree_nodes=[]
        #print("hie")
        #print(result)
        for node in nodes:
            if node.parent is None:
                continue
            Tree.add_edge(node,node.parent)
            node.hop=node.parent.hop+1
            update_payload(node.parent)
        for node in nodes:
            if node.parent is None:
                continue
            ST.append((node,node.id,node.hop))
        #print(ST)
        ST.sort(key=func,reverse=True)
        #print(ST)
        #for edge in result:
            #print(edge[0].id,edge[1].id)
        for node in ST:
            self.tree_nodes.append(node)
        #Tree.add_edges_from(result)
        #for node in self.tree_nodes:
        #    print(node[0].id,node[0].payload)
        pos={}
        for node in Tree.nodes():
            print(node)
            pos[node]=(node.pos_x,node.pos_y)
            print(pos[node])

        return Tree,pos
        
                   

        
            
        

            
        








        
        

