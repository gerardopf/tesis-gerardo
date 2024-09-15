""" =========================================================================
% SWARM INTELLIGENCE ALGORITHM FOCUSED ON FORMATION SYNCHRONIZATION AND 
% CONTROL IN A MULTI-AGENT ROBOTIC SYSTEM
% DYNAMIC MODEL WITH FORMATION CONTROL, USING HYPERBOLIC COSINE, AND
% COLLISION AVOIDANCE INCLUDING SPEED LIMITS.
% CENTRAL PROGRAM
% =========================================================================
% Author: Alejandro Rodríguez
% Last update: 12/1/2024
% =========================================================================
% The following script implements the dynamic model with a modification to 
% the consensus equation using the obstacle avoidance and a combination 
% of the formation control with a hyperbolic cosine function (tension 
% function) for minimally rigid graphs and collision avoidance. It also
% includes speed limits to keep the robots within its physical capacity.
%
% It is Supervisor controller.
========================================================================="""

"""Supervisor_simulacion_y_fisico_v4 controller."""

# Library imports
from controller import Robot, Supervisor
import numpy as np
import random
import math
import pickle
import keyboard
import time
from funVel import Fmatrix
import funciones
from multiprocessing import shared_memory, Lock
from funciones_conjunto import *

# shared memory spaces creation to communicate the supervisor program with each individual agent program
shm1 = shared_memory.SharedMemory(name="my_shared_memory1", create=True, size=1024)
shm2 = shared_memory.SharedMemory(name="my_shared_memory2", create=True, size=4096)

# synchronization Lock to ensure a stable communication between programs (IPC, interprocess communication)
lock = Lock()
TIME_STEP = 64 #each step of the simulation is 64 ms

supervisor = Supervisor() # Creates Supervisor instance

"""real or not"""
fisico = 1               # 0 to use Webots | 1 to use Robotat
initial_conditions_file = 'trial0.npz' # select the initial conditions file (.npz) to compare the physical run to simulation
r_initial_conditions = 0 # 0: new simulation | 1: simulation based on real physical conditions
r_obs = 1                # 0: virtual obstacles | 1: real obstacles (obtained from OptiTrack markers)
r_obj = 1                # 0: virtual objective | 1: real objective (obtained from Optitrack marker)
r_webots_visual = 1      # 0: doesnt update visuals of real obj and obs | 1: updates visuals of real obj and/or obj
MAX_SPEED = 30           # MAXIMUM SPEED OF THE WHEELS IN RPM

# Formation Matrix
form_shape = 1    # 1: triangle | 2: long hexagon
rigidity_level = 8 # integer values between 1 and 8, lower being less rigid 

""" Agents """
NMax = 10  # Maximum agent number that the formation shape can contain
NStart = 5 # First agent (lower limit of the interval of agents)
N = 8	# Last agent (higher limit of the interval of agents)

"""radar"""
r = 0.07	# radius to consider to avoid collisions (in centimeters)
R = 4	# radar range (how far can the agents detect each other) 

"""obstacles and objective"""
obs_active = 1        # 0: obs not active | 1: obs active
obj_marker = 12        # starting OptiTrack marker for objective 
obs_start_marker = 2 # starting OptiTrack marker for obstacles  
robotat_markers = [1,2,3,4,5,6,7,8,9,10,11,12] #OptiTrack markers

"""initial positions"""
setup_shape = 0         # 0: Initial marks line setup | 1: circle marks setup
setup_shape_space = 1.5 # space to cover with the setup

# Specify the starting point
setup_starting_point = np.array([-1.0, -1.5])

# Assign revised positions
agent_setup = 5 # use 5        
#agent_setup:
# for simulation
# 0: actual agent positions
# 1: random agent instant positions
# 2: random marker positions, actual agent positions
# 3: L marker positions, actual agents positions
# for both simulation and physical
# 4: is a downgraded version of 5, so avoid using this

# 5: MAIN FUNCTIONING --> custom agent positioning taking into account the initial conditions of real world

initial_pos_setup = 1 # marker initialization 0: random | 1: planified

formation_edge = 0.3 # edge length for graph (assigned distance between agents in the matrix)

#robot dimensions
#pololu
r_f = 0.017
l_f = 0.0485
a_f = 0.0485

#initial conditions from real life run
if (r_initial_conditions == 1):
    initial_data = np.load(initial_conditions_file)
    real_begin_alg_time = initial_data['begin_alg_time']
    r_obs = initial_data['r_obs']
    r_obj = initial_data['r_obj']
    form_shape = initial_data['form_shape']
    rigidity_level = initial_data['rigidity_level']
    NMax = initial_data['NMax']
    N = initial_data['N']
    NStart = initial_data['NStart']
    r = initial_data['r']
    R = initial_data['R']
    obs_active = initial_data['obs_active']
    obj_marker = initial_data['obj_marker']
    obs_start_marker = initial_data['obs_start_marker']
    robotat_markers = -1
    setup_shape = initial_data['setup_shape']
    setup_shape_space = initial_data['setup_shape_space']
    setup_starting_point = initial_data['setup_starting_point']
    agent_setup = initial_data['agent_setup']
    initial_pos_setup = initial_data['initial_pos_setup']

