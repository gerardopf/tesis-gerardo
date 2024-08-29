# prueba_funciones_combinadas.py

import time
from funciones_conjunto_3pi import *
from funciones_conjunto import *
robotat = robotat_connect()
if robotat:
    print("connected to robotat")
else:
    print("error")

try:
    agentes = [2,3]
    n = len(agentes)
    print("Number of agents:\n",n)
    
    pose = robotat_get_pose(robotat, agentes)
    print("Pose per agent\n:", pose)
    
    robot = robotat_3pi_connect(agentes[0])
    robot2 = robotat_3pi_connect(agentes[1])
    print(f"Connected to robot ID: {robot['id']}, IP: {robot['ip']}, Port: {robot['port']}")
    print(f"Connected to robot ID: {robot2['id']}, IP: {robot2['ip']}, Port: {robot2['port']}")
    
    robotat_3pi_set_wheel_velocities(robot, 50, -50)
    robotat_3pi_set_wheel_velocities(robot2, -50, 50)
    
    robotat_disconnect(robotat)
    time.sleep(3)
    robotat = robotat_connect()
    
    pose = robotat_get_pose(robotat, agentes)
    print("Pose per agent\n:", pose)
    
    robotat_3pi_force_stop(robot)
    robotat_3pi_force_stop(robot2)
except ValueError as ve:
    print(ve)
except Exception as e:
    print('An error occurred:', e)
finally:
    robotat_3pi_disconnect(robot)
    robotat_3pi_disconnect(robot2)
    robotat_disconnect(robotat)