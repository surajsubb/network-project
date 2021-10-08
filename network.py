import config as cf
from node import Node
import numpy as np 
import simpy
from utils import *
from rout import Routing
import matplotlib.pyplot as plt
import json
from collections import defaultdict

#function to get number of decendants list of self.payload in node

class Network():
  def __init__(self, env):
    self.end = 0
    self.env = env
    self.is_any_dead=0
    self.round_number = 0
    self.my_nodes=[]
    self.makeGraph()
    self.initial_energy_in_network()
    self.action = self.env.process(self.Simulate())
    # self.Simulate()


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

    # t,p,final_edges=r.make_Lifetime_Tree(self.round_number) #CHANGE HERE
    t,p,final_edges=r.random_spanning() #CHANGE HERE
    # t,p,final_edges=r.dijkstra() #CHANGE HERE

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

    self.createFile('r',data) #CHANGE HERE

    if p == 0:
      self.end = 1
      return
    r.time_synchronize()

    '''change the below function according to which Tree function is being run, for maximum lifetime, make last parameter 'm'. 
        for random spanning make last parameter 'r' and for dikistra make last parameter 'd'. 
    '''

    visualize_Tree(t,self.round_number,p,sink,'r') #CHANGE HERE
    for i in range(25):
      r.start_convergecast()
      alive_nodes = self.get_alive_nodes()
      if(len(alive_nodes) < cf.NB_NODES):
        self.end = 1
        break
      # print(self.get_energy_network())
      # print(self.get_energy_consumed_by_network())
      # print(self.energy_before)
      print(r.number_of_descendents())
    print(Jain_fairness(self))
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
      self.energy_before.append(node.battery)
      self.total_energy_before+=node.battery
    self.average_energy_before = self.total_energy_before/cf.NB_NODES

  def makeGraph(self):
    #creating nodes in a grid shape
    # 0 4 8  12 16
    # 1 5 9  13 17
    # 2 6 10 14 18
    # 3 7 11 15 19
 
    self.my_nodes = []
    i=0
    for x in range(5):
      for y in range(4):
          px = x*10
          py = y*10
          if(i == cf.SINK_ID):
            self.my_nodes.append(Node(i,None,True,px,py))
            i+=1
            continue
          self.my_nodes.append(Node(i,None,None,px,py))
          i+=1
    self.position={}
    for node in self.my_nodes:
      position[node]=(node.px,node.py)
  
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
    my_edges = []
    my_edges.extend([
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

    # my_edges = []
    # my_edges.extend([
    #   [
    #     self.my_nodes[0],
    #     self.my_nodes[1],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[0],
    #     self.my_nodes[2],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[0],
    #     self.my_nodes[3],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[0],
    #     self.my_nodes[4],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[1],
    #     self.my_nodes[2],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[1],
    #     self.my_nodes[3],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[1],
    #     self.my_nodes[4],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[2],
    #     self.my_nodes[3],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[2],
    #     self.my_nodes[4],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    #   [
    #     self.my_nodes[3],
    #     self.my_nodes[4],
    #     {'weight': np.random.uniform(1,5)}
    #   ],
    # ])

    return my_edges

#env = simpy.Environment() 
def main():
  # env=None
  env = simpy.Environment() 
  my_network = Network(env)
  env.run()
  # print(my_network.energy_before)
  # visualize_graph(my_network)
  # r=Routing(my_network)
  # t,p=r.dijkstra()
  #print("hello")
  #print(t)
  #
  # s=my_network.get_sink()
  # visualize_Tree(t,0,p,s,'d')
  # for i in range(10):
  #   r.start_convergecast()
  #   print(my_network.get_energy_network())
  #   print(my_network.energy_before)


main()