# epuck dimensions and max speed for simulation
if (fisico == 0):
    MAX_SPEED = 6.28 #radians/s
    r_f = 0.0205
    l_f = 0.0355
    a_f = 0.0355  

# initialization of some variables
setup_pos = np.zeros((NMax, 6))
NStart = NStart-1 
total_agent_number = N-NStart
total_agent_weight = (total_agent_number)/NMax
begin_alg_time = -1 # valor arbitrario para inicializar variable    
obs_start_marker = obs_start_marker - 1 
obj_marker = obj_marker - 1 

# defines spawn shape of epucks/starting agent positions
if (r_initial_conditions == 0):
    # line shape
    if (setup_shape == 0):
        for i in range(NStart,N):
            setup_pos[i, 0] = setup_starting_point[0] + i * 0.3 
            setup_pos[i, 1] = setup_starting_point[1] + i * 0.3 * 0
            setup_pos[i, 2] = 0.5
    # circle shape
    elif (setup_shape == 1):
        for i in range(NStart,N):
            angle = 2 * np.pi * i / (total_agent_number)  # Calculate the angle for each marker
            setup_shape_radius = setup_shape_space/2
            setup_pos[i, 0] = setup_starting_point[0] + setup_shape_radius * np.cos(angle)  # x-coordinate
            setup_pos[i, 1] = setup_starting_point[1] + setup_shape_radius * np.sin(angle)  # y-coordinate
            setup_pos[i, 2] = 0.5  # constant z-coordinate

# set to -1 if the object is not real, i.e. virtual
if(r_obj == 0):
   obj_marker = -1 
if(r_obs == 0):
   obs_start_marker = -1  
    
#variable initialization    
trajectory = []
velocityHist = []
normVHist = []
objHist = []
obsHist = []
formation_mseHist = []
rotHist = []
PosRealAgents = 0
RotRealAgents = 0 
form_cycle = -1
obj_cycle = -1
obj_success_cycle = -1
obj_success = 0
agents_pose = []
obj_cont = 0
ciclo = 0  
					
#function to acquire specific markers poses on command
def update_data(robotat, markers_to_use):
    try: 
        if robotat:
            #print(robotat)
            n_ag = len(markers_to_use)
            #print("Number of agents:\n",n_ag)
            pose = robotat_get_pose(robotat, markers_to_use)
            pose_eul = quat2eul(pose,'zyx')
        else: 
            print("no connection?")
            pose_eul = None
    except:
        print("error")
        print(pose)
        pose_eul = None
    finally:
        return pose_eul   

if (fisico == 1):
    try:
        robotat = robotat_connect()
    except:
        print("error")
    # takes into account the natural orientation of markers and uses them to calibrate the bearing
    desfases = np.load('calibracion_markers_inicial.npy') 
    desfases_euler = quat2eul(desfases,'zyx')
    agents_pose = update_data(robotat,robotat_markers)
    # calibrates the bearing for each agent marker
    for marker in range(len(agents_pose)):
            agents_pose[marker,3] = agents_pose[marker,3] - desfases_euler[marker,3]
    
""" Arena """
arena = supervisor.getFromDef("Arena")
size = arena.getField("floorSize")
sizeVec = size.getSFVec2f() # vector containing the arena size

""" Obstacles """
cantO = 3  # Adjust this to the number of obstacles you have
quantOMax = 3
Obstaculos = [] # obstacle obj list
posObs = []     # obstacle positions list
posObsAct = np.empty([2,cantO])
sizeObsIn = np.empty([2,cantO])

# Obstacle initialization
for i in range(0, cantO):
    obstacle_name = f"Obs{i}"
    obstacle = supervisor.getFromDef(obstacle_name)
    pos_obstacle = obstacle.getField("translation")
    Obstaculos.append(obstacle)
    posObs.append(pos_obstacle)
    posObsAct[0][i] = posObs[i].getSFVec3f()[0]
    posObsAct[1][i] = posObs[i].getSFVec3f()[1]

# minimum distance preferred between agent and obstacle
safety_distance = 0.04 
# obstacle size to consider
sizeO = 1*Obstaculos[0].getField("majorRadius").getSFFloat()+1*Obstaculos[0].getField("minorRadius").getSFFloat()+ safety_distance 

#print(sizeO)
#print(sizeO) 0.175m
#print(Obstaculos)

""" Objetive """

objetivo = supervisor.getFromDef("OBJ")
pObj = objetivo.getField("translation")
pObjVec = pObj.getSFVec3f()

""" Agent initialization """

Agents = []           # list of agent objects
PosTodos = []         # list of agent object positions
RotTodos = []         # list of agent object rotation

PosTodosVec = []      # list of agent positions (vector itself)
RotTodosVec = []      # list of agent rotations (vector itself)


initialPositions = [] # list of initial positions object
posIniPos = []        # list of initial positions object positions
posIniPosVec = []     # list of initial positions positions (vector itself)

