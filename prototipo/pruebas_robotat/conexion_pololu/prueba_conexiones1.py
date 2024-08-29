import time
from funciones_conjunto_3pi import *
from funciones_conjunto import *

try:
    agentes = [2, 3, 4, 5]
    
    # Conexión con el robotat
    robotat = robotat_connect()
    if robotat:
        print("Connected to robotat...", robotat, '\n')
    else:
        print("Error...")
    
    # Obtener pose de agentes
    pose = robotat_get_pose(robotat, agentes)
    print(pose, '\n')
    
    #time.sleep(1)
    # Conexión al pololu
    robot = robotat_3pi_connect(agentes[0])
    robot2 = robotat_3pi_connect(agentes[1])
    print(robot, '\n')
    print(robot2, '\n')
    
    # Prueba movimiento pololu
    robotat_3pi_set_wheel_velocities(robot, 50, -50)
    robotat_3pi_set_wheel_velocities(robot2, -50, 50)
    time.sleep(2)
    robotat_3pi_force_stop(robot)
    robotat_3pi_force_stop(robot2)
    
    # Desconexión
    robotat_disconnect(robotat)
    robotat_3pi_disconnect(robot)
    robotat_3pi_disconnect(robot2)
    
except Exception as e:
    print(e)

    

