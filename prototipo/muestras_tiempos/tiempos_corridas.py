import time 
import numpy as np
import csv

archivo = 'TiempoOptim_2A_AB1C_f_1.npz'
data = np.load(archivo)

tiempo_total = data['tiempo_total']
ciclos = data['total_cycle']
agentes = data['N']
corrida_numero = data['corrida_numero']

print(f'Agentes: {agentes}')
print(f'Corrida: {corrida_numero}')
print(f'Tiempo (s) = {tiempo_total: .6f}\n')

# Datos a guardar
data = [
    ['Agentes', 'Corrida', 'Tiempo (s)'],
    [agentes, corrida_numero, np.round(tiempo_total,3)]
]

# Nombre del archivo CSV
filename = "tiempos_no_optim.csv"

# Guardar los datos en un archivo CSV
with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"Datos guardados exitosamente en {filename}")
