import config as cf
from node import Node
import numpy as np 
import simpy
from utils import *
from rout import Routing
import matplotlib.pyplot as plt

#function to get number of decendants list of self.payload in node

class Network():
  def __init__(self, env):
    self.end = 0
    self.env = env
    self.is_any_dead=0
    self.round_number = 0
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
    # yield self.env.timeout(duration)
    # print(self.energy_before)
    # visualize_graph(self)
    print("hello world")
    for node in self.my_nodes:
      node.reactivate()
    r=Routing(self)
    r.wakeup()
    t=r.make_Lifetime_Tree()
    if t == 0:
      # simpy.Interrupt()
      self.end = 1
      return
    r.time_synchronize()
    # print("hello world")

    visualize_Tree(t,self.round_number)
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
 
    # self.my_nodes = []
    i=0
    self.my_nodes.append(Node(i,None,True,0,0))
    for x in range(5):
      for y in range(4):
          if(i == 0):
            i+=1
            continue
          px = x*10
          py = y*10
          self.my_nodes.append(Node(i,None,None,px,py))
          i+=1
  
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
  # t=r.make_Lifetime_Tree()
  #print("hello")
  #print(t)
  # visualize_Tree(t)
  # for i in range(10):
  #   r.start_convergecast()
  #   print(my_network.get_energy_network())
  #   print(my_network.energy_before)


main()
