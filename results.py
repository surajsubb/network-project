import config
from matplotlib import pyplot as plt
import numpy as np
from utils import *
from rout import Routing

class Result:
    def __init__(self,network,trace):
        self.network=network
        self.trace=trace
        self.routing=Routing(self.network)
    
    
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

    def plot_descendants(self,type,round_number):
        if(type == 'r' and round_number == 1):
            files = glob.glob('random_plots_desc/*')
            for f in files:
                os.remove(f)
        elif(type == 'd' and round_number == 1):
            files = glob.glob('dijikstra_plots_desc/*')
            for f in files:
                os.remove(f)
        elif(type == 'm' and round_number == 1):
            files = glob.glob('maximum_plots_desc/*')
            for f in files:
                os.remove(f)
        X=np.linspace(1,config.NB_NODES,num=config.NB_NODES-1)
        Y=self.routing.number_of_descendents()
        plt.bar(X,Y,width=1)
        plt.tight_layout()
        plt.show()
        if(type == 'r'):
            plt.savefig("random_plots_desc/plot%d.png" % round_number)
        elif(type == 'd'):
            plt.savefig("dijikstra_plots_desc/plot%d.png" % round_number)
        else:
            plt.savefig("maximum_plots_desc/plot%d.png" % round_number)
        plt.close()

    def plot_average_descendants(self):
        color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(filepath)
        i=0
        for file in filepath:
            Mat=np.load(file)
            X=Mat[:][0]
            Y=Mat[:][1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            plt.legend(legends[i])
            i+=1
        plt.title("Average payload per node in each round ")
        plt.show()

    def plot_fairness(self,filepath):
        #X=np.linspace(0,self.network.rounds,num=self.network.rounds)
        color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(filepath)
        i=0
        for file in filepath:
            Mat=np.load(file)
            X=Mat[:][0]
            Y=Mat[:][1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            plt.legend(legends[i])
            i+=1
        plt.title("Jain's Fairness Index comparison ")
        plt.show()

    def plot_lifetime(self,filepath):
        color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(filepath)
        i=0
        for file in filepath:
            Mat=np.load(file)
            X=Mat[:][0]
            Y=Mat[:][1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            plt.legend(legends[i])
            i+=1
        plt.title("Lifetime of the Convergecast tree vs Number of Nodes")
        plt.show()
        
        
        
    def plot_energy_consumed(self,filepath):
        color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(filepath)
        i=0
        for file in filepath:
            Mat=np.load(file)
            X=Mat[:][0]
            Y=Mat[:][1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            plt.legend(legends[i])
            i+=1
        plt.title("Total Energy consumed in each round ")
        plt.show()
        
    
    def plot_average_consumed(self,filepath):
        color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(filepath)
        i=0
        for file in filepath:
            Mat=np.load(file)
            X=Mat[:][0]
            Y=Mat[:][1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            plt.legend(legends[i])
            i+=1
        plt.title("Average Energy consumed in each round by each node")
        plt.show()
    

    def plot_energy_remaining(self,filepath)
    color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(filepath)
        i=0
        for file in filepath:
            Mat=np.load(file)
            X=Mat[:][0]
            Y=Mat[:][1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            plt.legend(legends[i])
            i+=1
        plt.title("Energy Left in each round by each node")
        plt.show()

    


