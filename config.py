import math

AREA_WIDTH=100
AREA_HEIGHT=100


INITIAL_BATTERY=10

sense_energy=3.2e-9

MSG_LENGTH=8
l=8
beta=8

MAX_ROUNDS = 15000
# number of transmissions of sensed information to cluster heads or to
# base station (per round)
MAX_TX_PER_ROUND = 1

NOTIFY_POSITION = 0


SLEEP_TIME=15
WAKE_UP=5

C_avg=13.67

TIME_SYN=3


## Network configurations:
# number of nodes
NB_NODES = 20
# node sensor range
COVERAGE_RADIUS = 15 # meters 
# node transmission range
TX_RANGE = 30 # meters
# base station position
BS_POS_X = 0
BS_POS_Y = 0

E_ELEC = 50e-5 # Joules
# energy dissipated at the data aggregation (/bit)
E_DA = 5e-5 # Joules
# energy dissipated at the power amplifier (supposing a multi-path
# fading channel) (/bin/m^4)
E_MP = 0.0013e-12 # Joules
# energy dissipated at the power amplifier (supposing a line-of-sight
# free-space channel (/bin/m^2)
E_FS = 10e-12 # Joules
THRESHOLD_DIST = math.sqrt(E_FS/E_MP)

RESULT='./result/'
