import numpy as np 
import config
#from utils import *

class Node(object):
    def __init__(self,id,parent=None,sink=None,pos_x=None,pos_y=None):
        self.id=id
        if pos_x is None and pos_y is None:
          self.pos_x=np.random.uniform(0,config.AREA_WIDTH)
          self.pos_y=np.random.uniform(0,config.AREA_HEIGHT)
        else:
          self.pos_x=pos_x
          self.pos_y=pos_y
        if sink is None:
          self.battery=config.INITIAL_BATTERY
        else: 
          self.battery=1000000
        self.parent=parent
        self.sink=sink
        self.energy=config.sense_energy
        self.alive=1
        self.reactivate()
        
    def reactivate(self):
        self.recieved_bit=0
        self.sleep=0
        self.transmit_bit=0
        self.sensed=0
        self.neighbors=[]
        self.radius=0
        self.death=10000000
        self.payload=0
        self.hop=0
        self.visited=0
        self.timer=0
        self.amount_sensed=0
        self.amount_received=0
        self.amount_transmitted=0

    def helloWorld(self):
      print("Hello World")
    
    
    def recharge(self):
      if self.sink is None:
        self.battery=config.INITIAL_BATTERY
      else: 
        self.battery=1000000
    
    def consume(self,energy):
      if self.battery>=energy:
        self.battery-=energy
      else:
        print("Network Failure Battery Depleted %d"%self.id)
        self.battery_depletion()
    
    

    @property
    def nexthop(self):
        return self.hop 
    
    @nexthop.setter
    def nexthop(self,value):
        self.hop=value


    @property
    def is_sleeping(self):
        if self.is_head():
            self.sleep=0
        return self.sleep
    
    @is_sleeping.setter
    def is_sleeping(self, value):
      self.sleep = value if not self.is_head() else 0

    def is_head(self):
      if self.sink is not None:
        return 1
      return 0
    


        
    def _only_active_nodes(func):
      """This is a decorator. It wraps all energy consuming methods to
    ensure that only active nodes execute this method. Also it automa-
    tically calls the battery. 
      """
      def wrapper(self, *args, **kwargs):
        if self.alive and not self.sleep:
          func(self, *args, **kwargs)
          return 1
        else:
          return 0
      return wrapper


    @_only_active_nodes
    def _aggregate(self, msg_length):
      print("node %d aggregating." % (self.id))
      # number of bits to be sent increase while forwarding messages
      aggregation_cost = self.aggregation_function(msg_length)
      self.tx_queue_size += aggregation_cost

      # energy model for aggregation
      energy = config.E_DA * aggregation_cost
      self.energy_source.consume(energy)

    @_only_active_nodes
    def transmit(self, msg_length=None, destination=None):
      print("node %d transmitting." % (self.id))
      if not msg_length:
        msg_length = self.tx_queue_size
      #msg_length += config.HEADER_LENGTH

      if not destination:
        destination = self.parent
      distance = calculate_distance(self, destination)

      # transmitter energy model
      energy = config.E_ELEC*msg_length
      if distance > config.THRESHOLD_DIST:
        energy += config.E_MP * (distance**4)
      else:
        energy += config.E_FS * (distance**2)
      # energy *= msg_length

      # automatically call other endpoint receive
      destination.receive(msg_length)
      # after the message is sent, queue is emptied 
      self.tx_queue_size = 0
      self.amount_transmitted += msg_length

      self.consume(energy)

    @_only_active_nodes
    def receive(self, msg_length):
      print("node %d receiving." % (self.id))
      #self._aggregate(msg_length - config.HEADER_LENGTH
      self.amount_received += msg_length

      # energy model for receiver
      energy = config.E_ELEC * msg_length
      self.consume(energy)

    @_only_active_nodes
    def sense(self):
      self.tx_queue_size = config.MSG_LENGTH
      self.amount_sensed += config.MSG_LENGTH
      self.consume(self.energy)

    def battery_depletion(self):
      self.alive = 0
      self.sleep_prob = 0.0

    def set_load(self,value):
      self.payload=value


