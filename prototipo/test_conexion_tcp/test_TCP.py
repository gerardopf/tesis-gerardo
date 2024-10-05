from funciones_conjunto import *
import keyboard
import time
import numpy as np

def update_data(robotat, markers_to_use):
    try: 
        if robotat:
            pose = robotat_get_pose_test(robotat, markers_to_use)
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


markers = [2,3,4,5,6,7,8,10,15,20,21,22]

# Conexión con el robotat
robotat = robotat_connect()

iteraciones = 50;
tic = 0
toc = 0
tHist = []

print(f'markers: {len(markers)}')
for i in range (0,iteraciones):
    tic = time.perf_counter_ns()
    pose = update_data(robotat, markers)
    toc = time.perf_counter_ns()
    tiempo = (toc-tic)/1000000
    #print(tiempo)
    tHist.append(tiempo)
    time.sleep(0.001)
    
tHistVec = np.array(tHist)
print(f'tiempo máximo (ms): {np.max(tHistVec)}')
print(f'tiempo mínimo (ms): {np.min(tHistVec)}')
print(f'tiempo media (ms): {np.average(tHistVec)}')
print(pose)

    