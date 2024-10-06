import time 
import numpy as np
import csv
import matplotlib.pyplot as plt
import os

""" selección de archivo """
guardar = 0 # 0: no guardar datos | 1: si guardar datos
optimizado = 0 # 0: no optimizado | 1: optimizado
file_name = 'TiempoNoOptim_8A_AB1C_f_1'

""" configuración de ruta y textos """
archivo = f'{file_name}.npz'
img_folder = f'{file_name}'

if optimizado == 1:
    folder = 'tiempos_optim' # folder con los datos de la corrida
    ruta = f'{folder}/{archivo}'
    csv_filename = "tiempos_optim.csv" # csv para guardar datos
    figure_title = 'corrida optimizada'
elif optimizado == 0:
    folder = 'tiempos_no_optim' # folder con los datos de la corrida
    ruta = f'{folder}/{archivo}'
    csv_filename = "tiempos_no_optim.csv" # csv para guardar datos 
    figure_title = 'corrida no optimizada'
    
img_folder_rute = os.path.join(folder, img_folder)

"""" extracción de datos"""
data = np.load(ruta)
tiempo_total = data['tiempo_total']
tiempo_ciclo = data['tiempo_ciclo']
ciclos = data['total_cycle']
agentes = data['N']
corrida_numero = data['corrida_numero']

tiempo_ciclo_med = np.average(tiempo_ciclo)

print(f'Agentes: {agentes}')
print(f'Corrida: {corrida_numero}')
print(f'Tiempo (s) = {tiempo_total: .6f}')
print(f'Tiempo de ciclo promedio (ms): {tiempo_ciclo_med}\n')

""" graficar """
plt.figure(figsize=(40,20))
plt.xlim(0, ciclos)
plt.ylim(min(tiempo_ciclo), max(tiempo_ciclo))
plt.xlabel('Ciclos')
plt.ylabel('Tiempo de ciclo (ms)')
plt.title(f'Tiempo de cada ciclo con {agentes} agentes en {figure_title} {corrida_numero}')

x = np.arange(1,ciclos+1)
plt.plot(x, tiempo_ciclo, color='darkblue')

""" guardado de datos """
if guardar == 1:
    # crear folder para imagenes
    if not os.path.exists(img_folder_rute):
        os.makedirs(img_folder_rute)
        print(f'Carpeta {img_folder_rute} creada correctamente')
        
    # datos a guardar
    if not os.path.exists(f'{folder}/{csv_filename}'):
        data = [
            ['Agentes', 'Corrida', 'Tiempo (s)', 'Tiempo de ciclo promedio (ms)'],
            [agentes, corrida_numero, np.round(tiempo_total,3), np.round(tiempo_ciclo_med,3)]
        ]
    else:
        data = [
            [agentes, corrida_numero, np.round(tiempo_total,3), np.round(tiempo_ciclo_med,3)]
        ]
    # guardar los datos en un archivo CSV
    with open(f'{folder}/{csv_filename}', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Datos guardados exitosamente en \n{csv_filename}\n")
    
    # guardar gráfica
    plt.savefig(f'{img_folder_rute}/{file_name}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'{img_folder_rute}/{file_name}.png', format='png', bbox_inches='tight')
    print(f"Imágenes guardadas exitosamente en \n{img_folder}")
