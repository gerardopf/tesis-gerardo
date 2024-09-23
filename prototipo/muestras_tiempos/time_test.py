import time 
import numpy as np
import csv

archivo = '22sepTest_3A_NNN_v_1.npz'
data = np.load(archivo)


tiempo_mainVec = data['tiempo_mainVec']
tiempo_robotatVec = data['tiempo_robotatVec']
tiempo_total = data['tiempo_total']
ciclos = data['total_cycle']
agentes = data['N']
corrida_numero = data['corrida_numero']

print(f'muestras: {ciclos}')
print(f'tiempo de corrida (s) = {tiempo_total: .6f}\n')

tiempo_ciclo_media = np.mean(tiempo_mainVec)
tiempo_ciclo_std = np.std(tiempo_ciclo_media)
tiempo_ciclo_max = np.max(tiempo_mainVec)
tiempo_ciclo_min = np.min(tiempo_mainVec)

tiempo_robotat_media = np.mean(tiempo_robotatVec)
tiempo_robotat_std = np.std(tiempo_robotat_media)
tiempo_robotat_max = np.max(tiempo_robotatVec)
tiempo_robotat_min = np.min(tiempo_robotatVec)

print('Tiempo de ciclo:')
print(f'Media (ms) = {tiempo_ciclo_media: .6f}')
print(f'Desviación estándar (ms) = {tiempo_ciclo_std: .6f}')
print(f'Max: {tiempo_ciclo_max}')
print(f'Min: {tiempo_ciclo_min}\n')

print('Tiempo al obtener poses:')
print(f'Media (ms) = {tiempo_robotat_media: .6f}')
print(f'Desviación estándar (ms) = {tiempo_robotat_std: .6f}')
print(f'Max: {tiempo_robotat_max}')
print(f'Min: {tiempo_robotat_min}')

