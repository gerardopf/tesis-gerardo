# Autor: José Alejandro Rodríguez Porras
# Generación de gráficas de las corridas del algoritmo, de los datos guardados en el archivo .npz, de la corrida
import numpy as np
import matplotlib.pyplot as plt

#trajectory = np.load('robot_trajec.npy')
#trajectory = np.load('trial.npy')
#trajectory = np.load('setup_traj0_formacion_2.npy')

data = np.load('trial_distance_1A_2.npz')
#print(data)

#to find out the files within the .npz
"""
data = np.load('trial.npz', allow_pickle=True)
print(data.files)
"""

trajectory = data['trajectory_data']
velocityHist = data['velocity_data']
ciclos = data['ciclo']
posObsIn = data['posObsAct']
sizeO = data['sizeO']
NStart = data['NStart']
pObjVec = data['pObjVec']

graphCycleStart = 0

# Extract x and y coordinates for each element
x_positions = trajectory[:, 0, :]
y_positions = trajectory[:, 1, :]
x_posObsIn = posObsIn[0, :]
y_posObsIn = posObsIn[1, :]
x_pObjVec = pObjVec[0]
y_pObjVec = pObjVec[1]


print(x_positions)
vx_positions = velocityHist[:, 0, :]
vy_positions = velocityHist[:, 1, :]
time_steps = np.arange(0, ciclos-graphCycleStart, 1)

plt.figure(figsize=(3.8*1.5, 4.8*1.5))
# plotting the points 
# trajectory
plt.xlim(-1.9, 1.9)  # Set the x-axis limits (from 0 to 6)
plt.ylim(-2.4, 2.4)  # Set the y-axis limits (from 0 to 6)

factor_m = 0.0003528 # m por punto de scatter
diam_agente = 0.0375 #diametro promedio agentes

num_agents = x_positions.shape[1]  # Get the number of agents
labels = [f'Agente {i + 1}' for i in range(NStart,num_agents)] 

print(x_positions[:,NStart:])

plt.plot(x_positions[graphCycleStart:,NStart:], y_positions[graphCycleStart:,NStart:], linestyle='--', zorder=4, label=labels)
plt.scatter(x_positions[graphCycleStart,NStart:], y_positions[graphCycleStart,NStart:], marker='o', facecolor='none', edgecolor='red', label='Pos Iniciales', zorder=5, s = diam_agente/factor_m)
plt.scatter(x_positions[-1,NStart:], y_positions[-1,NStart:], marker='o', color='green', label='Pos Finales', zorder=4, s = diam_agente/factor_m)
plt.scatter(x_posObsIn, y_posObsIn, marker='o', color='purple', label='Obstáculos', zorder=3, s = sizeO/factor_m) # s para convertir a m
plt.scatter(x_pObjVec, y_pObjVec, marker='*', color='yellow', label='Objetivo', zorder=2, s = 0.1/factor_m) 

# naming the x axis
plt.xlabel('Eje x (m)')
# naming the y axis
plt.ylabel('Eje y (m)')
  
# giving a title to my graph
plt.title('Trayectorias')

legend = plt.legend(markerscale=0.5)
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((0.99, 1))
plt.grid()
plt.figure()

# velocityHist in x
plt.plot(time_steps,vx_positions[graphCycleStart:,NStart:], label = labels)
plt.ylim([-20, 20])
# naming the x axis
plt.xlabel('t (ciclos)')
# naming the y axis
plt.ylabel('Vx (m/s)')
  
# giving a title to my graph
plt.title('Velocidades en X')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((0.99, 1))

plt.grid()

plt.figure()

# velocityHist in y
plt.plot(time_steps,vy_positions[graphCycleStart:,NStart:], label = labels)
plt.ylim([-20, 20])
# naming the x axis
plt.xlabel('t (ciclos)')
# naming the y axis
plt.ylabel('Vy (m/s)')
  
# giving a title to my graph
plt.title('Velocidades en Y')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((0.99, 1))

plt.grid()



r = 0.0205
l = 0.0355
a = 0.0355
# function to show the plot
plt.show()





