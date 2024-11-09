from funciones_conjunto import *
import keyboard
import time

""" función para obtener pose de markers ROBOTAT """
def update_data(robotat, markers_to_use):
    try: 
        if robotat:
            pose = robotat_get_pose(robotat, markers_to_use)
            pose_eul = quat2eul(pose,'zyx')
            #print("poses euler: ", pose_eul)
        else: 
            print("No está conectado al Robotat")
            pose_eul = None
    except:
        print("Error al obtener poses de los markers")
        print(pose)
        pose_eul = None
    finally:
        return pose_eul   
    
markers_to_use = [2,3,4,5,6,7,15,20,21,22]
    
robotat = robotat_connect()
    
while True:
    tic_latencia = time.perf_counter_ns()
    poses = update_data(robotat, markers_to_use)
    toc_latencia = time.perf_counter_ns()
    latencia = (toc_latencia - tic_latencia)/1000000
    print(f"Latencia (ms): {latencia:.2f}")
    if keyboard.is_pressed('a'):
        break
    