# agent and initial position initialization
for i in range(0, NMax):
    inipos_name = f"IniPos{i+1}"
    inipos = supervisor.getFromDef(inipos_name)
    inipos_pos = inipos.getField("translation")
    inipos_pos_vec = inipos_pos.getSFVec3f()
    initialPositions.append(inipos)
    posIniPos.append(inipos_pos)
    posIniPosVec.append(inipos_pos_vec)
    agent_name = f"Agent{i+1}"
    agent = supervisor.getFromDef(agent_name)
    agent_pos = agent.getField("translation")
    agent_rot = agent.getField("rotation")
    pos_todos_vec = agent_pos.getSFVec3f()
    rot_todos_vec = agent_rot.getSFVec3f()
    Agents.append(agent)
    PosTodos.append(agent_pos)
    RotTodos.append(agent_rot)
    PosTodosVec.append(pos_todos_vec)
    RotTodosVec.append(rot_todos_vec)
 
X = np.empty([2,N])

# Asignar posiciones random a cada agente
for a in range(0, NMax):
    if a in range(NStart,N):
        X[0,a] = random.uniform(sizeVec[1]/2-0.5,-sizeVec[1]/2+0.5) # 0.4 m so that the agent is not on the wall
        X[1,a] = random.uniform(sizeVec[0]/2-0.5,-sizeVec[0]/2+0.5)

print("X",X)

# Revision of the positions    
cW1 = 2 # agent on agent counter
while(cW1 > 1 or cW2 > 1):
    cW1 = 0
    cW2 = 0
    # Ensure the agents wont start over each other
    contR = 1 # intersection counter
    while(contR > 0):
        contR = 0
        for i in range(NStart+1, N):
            for j in range(NStart+1, N-i):
                resta = math.sqrt((X[0,i]-X[0,i+j])**2+(X[1,i]-X[1,i+j])**2)	# difference between positions
                if(abs(resta) < r):
                    X[0,i+j] = random.uniform(sizeVec[1]/2-0.4,-sizeVec[1]/2+0.4)
                    X[1,i+j] = random.uniform(sizeVec[0]/2-0.4,-sizeVec[0]/2+0.4) # intersection detected
                    contR = contR+1
        cW1 = cW1+1
    
    contRO = 1 # intersections with obstacles counters
    while(contRO > 0):
        contRO = 0
        for i in range(NStart,N):
            for j in range(1,cantO):
                # distance between agent and obstacle
                resta = math.sqrt((X[0,i]-posObs[j].getSFVec3f()[1])**2 + (X[1,i]-posObs[j].getSFVec3f()[0])**2)	
                if(abs(resta) < sizeO):
	         # position change
                    X[0,i+j] = random.uniform(sizeVec[1]/2-0.4,-sizeVec[1]/2+0.4)
                    X[1,i+j] = random.uniform(sizeVec[0]/2-0.4,-sizeVec[0]/2+0.4)
                    contRO = contRO + 1 # intersection detected
        cW2 = cW2 + 1        

Xi = X

# initializes the obstacles outside the map
for i in range(0, quantOMax):
    if (obs_active == 0):
        posObs[i].setSFVec3f([-sizeVec[0], i*0.9, -6.39203e-05])
    
# acquires virtual obstacle positions
if (r_obs == 0):
    for obs in range(0,cantO):
        posObsAct[0][obs] = posObs[obs].getSFVec3f()[0]
        posObsAct[1][obs] = posObs[obs].getSFVec3f()[1]
 
# acquires real obstacles and/or objective markers positions    
if (fisico == 1):
    if (r_obs == 1):
        for obs in range(0,cantO):
            posObsAct[0][obs] = agents_pose[obs+obs_start_marker,0]
            posObsAct[1][obs] = agents_pose[obs+obs_start_marker,1]
            posObs[obs].setSFVec3f([agents_pose[obs+obs_start_marker,0], agents_pose[obs+obs_start_marker,1], -6.39203e-05])
    if (r_obj == 1):
        pObjVec[0] = agents_pose[obj_marker,0]
        pObjVec[1] = agents_pose[obj_marker,1]
        #pObj.setSFVec3f([pObjVec[0], pObjVec[1], -6.39203e-05])

# initializes unused agents outside the map
for b in range(0, NMax):
    if (b<NStart or b>=N):
        PosTodos[b].setSFVec3f([-sizeVec[0]+1, b*0.3, 0.3])
        posIniPos[b].setSFVec3f([-sizeVec[0]+1, b*0.3, -6.39203e-05])

# loads some more initial conditions to set the scenario
if (r_initial_conditions == 1):
    PosRealAgents = initial_data['PosRealAgents']
    RotRealAgents = initial_data['RotRealAgents']
    PosRealIniPosVec = initial_data['posIniPosVec']
    posObsAct = initial_data['posObsAct']
    pObjVec = initial_data['pObjVec']
    obj_data = initial_data['obj_data']
    obs_data = initial_data['obs_data']

