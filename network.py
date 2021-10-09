import config as cf
from node import Node
import numpy as np 
import simpy
from utils import *
from rout import Routing
import matplotlib.pyplot as plt
import json
from collections import defaultdict
import os
import pickle
from results import Result
import glob
#function to get number of decendants list of self.payload in node

class Network():
  def __init__(self, env,mode,File=None):
    self.end = 0
    self.env = env
    self.is_any_dead=0
    self.round_number = 0
    self.file=File
    #print(self.file)
    self.my_nodes=[]
    self.makeGraph()
    self.initial_energy_in_network()
    self.action = self.env.process(self.Simulate())
    self.Jain=[]
    self.energy_left=[]
    self.average_desc=[]
    self.average_energy=[]
    self.total_energy_cons=[]
    self.lifetime=[]
    # self.Simulate()
    self.desc=Result(self,None)
    self.mode=mode


  def Simulate(self):
    
    while self.end == 0:
      print("wake up at %d" % self.env.now)
      self.round_number+=1
      print("starting round number %d" % self.round_number)

      self.env.process(self.run_round())

      print("going to sleep at %d" % self.env.now)
      yield self.env.timeout(18)
    print("Dead node found in round: %d" % self.round_number)
    print("SIMULATION OVER")
  
  def run_round(self):

    sink=self.get_sink()
    for node in self.my_nodes:
      node.reactivate()
    r=Routing(self)
    r.wakeup()

    '''the below 3 functions are used to get different types of trees, run them one at a time and change visualize tree accordingly.'''
    if self.mode=='m':
      t,p,final_edges=r.make_Lifetime_Tree(self.round_number) #CHANGE HERE
    elif self.mode=='r':
      t,p,final_edges=r.random_spanning() #CHANGE HERE
    else:
      t,p,final_edges=r.dijkstra() #CHANGE HERE

    #to make JSON file
    data = defaultdict(list)
    nodes = []
    isSink = False
    fillStyle = "#22cccc"
    strokeStyle = "#009999"
    for node in self.my_nodes:
      if(node.id == cf.SINK_ID):
        isSink = True
        fillStyle = "ff0000"
        strokeStyle = "ff0000"
      jsonNode = {
        "id": node.id, 
        "x": node.pos_x*5+10, 
        "y": node.pos_y*5+10,
        "radius": 10,
        "isSink": isSink,
        "fillStyle": fillStyle,
        "strokeStyle": strokeStyle 
      }
      isSink = False
      fillStyle = "#22cccc"
      strokeStyle = "#009999"
      nodes.append(jsonNode)
    data['nodes'] = nodes
    data['edges'] = final_edges

    self.createFile(self.mode,data) #CHANGE HERE
    self.initial_energy_in_network()
    self.energy_left.append(self.total_energy_before)
    if p == 0:
      self.end = 1
      return
    r.time_synchronize()

    '''change the below function according to which Tree function is being run, for maximum lifetime, make last parameter 'm'. 
        for random spanning make last parameter 'r' and for dikistra make last parameter 'd'. 
    '''

    visualize_Tree(t,self.round_number,p,sink,self.mode) #CHANGE HERE
    for i in range(cf.MAX_TX_PER_ROUND):
      r.start_convergecast()
      alive_nodes = self.get_alive_nodes()
      if(len(alive_nodes) < cf.NB_NODES):
        self.end = 1
        self.lifetime=[self.round_number,cf.NB_NODES]
        break
    print(Jain_fairness(self))
    self.Jain.append(Jain_fairness(self))
    desc,avg,X=r.number_of_descendents()
    self.desc.plot_descendants(self.mode,self.round_number,desc,X)
    self.average_desc.append(avg)
    self.total_energy_cons.append(self.get_energy_consumed_by_network())
    self.average_energy.append(self.get_energy_consumed_by_network()/cf.NB_NODES)
    r.sleep()
    yield self.env.timeout(2)
    print("----------------------------------------------------------------------------------------------------------------------------")
    
  #making graph
  def initial_energy_in_network(self):
    self.energy_before = []
    self.energy_consumed_per_round = []

    self.total_energy_before = 0
    self.average_energy_before = 0

    for node in self.my_nodes:
      if node.id==0:
        continue
      self.energy_before.append(node.battery)
      self.total_energy_before+=node.battery
    self.average_energy_before = self.total_energy_before/cf.NB_NODES

  def makeGraph(self):
    self.my_nodes = []
    i=0
    
    for x in range(cf.NB_NODES):
      #for y in range(4):
      px = np.random.randint(0,100)#
      py = np.random.randint(0,100)#
      if(i == cf.SINK_ID):
        self.my_nodes.append(Node(i,None,True,0,0))
        i+=1
        continue
      self.my_nodes.append(Node(i,None,None,px,py))
      i+=1
    #graph,self.my_edges1=generate_graph(self.my_nodes,self.position)
    with open(self.file,"rb") as f:
      G=pickle.load(f)
    self.my_nodes,self.my_edges1=G[0],G[1]
    self.position={}
    for node in self.my_nodes:
      self.position[node]=(node.pos_x,node.pos_y)
    sink=self.get_sink()
    visualize_graph(self.my_nodes,self.my_edges1,0,self.position,sink)

  
  #getting the sink node
  def get_sink(self):
    for node in self.my_nodes:
      if node.sink is not None:
        return node
  
  #getting the nodes that are alive
  def get_alive_nodes(self):
    alive_nodes = []
    for node in self.my_nodes:
      if node.alive:
        alive_nodes.append(node)
    return alive_nodes
  
  #know is all the nodes have been visited or not
  def all_visited_nodes(self):
    for node in self.my_nodes:
      if node.visited == 0:
        return False
    return True

  #calculate total energy consumed by network and average energy consumed
  def get_energy_consumed_by_network(self):
    total_energy = 0
    for node in self.my_nodes:
      if node.id is 0:
        continue

      total_energy+=node.battery
    energy_consumed = self.total_energy_before-total_energy
    self.total_energy_before = total_energy
    self.average_energy_before = energy_consumed/cf.NB_NODES
    self.energy_consumed_per_round.extend([energy_consumed])
    return energy_consumed

  #return list of energies of each node
  def get_energy_network(self):
    energy_consumed_each_node = []
    energy_in_each_node = []
    i=0
    for node in self.my_nodes:
      if node.id is 0:
        continue

      energy_in_each_node.append(node.battery)
      energy_consumed_each_node.append(self.energy_before[i]-node.battery)
      i+=1
    self.energy_before = energy_in_each_node
    return energy_consumed_each_node

  #create file for each round
  def createFile(self,type,data):
   #delete pre existing files
   if(type == 'm' and self.round_number == 1):
       files = glob.glob('Simulator/JSON/Lifetime_Tree/*')
       for f in files:
         os.remove(f)
   elif(type == 'r' and self.round_number == 1):
       files = glob.glob('Simulator/JSON/Random_Tree/*')
       for f in files:
         os.remove(f)
   elif(type == 'd' and self.round_number == 1):
       files = glob.glob('Simulator/JSON/Dijikstra_Tree/*')
       for f in files:
         os.remove(f)

   #creation of file 
   if(type == 'm'):
     filepath = os.path.join('Simulator/JSON/Lifetime_Tree/', 'tree%d.json'%self.round_number)
     f = open(filepath, "w")
     with open('Simulator/JSON/Lifetime_Tree/tree%d.json'%self.round_number, 'w') as outfile:
       json.dump(data, outfile)
   elif(type == 'r'):
     filepath = os.path.join('Simulator/JSON/Random_Tree/', 'tree%d.json'%self.round_number)
     f = open(filepath, "w")
     with open('Simulator/JSON/Random_Tree/tree%d.json'%self.round_number, 'w') as outfile:
       json.dump(data, outfile)
   elif(type == 'd'):
     filepath = os.path.join('Simulator/JSON/Dijikstra_Tree/', 'tree%d.json'%self.round_number)
     f = open(filepath, "w")
     with open('Simulator/JSON/Dijikstra_Tree/tree%d.json'%self.round_number, 'w') as outfile:
       json.dump(data, outfile)
  
  #edges between nodes
  def communication_link(self):
    if self.my_edges1 is not None:
      self.my_edges = []
      for edge in self.my_edges1:
        self.my_edges.extend([[edge[0],edge[1],{'weight':calculate_distance(edge[0],edge[1])}]])
      return self.my_edges
    self.my_edges = []
    self.my_edges.extend([
      [
        self.my_nodes[1],
        self.my_nodes[0],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[2],
        self.my_nodes[1],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[3],
        self.my_nodes[2],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[4],
        self.my_nodes[0],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[8],
        self.my_nodes[4],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[12],
        self.my_nodes[8],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[16],
        self.my_nodes[12],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[5],
        self.my_nodes[4],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[5],
        self.my_nodes[1],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[9],
        self.my_nodes[8],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[9],
        self.my_nodes[5],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[13],
        self.my_nodes[12],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[13],
        self.my_nodes[9],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[17],
        self.my_nodes[16],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[17],
        self.my_nodes[13],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[6],
        self.my_nodes[5],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[6],
        self.my_nodes[2],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[10],
        self.my_nodes[9],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[10],
        self.my_nodes[6],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[14],
        self.my_nodes[13],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[14],
        self.my_nodes[10],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[18],
        self.my_nodes[17],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[18],
        self.my_nodes[14],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[7],
        self.my_nodes[6],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[7],
        self.my_nodes[3],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[11],
        self.my_nodes[10],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[11],
        self.my_nodes[7],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[15],
        self.my_nodes[14],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[15],
        self.my_nodes[11],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[19],
        self.my_nodes[18],
        {'weight': np.random.uniform(1,5)}
      ],
      [
        self.my_nodes[19],
        self.my_nodes[15],
        {'weight': np.random.uniform(1,5)}
      ],
    ])


    return self.my_edges

  
  def finish(self,filepath):

    files=['./Jain/','./Battery_left/','./Total_energy_consumed/','./Average_energy_consumed/','./Average_descendants/']
    for file in files:
      if not os.path.exists(file):
        os.mkdir(file)
    value=self.round_number
    Y=np.arange(start=0,stop=value+1,step=1)
    to_store=[self.Jain,self.energy_left,self.total_energy_cons,self.average_energy,self.average_desc]
    Mat=np.zeros(shape=(value,2))
    i=0
    for val in to_store:
      # print(len(val),Mat.shape)
      for j in range(value):
        Mat[j][0]=val[j]
        Mat[j][1]=Y[j]
      #print(Mat)
      np.save(os.path.join(files[i],filepath+".npy"),Mat)
      i+=1

