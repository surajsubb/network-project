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

    def plot_descendants(self,type,round_number,desc,X):
        if(type == 'r' and round_number == 1):
            files = glob.glob('./random_plots_desc/*')
            for f in files:
                os.remove(f)
        elif(type == 'd' and round_number == 1):
            files = glob.glob('./dijikstra_plots_desc/*')
            for f in files:
                os.remove(f)
        elif(type == 'm' and round_number == 1):
            files = glob.glob('./maximum_plots_desc/*')
            for f in files:
                os.remove(f)
        X=X
        Y=desc
        plt.bar(X,Y,width=1)
        #plt.xticks(np.arange(min(X),max(X),step=1))
        plt.title("payload for each node")
        plt.xlabel("Node")
        plt.ylabel("payload")
        plt.tight_layout()
        #plt.show()
        if(type == 'r'):
            if not os.path.exists("./random_plots_desc"):
                os.mkdir("./random_plots_desc")
            plt.savefig("./random_plots_desc/plot%d.png" % round_number)
        elif(type == 'd'):
            if not os.path.exists("./dijikstra_plots_desc"):
                os.mkdir("./dijikstra_plots_desc")
            plt.savefig("./dijikstra_plots_desc/plot%d.png" % round_number)
        else:
            if not os.path.exists("./maximum_plots_desc"):
                os.mkdir("./maximum_plots_desc")
            plt.savefig("./maximum_plots_desc/plot%d.png" % round_number)
        plt.close()

    def plot_average_descendants(self,Filepath):
        color=['r','g','b']
        legends=["Balanced_Tree","Random_Spanning_Tree","Dijkstra Spanning Tree"]
        filepath=os.listdir(Filepath)
        print(filepath)
        i=0
        for file in filepath:
            Mat=np.load(os.path.join(Filepath,file))
            Y=Mat[:,0]
            X=Mat[:,1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            i+=1
        plt.legend(legends)
        plt.xlabel("Rounds")
        plt.ylabel("Average Payload")
        plt.yticks(np.arange(0,11,1))
        plt.title("Average payload per node in each round ")
        plt.show()

    def plot_fairness(self,Filepath):
        #X=np.linspace(0,self.network.rounds,num=self.network.rounds)
        color=['r','g','b']
        legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(Filepath)
        i=0
        for file in filepath:
            Mat=np.load(os.path.join(Filepath,file))
            Y=Mat[:,0]
            X=Mat[:,1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            i+=1
        plt.title("Jain's Fairness Index comparison ")
        plt.legend(legends)
        plt.xlabel("Rounds")
        plt.ylabel("Jain's Fairness")
        #plt.yticks(np.linspace(start=min(Y),stop=max(Y),num=50))
        #plt.xticks(np.linspace(start=1,end=0.3,num=50))
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
        
        
        
    def plot_energy_consumed(self,Filepath):
        color=['r','g','b']
        legends=["Balanced_Tree","Random_Spanning_Tree","Dijkstra Spanning Tree"]
        #legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        filepath=os.listdir(Filepath)
        i=0
        for file in filepath:
            Mat=np.load(os.path.join(Filepath,file))
            Y=Mat[:,0]
            X=Mat[:,1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            i+=1
        plt.legend(legends)
        plt.xlabel("Rounds")
        plt.ylabel("Total Energy ")
        
        plt.title("Total Energy consumed in each round ")
        plt.show()
        
    

    def plot_energy_remaining(self,Filepath):
        color=['r','g','b']
        #legends=["Balanced_Tree","Dijkstra Spanning Tree","Random_Spanning_Tree"]
        legends=["Balanced_Tree","Random_Spanning_Tree","Dijkstra Spanning Tree"]
        filepath=os.listdir(Filepath)
        i=0
        for file in filepath:
            Mat=np.load(os.path.join(Filepath,file))
            Y=Mat[:,0]
            X=Mat[:,1]
            plt.plot(X,Y,color=color[filepath.index(file)])
            i+=1
        
        plt.title("Energy Left in each round by each node")
        plt.legend(legends)
        plt.xlabel("Rounds")
        plt.ylabel("Energy Left")
        plt.show()

    


