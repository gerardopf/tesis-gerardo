import os
import numpy as np
from funciones_conjunto import *


# """ conexión rootat """
# robotat = robotat_connect()

# """ obtener poses """
# markers = [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
# poses = robotat_get_pose(robotat, markers)
# poses_eul = quat2eul(poses, 'zyx')
# #print(poses)

# """" guardar solo offsets en array """
# i = 0
# marker_offsets = []
# for pose_marker in poses_eul:
#     marker_offsets.append(pose_marker[3])
#     i = i + 1
# vector_offsets = np.array(marker_offsets)
# #print("offsets medidos: \n", vector_offsets)



""" guardar datos """
#print(os.path.abspath(".")) # ver el path actual

#np.save('calibracion_markers_poses_quat.npy', poses) # guardar poses en quaterniones
#np.save('calibracion_markers_poses_eul.npy', poses_eul) # guardar poses en euler zyx
#np.save('calibracion_markers_nuevo.npy', vector_offsets) # guardar solo desfases en euler zyx

""" cargar datos y comparar """
m = np.load('calibracion_markers_inicial.npy') # poses completas original (quat)
#m2 = np.load('calibracion_markers_nuevo.npy') # solo offsets nuevos (eul)
m3 = np.load('calibracion_markers_poses_quat.npy')
#m4 = np.load('calibracion_markers_poses_eul.npy')

#np.savetxt("calibracion_markers_nuevo.csv", m2, delimiter=",") # guardar solo desfases en euler zyx (txt)

""" agregar desfases faltantes marker 1 y 9 al nuevo archivo """
print("m3: \n", m3)
print(len(m3))
marker1 = m[0]
marker9 = m[8]
print("markers: \n")
print(marker1)
print(marker9)

vector = np.zeros((22, 7))

vector[0] = marker1
vector[1] = m3[0]
vector[2] = m3[1]
vector[3] = m3[2]
vector[4] = m3[3]
vector[5] = m3[4]
vector[6] = m3[5]
vector[7] = m3[6]
vector[8] = marker9
vector[9] = m3[7]
vector[10] = m3[8]
vector[11] = m3[9]
vector[12] = m3[10]
vector[13] = m3[11]
vector[14] = m3[12]
vector[15] = m3[13]
vector[16] = m3[14]
vector[17] = m3[15]
vector[18] = m3[16]
vector[19] = m3[17]
vector[20] = m3[18]
vector[21] = m3[19]
    
print("vector \n", vector)

markers_nuevo_eul = quat2eul(vector, 'zyx')
print("euler \n",markers_nuevo_eul)

""" guardar nuevos desfases """
# print(os.path.abspath(".")) # ver el path actual
# np.save('nueva_calibracion_markers_1_al_22.npy', vector) # guardar poses en quaterniones
    

