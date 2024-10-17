""" =========================================================================
% AGENT CONTROLLER FOR LINEAR TO RADIAL VELOCITY TRANSFORMATION OF THE WHEELS
% =========================================================================
% Author: José Alejandro Rodríguez Porras
% =========================================================================
% The following script implements the necessary transformations so that the 
% differential robots move to the velocity determined by the Supervisor 
% program.
% It is a Robot controller.

% The controller is used to control each robot individually, receiving the 
% individual instruction so that the robot executes the program. For example,
% if we are running the controller on robot # 1, it only process the
% instructions related to that specific robot.
========================================================================="""

"""pruebaMatrizDifeomorfismo controller."""

# Import de librerías
from controller import Robot, Compass, Motor
import math
import numpy as np
import pickle
import keyboard
from multiprocessing import shared_memory, Lock
from funciones_conjunto_3pi import *
import time

time.sleep(1)
TIME_STEP = 64 # each step of the simulation is 64 ms
MAX_SPEED = 6.28 # rad/s, virtual agents --> epucks
MAX_SPEED_f = 30 # rpm, physical agents --> pololus

# shared memory spaces to receive the supervisor program instructions 
# with each individual agent program
shm1 = shared_memory.SharedMemory(name="my_shared_memory1")
shm2 = shared_memory.SharedMemory(name="my_shared_memory2")
# synchronization Lock to ensure a stable communication between 
# programs (IPC, interprocess communication)
lock = Lock()
fisico = 1 # 0: Webots, 1: Robotat, has to match supervisor fisico parameter.
NStart = 2 # First agent (lower limit of the interval of agents)
N = 3      # Last agent (higher limit of the interval of agents)

# NStart and N have to be the same as they are configured 
# in the Supervisor program, depending on how many agents are to be used

# Webots mode (epucks)
if (fisico == 0):

    # Robot dimensions (epucks)
    r = 0.0205
    l = 0.0355
    a = 0.0355
    
    # Robot instance.
    robot = Robot()
    argc = int(robot.getCustomData()) #receives the agent number from the robot field
    # called custom data
    
    # Enable compass
    compass = robot.getDevice("compass")
    compass.enable(TIME_STEP)
    robot.step(TIME_STEP)
    
    # get a handler to the motors and set target position to infinity (speed control)
    leftMotor = robot.getDevice('left wheel motor')
    rightMotor = robot.getDevice('right wheel motor')
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    
    # Main loop:
    while robot.step(TIME_STEP) != -1:
        # current positions and final positions according to Supervisor
        lock.acquire()
        pick_V = shm1.buf[:shm1.size] # receive instructions from supervisor
        lock.release()
        V = pickle.loads(pick_V)
                
        # Velocities
        
        # Robot orientation
        comVal = compass.getValues()
        angRad = math.atan2(comVal[0],comVal[1]) # they are input as (x,y) instead of (y,x) to compensate for the 90° desfase in physical
        angDeg = (angRad/math.pi)*180
        if(angDeg < 0):
            angDeg = angDeg + 360
        theta_o = angDeg
        #Transformation of angular and linear velocity
        v = (V[0][argc])*(math.cos(theta_o*math.pi/180)) + (V[1][argc])*(math.sin(theta_o*math.pi/180))
        w = (V[0][argc])*(-math.sin(theta_o*math.pi/180)/a) + (V[1][argc])*(math.cos(theta_o*math.pi/180)/a)
        
        # Wheel velocities calculation 
        phi_r = (v+(w*l))/r
        phi_l = (v-(w*l))/r
        # Maximum velocity truncation
        if(phi_r > 0):
            if(phi_r > MAX_SPEED):
                phi_r = MAX_SPEED
        else:
            if(phi_r < -MAX_SPEED):
                phi_r = -MAX_SPEED
                
        if(phi_l > 0):
            if(phi_l > MAX_SPEED):
                phi_l = MAX_SPEED
        else:
            if(phi_l < -MAX_SPEED):
                phi_l = -MAX_SPEED
        
        # Velocity assignment of the wheels 
        leftMotor.setVelocity(phi_l)
        rightMotor.setVelocity(phi_r)
        pass

# Robotat mode  (pololu 3pi+)    
elif (fisico == 1):
    # Robot dimensions
    # epuck
    r = 0.0205
    l = 0.0355
    a = 0.0355
    # pololu
    r_f = 0.017
    l_f = 0.0485
    a_f = 0.0485
    
    # Robot instance.
    robot = Robot()
    argc = int(robot.getCustomData()) #receives the agent number from the robot field
    # called custom data
    
    agente = argc + 1 # to match python index convention of lists
    
    # attempt to connect to the respective agent 
    if (NStart <= agente <= N): 
        try:
            pololu = robotat_3pi_connect(agente)
        except:
            print("error, could not connect to the Pololu 3Pi+")
            pass

    robot.step(TIME_STEP)    
    
    # Main loop:
    while robot.step(TIME_STEP) != -1:
        # current positions and final positions according to Supervisor
        lock.acquire()
        pick_V = shm1.buf[:shm1.size]
        pick_agents_pose = shm2.buf[:shm2.size]
        lock.release()
        V = pickle.loads(pick_V)
        agents_pose = pickle.loads(pick_agents_pose)
        
        theta_o_f = agents_pose[argc][3]+90 # 90° degree compensation for the real life orientation
        if(theta_o_f < 0):
            thetha_o_f = theta_o_f + 360
        # linear and angular velocity transformation
        v_f = (V[0][argc])*(math.cos(theta_o_f*math.pi/180)) + (V[1][argc])*(math.sin(theta_o_f*math.pi/180))
        w_f = (V[0][argc])*(-math.sin(theta_o_f*math.pi/180)/a_f) + (V[1][argc])*(math.cos(theta_o_f*math.pi/180)/a_f)
        
        # wheels velocity calculation           
        phi_r_f = (v_f+(w_f*l_f))*10/(r_f*10)
        phi_l_f = (v_f-(w_f*l_f))*10/(r_f*10)
        
        
        # Truncate velocities to max speed limit if surpass the limit
        if(phi_r_f > 0):
            if(phi_r_f > MAX_SPEED_f):
                phi_r_f = MAX_SPEED_f
        else:
            if(phi_r_f < -MAX_SPEED_f):
                phi_r_f = -MAX_SPEED_f
                
        if(phi_l_f > 0):
            if(phi_l_f > MAX_SPEED_f):
                phi_l_f = MAX_SPEED_f
        else:
            if(phi_l_f < -MAX_SPEED_f):
                phi_l_f = -MAX_SPEED_f
        
        # send speeds to selected virtual agents
        if (NStart <= agente <= N):
            try:
                robotat_3pi_set_wheel_velocities(pololu, phi_l_f, phi_r_f)
            except:
                #print("error, no se pudo conectar al pololu")
                pass
            
        if keyboard.is_pressed('a'):
            if (NStart <= agente <= N):    
                try:
                    robotat_3pi_force_stop(pololu)
                    robotat_3pi_disconnect(pololu)
                except:
                    #print("error, no se pudo conectar al pololu")
                    pass
            break
        pass
        