#env = simpy.Environment() 


def lifetime():
  paths=["Graph_20.pkl","Graph_40.pkl","Graph_60.pkl","Graph_80.pkl","Graph_100.pkl"]
  Djikstra=[]
  Maximum=[]
  Nodes=[]
  random=[]
  node={}
  node["Graph_20.pkl"]=20
  node["Graph_40.pkl"]=40
  node["Graph_60.pkl"]=60
  node["Graph_80.pkl"]=80
  node["Graph_100.pkl"]=100
  for path in paths:
    number=node[path]
    Nodes.append(number)
    cf.NB_NODES=number
    env = simpy.Environment() 

    my_network = Network(env,"m",path)
    env.run()
    Maximum.append(my_network.round_number)
    my_network = Network(env,"d",path)
    env.run()
    Djikstra.append(my_network.round_number)
    my_network = Network(env,"r",path)
    env.run()
    random.append(my_network.round_number)
  color=['r','g','b']
  legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
  plt.plot(Nodes,Maximum,marker='o',color=color[0])
  plt.plot(Nodes,Djikstra,color=color[1])
  plt.plot(Nodes,random,color=color[2])
  plt.xlabel("Number of Nodes")
  plt.ylabel("Number of Rounds")
  plt.title("Lifetime")
  plt.legend(legends)
  plt.savefig("lifetime.png")
  plt.show()


def main():
  env=None

  env = simpy.Environment() 
  my_network = Network(env,"m","Graph_80.pkl")
  env.run()
  my_network.finish("lifetime")

  env = simpy.Environment() 
  my_network = Network(env,"d","Graph_80.pkl")
  env.run()
  my_network.finish("djikstra")

  env = simpy.Environment() 
  my_network = Network(env,"r","Graph_80.pkl")
  env.run()
  my_network.finish("random")
  
  result=Result(my_network,None)
  result.plot_fairness('./Jain/')
  result.plot_average_descendants('./Average_descendants/')
  result.plot_energy_remaining('./Battery_left/')
  result.plot_energy_consumed("./Total_energy_consumed")
  # lifetime()


main()
