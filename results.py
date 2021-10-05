import config
from matplotlib import pyplot as plt
import numpy as np
from utils import *



class Result:
    def __init__(self,network,trace):
        self.network=network
        self.trace=trace
    
    
    def plot_nodes(self):
        X=[node.pos_x for node in self.network.my_nodes]
        Y=[node.pos_y for node in self.network.my_nodes]
        fig,ax=plt.subplot()
        ax.xlim(xmin=0)
        ax.ylim(ymin=0)
        ax.xlim(xmax=config.AREA_WIDTH)
        ax.ylim(ymax=config.AREA_HEIGHT)
        ax.scatter(X,Y)
        ax.title("Node Position")
        ax.grid(True)
        plt.show()

    def plot_descendants(self):
        X=np.linspace(0,config.NB_NODES,num-config.NB_NODES)
        Y=[node.payload for node in self.network.my_nodes]
        plt.bar(X,Y)
        plt.show()

    def plot_fairness(self,Jain):
        X=np.linspace(0,self.network.rounds,num=self.network.rounds)
        Y=Jain
        plt.plot(X,Y,color='b')
        plt.show()

    
    

   
         





