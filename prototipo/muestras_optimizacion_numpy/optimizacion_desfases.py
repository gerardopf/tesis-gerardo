"""
Autor: Gerardo Paz Fuentes

Este programa tiene como propósito medir los tiempos de ejecución a la hora de
aplicar los desfases de las poses de los marcadores.

Los tiempos se miden para las funciones originales y las funciones optimizadas
con NumPy.

Se realizan 'n' muestras para encontrar un valor medio con su desviación 
estándar.

"""

import numpy as np
from funciones_conjunto import  *
import time

# markers 1
# agentes = [1,2,3,4]
# obs = [14,15,16]
# obj = [22]
# markers = agentes + obj + obs
# N = len(markers)
# print(f"markers {markers} \n")

# markers 2
N = 20
markers = []
for i in range(0,N):
    markers.append(i)
print(f"markers {markers} \n")

# iteraciones
n = 1000
tiempos_for = []
tiempos_numpy = []

desfases = np.load('nueva_calibracion_markers_1_al_22.npy')
desfases_euler = quat2eul(desfases,'zyx')
#print(f"desfases euler \n {desfases_euler} \n")

for iteracion in range (0,n):
    # test con ciclos for
    desfases_for = desfases_euler
    poses_for = np.ones((N,6))
    
    tic = time.perf_counter_ns()
    index = 0
    for marker in markers:
        poses_for[index, 3] = poses_for[index,3] - desfases_for[marker-1,3]
        index = index + 1
    toc = time.perf_counter_ns()
    t1 = (toc - tic)
    
    #print(f"tiempo for (ms): {t1: .6f}")
    #print(f"prueba\n {poses_for} \n")
    
    # test con Numpy
    desfases_numpy = np.zeros((N, 6))
    poses_numpy= np.ones((N,6))
    
    index = 0
    for marker in markers:
        desfases_numpy[index,3] = desfases_euler[marker-1, 3]
        index = index + 1
        
    tic = time.perf_counter_ns()
    poses_numpy = poses_numpy - desfases_numpy
    toc = time.perf_counter_ns()
    t2 = (toc - tic)
    
    #print(f"tiempo NumPy (ms): {t2: .6f}")
    #print(f"prueba\n {poses_numpy} \n")
    
    tiempos_for.append(t1)
    tiempos_numpy.append(t2)

tiempos_for_array = np.array(tiempos_for)
tiempos_numpy_array = np.array(tiempos_numpy)

tiempos_for_media = np.mean(tiempos_for_array)
tiempos_numpy_media = np.mean(tiempos_numpy_array)

tiempos_for_desviacion = np.std(tiempos_for_array)
tiempos_numpy_desviacion = np.std(tiempos_numpy_array)

print(f"Media tiempos con for: {tiempos_for_media: .6f}")
print(f"Desviación estándar tiempos con for: {tiempos_for_desviacion: .6f}")
print()
print(f"Media tiempos con NumPy: {tiempos_numpy_media: .6f}")
print(f"Desviación estándar tiempos con NumPy: {tiempos_numpy_desviacion: .6f}")