if (r_initial_conditions == 1):
    for i in range(0, cantO):
        posObs[i].setSFVec3f([posObsAct[0,i], posObsAct[1,i], -6.39203e-05])
    
    pObj.setSFVec3f([pObjVec[0], pObjVec[1], 0.3])
    

for b in range(NStart, N):
    if (agent_setup == 1): # random agent position spawn
        PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])
        
    elif (agent_setup == 2): # random initial position markers spawn
        posIniPos[b].setSFVec3f([X[1,b], X[0,b], 0.3])
        posIniPosVec[b] = posIniPos[b].getSFVec3f()
                
    elif (agent_setup == 3): # instant agent position based on saved setup
        with open('D:/AlejandroDigital/tesisAlejandro/codigo/comunicacion_pololu/first_setup.pickle','rb') as f:
            setup_pos = pickle.load(f)
        PosTodos[b].setSFVec3f([setup_pos[b,0], setup_pos[b,1], -6.39203e-05])
    
    elif (agent_setup == 4): # custom agent positioning (obsolete version of 5) 
    
        posIniPos[b].setSFVec3f([setup_pos[b,0],setup_pos[b,1], setup_pos[b,2]])
        posIniPosVec[b] = posIniPos[b].getSFVec3f()
        if (fisico == 0):  
            PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])

        elif (fisico == 1):#probarfisico 
            PosTodos[b].setSFVec3f([agents_pose[b,0], agents_pose[b,1], -6.39203e-05])
            RotTodos[b].setSFRotation([0, 0, 1, agents_pose[b,3]])
            PosTodosVec[b] = [agents_pose[b,0], agents_pose[b,1], -6.39203e-05]
            RotTodosVec[b] = [0, 0, 1, agents_pose[b,3]]
    
    elif (agent_setup == 5): # custom agent positioning 
        if (initial_pos_setup == 0):   # sets initial positions at random
            posIniPos[b].setSFVec3f([X[1,b], X[0,b], 0.3])
            
        elif (initial_pos_setup == 1): # sets initial positions in a planned way
            posIniPos[b].setSFVec3f([setup_pos[b,0],setup_pos[b,1], setup_pos[b,2]])
            
        if (fisico == 0):
            
            if (r_initial_conditions == 0):  # sets agents at random
                PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])
                if (initial_pos_setup == 1): #sets initial positions in a planned way
                    PosTodos[b].setSFVec3f([setup_pos[b,0],setup_pos[b,1], -6.39203e-05])
                
            if (r_initial_conditions == 1): # replicates initial conditions from real run
                PosTodos[b].setSFVec3f([PosRealAgents[b,0], PosRealAgents[b,1], -6.39203e-05])
                RotTodos[b].setSFRotation([0, 0, 1, RotRealAgents[b,3]])
                posIniPos[b].setSFVec3f([PosRealIniPosVec[b,0], PosRealIniPosVec[b,1], 0.3])    
        if (fisico == 1):  #try elif later
            PosTodos[b].setSFVec3f([agents_pose[b,0], agents_pose[b,1], -6.39203e-05])
            RotTodos[b].setSFRotation([0, 0, 1, agents_pose[b,3]])
            PosTodosVec[b] = [agents_pose[b,0], agents_pose[b,1], -6.39203e-05]
            RotTodosVec[b] = [0, 0, 1, agents_pose[b,3]]
            
        posIniPosVec[b] = posIniPos[b].getSFVec3f()
    #pObjs[b].setSFVec3f([X[1,b], X[0,b], 0.3])
    #PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])
    #PosTodos[b].setSFVec3f([setup_pos[b,0], setup_pos[b,1], -6.39203e-05])

# Actual positions initialization
posActuales = np.zeros([2,N])
rotActuales = np.zeros([1,N])

# Agent velocities matrix initialization
V = np.zeros([2,N])

# Matriz de obstaculos
#posObsAct = np.empty([2,cantO])
# desired formation matrix generation
formation_matrix = Fmatrix(form_shape,rigidity_level)
print(formation_matrix)

# the variable cambio represents the stage in the algorithm

# stage 0: setting the scenario, previous to the actual formation alg (the agents go
# to the initial positions of the experiment. The stage lasts until every agent reaches their
# initial position

# stage 1: the agents get close to each other until the velocities norm gets below 0.5 m/s

# stage 2: the agents make the desired formation. Once the mean squared error between the
# actual formation and the desired formation falls below 0.5, that means it is good enough,
# which triggers the change to stage 3.

# stage 3: the leader agent moves towards the objective, and pulls the formation towards it,
# while also letting the formation catch up to it.


cambio = 0	
# when replicating real initial conditions the stage (cambio) is set to 1, skipping
# the first stage of setting the agents in the scenario for the experiment, since they spawn in such
# positions
if (r_initial_conditions == 1):
    cambio = 1
    begin_alg_time = 0 
