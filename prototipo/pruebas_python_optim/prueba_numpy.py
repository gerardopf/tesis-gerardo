import numpy as np
from funciones_conjunto import  *

agentes = [2,5,10]
obs = [18,19,20]
obj = [11]

NMax = 10

markers = agentes + obj + obs
print(f"markers {markers} \n")

N = len(markers)

desfases = np.load('nueva_calibracion_markers_1_al_22.npy')
desfases_euler = quat2eul(desfases,'zyx')
print(f"desfases euler \n {desfases_euler} \n")

desfases_numpy = np.zeros((N, 6))
prueba = np.ones((N,6))

index = 0
for marker in markers:
    desfases_numpy[index,3] = desfases_euler[marker-1, 3]
    index = index + 1

prueba = prueba + desfases_numpy
print(f"prueba\n {prueba} \n")

