""" AGENTE """

from controller import Robot, Compass, Motor
import math
import numpy as np
import pickle
import keyboard
from multiprocessing import shared_memory, Lock
from funciones_conjunto_3pi import *
import time

time.sleep(3)

TIME_STEP = 64  # paso para simulación 64 ms
MAX_SPEED = 6.28    # simulación epucks (rad/s)
MAX_SPEED_f = 30  # físico Pololu 3Pi+ (rpm)

# creación de memoria compartida
shm1 = shared_memory.SharedMemory(name="my_shared_memory1")
shm2 = shared_memory.SharedMemory(name="my_shared_memory2")
lock = Lock()

fisico = 1 # 0: Webots | 1: Robotat

agents_marker_list = [5,3,4]
NStart = 1 # primer agente
N = len(agents_marker_list)	# último agente

# SIMULACIÓN - webots
if(fisico == 0):
    # dimensiones del robot - epuck
    r = 0.0205
    l = 0.0355
    a = 0.0355
    
    robot = Robot()
    argc = int(robot.getCustomData()) # número de agente

    # Enable compass
    compass = robot.getDevice("compass")
    compass.enable(TIME_STEP)
    robot.step(TIME_STEP)
    
    # variables para control de velocidad
    leftMotor = robot.getDevice('left wheel motor')
    rightMotor = robot.getDevice('right wheel motor')
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    
    # ------------------ MAIN LOOP ------------------
    while robot.step(TIME_STEP) != 1:
        
        # obtener velocidades del supervisor
        lock.acquire()
        pick_V = shm1.buf[:shm1.size] 
        lock.release()
        V = pickle.loads(pick_V)
        
        # orientación del robot
        comVal = compass.getValues()
        angRad = math.atan2(comVal[0],comVal[1]) # orden (x,y) en lugar de (y,x) para compensar los 90° de desfase en físico
        angDeg = (angRad/math.pi)*180
        if(angDeg < 0):
            angDeg = angDeg + 360   # ángulo siempre positivo
        theta_o = angDeg
        
        # transformar velocidad angular y lineal
        v = (V[0][argc])*(math.cos(theta_o*math.pi/180)) + (V[1][argc])*(math.sin(theta_o*math.pi/180))
        w = (V[0][argc])*(-math.sin(theta_o*math.pi/180)/a) + (V[1][argc])*(math.cos(theta_o*math.pi/180)/a)
        
        # calcular velocidad de ruedas
        phi_r = (v+(w*l))/r
        phi_l = (v-(w*l))/r
        
        # truncar velocidades
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
                
        # asignar velocidades a las ruedas
        leftMotor.setVelocity(phi_l)
        rightMotor.setVelocity(phi_r)
    
# FÍSICO - robotat
elif(fisico == 1):
    # dimensiones del robot - pololu
    r_f = 0.017
    l_f = 0.0485
    a_f = 0.0485

    robot = Robot()
    argc = int(robot.getCustomData()) # número de agente
    if(0 <= argc < len(agents_marker_list)):
        agente = agents_marker_list[argc] # hacer coincidir el índice de listas de python y matlab
    else:
        agente = -1
    
    # conectar con el robot
    if agente in agents_marker_list: 
        try:
            pololu = robotat_3pi_connect(agente)
        except:
            print("error al conectar con el agente No. ", agente)
            pass
    robot.step(TIME_STEP)    
    
    # ------------------ MAIN LOOP ------------------
    while robot.step(TIME_STEP) != -1:
        # obtener velocidad y pose desde el supervisor
        lock.acquire()
        pick_V = shm1.buf[:shm1.size]
        pick_agents_pose = shm2.buf[:shm2.size]
        lock.release()
        V = pickle.loads(pick_V)
        agents_pose = pickle.loads(pick_agents_pose)

        # orientación del robot
        theta_o_f = agents_pose[argc][3]+90 # 90° para compensar la orientación real
        if(theta_o_f < 0):
            thetha_o_f = theta_o_f + 360    # ángulo siempre positivo
            
        # transformar velocidad angular y lineal
        v_f = (V[0][argc])*(math.cos(theta_o_f*math.pi/180)) + (V[1][argc])*(math.sin(theta_o_f*math.pi/180))
        w_f = (V[0][argc])*(-math.sin(theta_o_f*math.pi/180)/a_f) + (V[1][argc])*(math.cos(theta_o_f*math.pi/180)/a_f)
        
        # calcular velocidad de ruedas        
        phi_r_f = (v_f+(w_f*l_f))*10/(r_f*10)
        phi_l_f = (v_f-(w_f*l_f))*10/(r_f*10)
        
        # truncar velocidades
        #print(f'\nagente: {agente} | phiR: {phi_r_f} | phiL {phi_l_f}')
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
        print(f'\nagente: {agente} | phiR: {phi_r_f} | phiL {phi_l_f}')

        # enviar velocidades al pololu
        if agente in agents_marker_list:
            try:
                robotat_3pi_set_wheel_velocities(pololu, phi_l_f, phi_r_f)
            except:
                print("error al enviar velocidades al agente No. ", agente)
        
        # presionar 'a' para detener
        if keyboard.is_pressed('a'):
            print("Fin de la corrida... -agente No. ", agente)
            if agente in agents_marker_list:    
                try:
                    robotat_3pi_force_stop(pololu)
                    robotat_3pi_disconnect(pololu)
                except:
                    print("error al detener y desconectar el agente No. ", agente)
            break
        pass