# Main loop:
# once the user is satisfied with the run, it can press the 'a' key anytime to end the run
while supervisor.step(TIME_STEP) != -1:
    #print(posActuales)
    # virtual world (Webots) mode
    if (fisico == 0):
        #updates the position information of virtual obstacles and objective
        for obs in range(0,cantO):
            posObsAct[0][obs] = posObs[obs].getSFVec3f()[0]
            posObsAct[1][obs] = posObs[obs].getSFVec3f()[1]
        
        pObjVec = pObj.getSFVec3f()
    
    # real world (Robotat) mode
    if (fisico == 1):
        #lock.acquire()
        
        # updates the position information of the markers in use from the real world
        try:#probar locks y quitar try
            agents_pose = update_data(robotat,robotat_markers)
            for marker in range(len(agents_pose)):
                agents_pose[marker,3] = agents_pose[marker,3] - desfases_euler[marker,3]
        except:
            #if the information acquisition is interrupted for some reason it uses the last known position acquired
            agents_pose = agents_pose_old
        agents_pose_old = agents_pose
        #lock.release()
        #agents_pose = update_data()
        # updates the real position information of the markers representing the obstacles
        if (r_obs == 1):
            for obs in range(0,cantO):
                posObsAct[0][obs] = agents_pose[obs+obs_start_marker,0]
                posObsAct[1][obs] = agents_pose[obs+obs_start_marker,1]
                # updates the current position of the obstacles in a visual way according to the real markers
                if (r_webots_visual == 1):
                    posObs[obs].setSFVec3f([agents_pose[obs+obs_start_marker,0], agents_pose[obs+obs_start_marker,1], -6.39203e-05])

        # updates the current position of the virtual obstacles
        if (r_obs == 0):
            for obs in range(0,cantO):
                posObsAct[0][obs] = posObs[obs].getSFVec3f()[0]
                posObsAct[1][obs] = posObs[obs].getSFVec3f()[1]
        # updates the real position information of the markers representing the objective
        if (r_obj == 1):
            pObjVec[0] = agents_pose[obj_marker,0]
            pObjVec[1] = agents_pose[obj_marker,1]
             # updates the current position of the objective in a visual way according to the real marker
            if (r_webots_visual == 1):
                pObj.setSFVec3f([pObjVec[0], pObjVec[1], -6.39203e-05])
        # updates the current position of the virtual objective
        if (r_obj == 0):
            pObjVec = pObj.getSFVec3f() 
        
    #print("cambio",cambio)
    	
    # Current poses of the agents are updated
    for c in range(NStart,N):
        # virtual world
        if (fisico == 0):
            posC = Agents[c].getField("translation")
            rotC = Agents[c].getField("rotation")
            posActuales[0][c] = posC.getSFVec3f()[0]
            posActuales[1][c] = posC.getSFVec3f()[1]
            rotActuales[0][c] = rotC.getSFVec3f()[3]*180/math.pi
        # real world    
        elif (fisico == 1):
            posActuales[0][c] = agents_pose[c][0]
            posActuales[1][c] = agents_pose[c][1]  
            rotActuales[0][c] = agents_pose[c][3]+90
                
        if(rotActuales[0][c] < 0):
                rotActuales[0][c] = rotActuales[0][c] + 360   
    # synchronization and formation control algorithm
    for g in range(NStart,N):
        E0 = 0
        E1 = 0
        for h in range(NStart,N):
            dist = np.asarray([posActuales[0][g]-posActuales[0][h], posActuales[1][g]-posActuales[1][h]]) # vector xi - xj   
            mdist = math.sqrt(dist[0]**2 + dist[1]**2)	 # euclidean norm vector xi - xj
            dij = formation_edge*formation_matrix[g][h]	 # desired distance between agents i y j
            
	# Weight added to the consensus equation
            if(mdist == 0 or mdist >= R):
                w = 0
            else:
                # stage 1: get agents close to each other
                if(cambio == 1 or cambio == 0): # start: get the agents close together without colliding
                    #print("collision avoidance")
                    w = 0.05*(mdist - (2*(r+0.05)))/(mdist - (r+0.05))**2 
                    #w = (mdist - (2*(r+0.05)))/(mdist - (r+0.05))**2 	# collision avoidance
                elif (cambio == 2 or cambio == 3):
                    if(dij == 0):	 # if there is no edge, a flat function is used as collision avoidance
                        #print("cosh")
                        w = 0.15*math.sinh(15*mdist-6)/mdist 		
                    else:         # collision avoidance & formation control
                        #print("formacion")
                        w = (4*(mdist - dij)*(mdist - r) - 2*(mdist - dij)**2)/(mdist*(mdist - r)**2)
                
            # edge (arista) tension between agents
            # weight applied
            E0 = E0 + 5*w*dist[0]
            E1 = E1 + 5*w*dist[1]
        # Collision avoidance with obstacles
        for j in range(0,cantO):
            distO0 = posActuales[0,g] - posObsAct[0][j]
            distO1 = posActuales[1,g] - posObsAct[1][j]  
            mdistO = math.sqrt(distO0**2 + distO1**2) - sizeO

            if(abs(mdistO) < 0.0001):
                mdistO = 0.0001
            w = -1/(mdistO**2)

            E0 = E0 + 0.6*w*distO0
            E1 = E1 + 0.6*w*distO1    
        # Velocities update
        V[0][g] = -1*(E0)*TIME_STEP/1000 
        V[1][g] = -1*(E1)*TIME_STEP/1000 

    # When near the desired position switch control
    normV2 = 0
    # calculates the norm of the velocities of the agents
    for m in range(NStart,N):
        nV2 = V[0][m]**2 + V[1][m]**2
        normV2 = normV2 + nV2
    normV = math.sqrt(normV2)
    print("normV", normV)
    
    #calculates the adjacency matrix of the current formation
    actual_adjacency = (1/formation_edge)*funciones.DistBetweenAgents(posActuales,NStart,N) 
    #calculates the mse between the current formation and the desired one
    formation_mse = funciones.FormationError(actual_adjacency, Fmatrix(form_shape,rigidity_level),NStart,N)
    # start stage 2: build formation
    if(normV < 0.5 and cambio == 1):
        form_cycle = ciclo
        cambio = 2
    # start stage 3: leader starts following objective and pulls formation
    elif(formation_mse < 0.5 and cambio == 2):
        obj_cycle = ciclo
        cambio = 3    
