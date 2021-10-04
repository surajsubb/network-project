import config as cf
from node import Node
import numpy as np 

class Network():
  def __init__(self):
    self.is_any_dead=0
    self.makeGraph()
  
  #making graph
  def makeGraph(self):
    #creating nodes in a grid shape
    # 0 4 8  12 16
    # 1 5 9  13 17
    # 2 6 10 14 18
    # 3 7 11 15 19
 
    self.my_nodes = []
    i=0
    self.my_nodes.extend([Node(i,None,True,0,0)])
    for x in range(5):
      for y in range(4):
          if(i == 0):
            i+=1
            continue
          px = x*10
          py = y*10
          self.my_nodes.extend([Node(i,None,None,px,py)])
          i+=1
  
  #getting the sink node
  def get_sink(self):
    for node in self.my_nodes:
      if node.sink is not None:
        return [node]
  
  #getting the nodes that are alive
  def get_alive_nodes(self):
    alive_nodes = []
    for node in self.my_nodes:
      if node.alive:
        alive_nodes.extend(node)
    return alive_nodes
  
  #know is all the nodes have been visited or not
  def all_visited_nodes(self):
    for node in self.my_nodes:
      if node.visited == 0:
        return False
    return True

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
        self.my_nodes[3],
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

    return my_edges
      