#normV <2
    # stage 0: agents go to their initial positions for the scenario/experiment
    if (cambio == 0):
        ready_ini_pos = 0
        cont_N = 0
        for obj in range(NStart,N):
            cont_N = cont_N + 1
            V[0][obj] = V[0][obj] - 5*(posActuales[0][obj]-posIniPosVec[obj][0])
            V[1][obj] = V[1][obj] - 5*(posActuales[1][obj]-posIniPosVec[obj][1])
            if ((posActuales[0][obj]-posIniPosVec[obj][0])<0.05 and (posActuales[1][obj]-posIniPosVec[obj][1])<0.05):
                ready_ini_pos = ready_ini_pos + 1
        if (ready_ini_pos == cont_N):
            # when all agents are in their positions start stage 1 (algorithm itself)
            begin_alg_time = ciclo
            cambio = 1
            if (fisico == 1):
                for b in range(NStart, N):
                    PosTodosVec[b] = [agents_pose[b,0], agents_pose[b,1], -6.39203e-05]
                    RotTodosVec[b] = [0, 0, 1, agents_pose[b,3]]
                PosRealAgents = np.array(PosTodosVec)
                RotRealAgents = np.array(RotTodosVec)                            
        #print(V)
    # stage 3: objective following    
    if (cambio == 3):
        # if leader is at least 0.7 m away from the objective it pulls and waits for the formation according to the current mse
        if (abs(posActuales[0][NStart]-pObjVec[0]) > 0.7 or abs(posActuales[1][NStart]-pObjVec[1]) > 0.7):     
            V[0][NStart] = V[0][NStart] - total_agent_weight*(1/(formation_mse))*(posActuales[0][NStart]-pObjVec[0])
            V[1][NStart] = V[1][NStart] - total_agent_weight*(1/(formation_mse))*(posActuales[1][NStart]-pObjVec[1])
        # if the leader is less than 0.7 m away from the objective the constant is higher so that it can pull the formation faster
        elif (abs(posActuales[0][NStart]-pObjVec[0]) <= 0.7 or abs(posActuales[1][NStart]-pObjVec[1]) <= 0.7):
            V[0][NStart] = V[0][NStart] - 10*(posActuales[0][NStart]-pObjVec[0])
            V[1][NStart] = V[1][NStart] - 10*(posActuales[1][NStart]-pObjVec[1])
        # when the leader is in 0.5 m proximity of the objective it is considered a success
        if (abs(posActuales[0][NStart]-pObjVec[0]) <= 0.5 and abs(posActuales[1][NStart]-pObjVec[1]) <= 0.5):
            obj_success = 1
            if (obj_cont == 0):
                obj_success_cycle = ciclo
            obj_cont = 1
#1/(errorF*10) o 4
    # data synchronization between the Supervisor program (centrol control unit) and the agents programs
    lock.acquire()                                     # ensures stable comms
    pick_V = pickle.dumps(V)                           # saves data in pickle file
    shm1.buf[:len(pick_V)] = pick_V                    # sends pickle file to shared memory space for the agent to read
    pick_agents_pose = pickle.dumps(agents_pose)       # same procedure
    shm2.buf[:len(pick_agents_pose)] = pick_agents_pose
    lock.release()
    # data storing process of the run
    trajectory.append(posActuales.copy())
    velocityHist.append(V.copy())
    normVHist.append(normV)
    objHist.append(pObjVec.copy())
    obsHist.append(posObsAct.copy())
    formation_mseHist.append(formation_mse)
    rotHist.append(rotActuales.copy())
    print(ciclo)
    print(cambio) 
    #print(formation_mse)  
    ciclo = ciclo + 1     
    
    # when the 'a' key is pressed the run is ended which triggers the following:
    # - the relevant information of the run is stored in a .npz file
    # - every agent is stopped (velocities set to 0)
    if keyboard.is_pressed('a'):
        V = np.zeros([2,N]) #agents stopped
        lock.acquire()
        pick_V = pickle.dumps(V)
        shm1.buf[:len(pick_V)] = pick_V
        pick_agents_pose = pickle.dumps(agents_pose)
        shm2.buf[:len(pick_agents_pose)] = pick_agents_pose
        # relevant data saved
        trajectory_data = np.array(trajectory)
        velocity_data = np.array(velocityHist)
        normV_data = np.array(normVHist) 
        obj_data = np.array(objHist) 
        obs_data = np.array(obsHist)
        formation_mse_data = np.array(formation_mseHist)
        rot_data = np.array(rotHist)
        NStart = NStart + 1
        obs_start_marker = obs_start_marker + 1 
        obj_marker = obj_marker + 1
        # if a new run then saved in npz file with a name of your choosing
        if (r_initial_conditions == 0):
            np.savez('trial0.npz', trajectory_data = trajectory_data, # agents positions register of the run
                                       velocity_data = velocity_data, # agents velocities registrr of the run
                                       normV_data = normV_data,       # agents velocities norm register of the run
                                       obj_data = obj_data,           # objetive positions register of the run
                                       obs_data = obs_data,           # objetive positions register of the run 
                                       formation_mse_data = formation_mse_data, # mse register of the run
                                       rot_data = rot_data,           # rotation data register of the run
                                       total_cycle = ciclo,           # total of cycles of the run
                                       form_cycle = form_cycle,       # cycle when formation began its construction
                                       obj_cycle = obj_cycle,         # cycle when the leader began following the objective
                                       quantO = cantO,                # total quantity of obstacles
                                       posObsAct = posObsAct,         # last position of obstacles when the run ended
                                       sizeO = sizeO,                 # size of the obstacles
                                       NStart = NStart,               # first agent (lower limit of the interval of agents)
                                       N = N,                         # last agent (higher limit of the interval of agents)
                                       NMax = NMax,                   # maximum agent number that the formation shape can contain
                                       pObjVec = pObjVec,             # last position of objective when the run ended
                                       PosRealAgents = PosRealAgents, # position of the agents at the start of stage 1 (initial conditions)
                                       RotRealAgents = RotRealAgents, # rotation of the agents at the start of stage 1 (initial conditions)
                                       begin_alg_time = begin_alg_time, # cycle when the algorithm itself started (aka start of stage 1)
                                       posIniPosVec = posIniPosVec, # position of initial position marks
                                       fisico = fisico,               # physical (Robotat) or virtual (Webots) world run
                                       r_initial_conditions = r_initial_conditions, # real initial conditions active or not (fresh run)
                                       r_obs = r_obs,                 # real or virtual obstacles
                                       r_obj = r_obj,                 # real or virtual objective
                                       TIME_STEP = TIME_STEP,         # time step of the program
                                       agent_setup = agent_setup,     # agent setup used for the run
                                       obs_active = obs_active,       # obstacles active or not
                                       initial_pos_setup = initial_pos_setup, # initial position setup (random or not)
                                       r = r,                         # radio to consider to avoid collisions
                                       R = R,                         # Radar radio
                                       MAX_SPEED = MAX_SPEED,         # allowed maximum speed of agents wheels
                                       form_shape = form_shape,       # shape of the formation    
                                       rigidity_level = rigidity_level, # rigidity level of the formation 
                                       total_agent_number = total_agent_number, # total agent number of agents involved in the run
                                       obj_marker = obj_marker,       # Robotat marker used for the objetive in real life
                                       obs_start_marker = obs_start_marker, # Robotat starting marker used for the obstacles in real life
                                       setup_starting_point = setup_starting_point, # beginning of the initial positions shape
                                       setup_shape = setup_shape,     # initial positions shape
                                       setup_shape_space = setup_shape_space, # what space to cover with the initial positions
                                       formation_edge = formation_edge, # how long is the age of the formation
                                       r_f = r_f,                     # robot dimensions for unicycle model
                                       l_f = l_f,
                                       a_f = a_f,
                                       obj_success = obj_success,     # indicates if the objective was successful
                                       obj_success_cycle = obj_success_cycle) # objective success cycle      
        
        if (r_initial_conditions == 1):
            try: 
                import re
                from prettytable import PrettyTable
                # Define a regular expression pattern to match either "_h_" or "_f_"
                pattern = re.compile(r'(_[hf]_)')
                filename_without_extension = initial_conditions_file.split('.')[0]
                # Use re.sub to replace the matched pattern with '_v_'
                formatted_file = re.sub(pattern, '_v_', initial_conditions_file)
                table_namefile = re.sub(pattern, '_t_', filename_without_extension)
                   
                np.savez(formatted_file, trajectory_data = trajectory_data,\
                                       velocity_data = velocity_data,\
                                       normV_data = normV_data,\
                                       obj_data = obj_data,\
                                       obs_data = obs_data,\
                                       formation_mse_data = formation_mse_data,\
                                       rot_data = rot_data,\
                                       total_cycle = ciclo,\
                                       form_cycle = form_cycle,\
                                       obj_cycle = obj_cycle,\
                                       quantO = cantO,\
                                       posObsAct = posObsAct,\
                                       sizeO = sizeO,\
                                       NStart = NStart,\
                                       N = N,\
                                       NMax = NMax,\
                                       pObjVec = pObjVec,\
                                       PosRealAgents = PosRealAgents,\
                                       RotRealAgents = RotRealAgents,\
                                       begin_alg_time = begin_alg_time,\
                                       posIniPosVec = posIniPosVec,\
                                       fisico = fisico,\
                                       r_initial_conditions = r_initial_conditions,\
                                       r_obs = r_obs,\
                                       r_obj = r_obj,\
                                       TIME_STEP = TIME_STEP,\
                                       agent_setup = agent_setup,\
                                       obs_active = obs_active,\
                                       initial_pos_setup = initial_pos_setup,\
                                       r = r,\
                                       R = R,\
                                       MAX_SPEED = MAX_SPEED,\
                                       form_shape = form_shape,\
                                       rigidity_level = rigidity_level,\
                                       total_agent_number = total_agent_number,\
                                       obj_marker = obj_marker,\
                                       obs_start_marker = obs_start_marker,\
                                       setup_starting_point = setup_starting_point,\
                                       setup_shape = setup_shape,\
                                       setup_shape_space = setup_shape_space,\
                                       formation_edge = formation_edge,\
                                       r_f = r_f,\
                                       l_f = l_f,\
                                       a_f = a_f,\
                                       obj_success = obj_success,\
                                       obj_success_cycle = obj_success_cycle)
                                       
                funciones.figure_gen(initial_conditions_file, 1)
                funciones.figure_gen(formatted_file, 1)
                funciones.table_gen(initial_conditions_file,formatted_file)
                       
            except e:
                print(e)
                np.savez('trial0.npz', trajectory_data = trajectory_data, # agents positions register of the run
                                       velocity_data = velocity_data, # agents velocities registrr of the run
                                       normV_data = normV_data,       # agents velocities norm register of the run
                                       obj_data = obj_data,           # objetive positions register of the run
                                       obs_data = obs_data,           # objetive positions register of the run 
                                       formation_mse_data = formation_mse_data, # mse register of the run
                                       rot_data = rot_data,           # rotation data register of the run
                                       total_cycle = ciclo,           # total of cycles of the run
                                       form_cycle = form_cycle,       # cycle when formation began its construction
                                       obj_cycle = obj_cycle,         # cycle when the leader began following the objective
                                       quantO = cantO,                # total quantity of obstacles
                                       posObsAct = posObsAct,         # last position of obstacles when the run ended
                                       sizeO = sizeO,                 # size of the obstacles
                                       NStart = NStart,               # first agent (lower limit of the interval of agents)
                                       N = N,                         # last agent (higher limit of the interval of agents)
                                       NMax = NMax,                   # maximum agent number that the formation shape can contain
                                       pObjVec = pObjVec,             # last position of objective when the run ended
                                       PosRealAgents = PosRealAgents, # position of the agents at the start of stage 1 (initial conditions)
                                       RotRealAgents = RotRealAgents, # rotation of the agents at the start of stage 1 (initial conditions)
                                       begin_alg_time = begin_alg_time, # cycle when the algorithm itself started (aka start of stage 1)
                                       posIniPosVec = posIniPosVec, # position of initial position marks
                                       fisico = fisico,               # physical (Robotat) or virtual (Webots) world run
                                       r_initial_conditions = r_initial_conditions, # real initial conditions active or not (fresh run)
                                       r_obs = r_obs,                 # real or virtual obstacles
                                       r_obj = r_obj,                 # real or virtual objective
                                       TIME_STEP = TIME_STEP,         # time step of the program
                                       agent_setup = agent_setup,     # agent setup used for the run
                                       obs_active = obs_active,       # obstacles active or not
                                       initial_pos_setup = initial_pos_setup, # initial position setup (random or not)
                                       r = r,                         # radio to consider to avoid collisions
                                       R = R,                         # Radar radio
                                       MAX_SPEED = MAX_SPEED,         # allowed maximum speed of agents wheels
                                       form_shape = form_shape,       # shape of the formation    
                                       rigidity_level = rigidity_level, # rigidity level of the formation 
                                       total_agent_number = total_agent_number, # total agent number of agents involved in the run
                                       obj_marker = obj_marker,       # Robotat marker used for the objetive in real life
                                       obs_start_marker = obs_start_marker, # Robotat starting marker used for the obstacles in real life
                                       setup_starting_point = setup_starting_point, # beginning of the initial positions shape
                                       setup_shape = setup_shape,     # initial positions shape
                                       setup_shape_space = setup_shape_space, # what space to cover with the initial positions
                                       formation_edge = formation_edge, # how long is the age of the formation
                                       r_f = r_f,                     # robot dimensions for unicycle model
                                       l_f = l_f,
                                       a_f = a_f,
                                       obj_success = obj_success,     # indicates if the objective was successful
                                       obj_success_cycle = obj_success_cycle) # objective success cycle      
        if (fisico == 1):
            robotat_disconnect(robotat)
        lock.release()
        #shm1.close()
        #shm2.close()  
        break

    
     