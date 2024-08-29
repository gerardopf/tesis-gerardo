# Autor: José Alejandro Rodríguez Porras
# Generación de gráficas de las corridas del algoritmo, de los datos guardados en el archivo .npz, de la corrida
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from prettytable import PrettyTable
import os
import re

#trajectory = np.load('robot_trajec.npy')
#trajectory = np.load('trial.npy')
#trajectory = np.load('setup_traj0_formacion_2.npy')

archivo = 'finaltrial_6A_AAA_v_1.npz'
show_images = 0

data = np.load(archivo)
# Extracting the filename without extension from 'archivo'
filename_without_extension = archivo.split('.')[0]
# Define the folder name
main_folder = 'finaltrials'
folder_name = f'{filename_without_extension}'
# Create the main folder if it doesn't exist
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

# Define the trial folder name
trial_folder = os.path.join(main_folder, folder_name)

# Create the trial folder inside the main folder
if not os.path.exists(trial_folder):
    os.makedirs(trial_folder)


pattern = r'A_([^_]+)_'
pattern_number = r'_([^_]+)$'

match = re.search(pattern, archivo)
if match:
    extracted_value = match.group(1)
    print(extracted_value)

match_number = re.search(pattern_number, filename_without_extension)
if match_number:
    extracted_number = match_number.group(1)
    print(extracted_number)

with open(f'finaltrials/{filename_without_extension}/latex.txt', 'w') as file:
    pass

def print_latex_figure(filename, caption, label, width):
    latex_code = f"""
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename}}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
"""

    # Open a text file in append mode ('a')
    with open(f'finaltrials/{filename_without_extension}/latex.txt', 'a') as file:
        # Use the print function to append new content to the file
        print(latex_code, file = file)
    print(latex_code)

    


def print_latex_figure_two(filename1,filename2, caption, label, width):
    latex_code = f"""
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename1}}}
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename2}}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
"""
    # Open a text file in append mode ('a')
    with open(f'finaltrials/{filename_without_extension}/latex.txt', 'a') as file:
        # Use the print function to append new content to the file
        print(latex_code, file = file)
    print(latex_code)

#print(data)

#to find out the files within the .npz
"""
data = np.load('trial.npz', allow_pickle=True)
print(data.files)
"""
fisico = data['fisico']
r_f = data['r_f']
l_f = data['l_f']
a_f = data['a_f']
trajectory_data = data['trajectory_data']
rot_data = data['rot_data']
velocity_data = data['velocity_data']
normV_data = data['normV_data']
formation_mse_data = data['formation_mse_data']
obj_data = data['obj_data']
obs_data = data['obs_data']
total_cycle = data['total_cycle']
form_cycle = data['form_cycle']
obj_cycle = data['obj_cycle']
quantO = data['quantO']
posObsAct = data['posObsAct']
sizeO = data['sizeO']
NStart = data['NStart']
N = data['N']
pObjVec = data['pObjVec']
begin_alg_time = data['begin_alg_time']
fisico = data['fisico']
r_initial_conditions = data['r_initial_conditions']
r_obs = data['r_obs']
r_obj = data['r_obj']
TIME_STEP = data['TIME_STEP']
agent_setup = data['agent_setup']
obs_active = data['obs_active']
initial_pos_setup = data['initial_pos_setup']
r = data['r']
R = data['R']
MAX_SPEED = data['MAX_SPEED']
form_shape = data['form_shape']
rigidity_level = data['rigidity_level']
total_agent_number = data['total_agent_number']
NMax = data['NMax']
obj_marker = data['obj_marker']
obs_start_marker = data['obs_start_marker']
setup_starting_point = data['setup_starting_point']
formation_edge = data['formation_edge']
#obj_success = data['obj_success']
#obj_success_cycle = data['obj_success_cycle']
graphCycleStart = begin_alg_time
graphCycleEnd = total_cycle
show_real_cycle = 0
show_in_seconds = 1
snapframes = 1
#print(obj_success_cycle)
# Extract x and y coordinates for each element
x_positions = trajectory_data[:, 0, :]
y_positions = trajectory_data[:, 1, :]
x_positions_obs = obs_data[:, 0, :]
y_positions_obs = obs_data[:, 1, :]
x_positions_obj = obj_data[:, 0]
y_positions_obj = obj_data[:, 1]
x_posObsAct = posObsAct[0, :]
y_posObsAct = posObsAct[1, :]
x_pObjVec = pObjVec[0]
y_pObjVec = pObjVec[1]

if (fisico == 1):
    real_time_compensation = 1.5
    TIME_STEP = TIME_STEP*real_time_compensation

if (show_in_seconds==1):
    escala_temp = 't (s)'
else:
    escala_temp = 't (ciclos)'
#print(x_positions)

if (fisico == 0):
    virtualtext = f'corrida {extracted_number}, en simulación'

elif (fisico == 1):
    virtualtext = f'corrida {extracted_number}, en físico'


if (fisico == 0):
    combined_fv = 0
    texto_fisico = 'simulación'

elif (fisico == 1):
    combined_fv = 1
    if (combined_fv == 1):
        pattern_f = re.compile(r'(_[hf]_)')
        # Use re.sub to replace the matched pattern with '_v_'
        filename_without_extension_v = archivo.split('.')[0]
        formatted_file = re.sub(pattern_f, '_v_', filename_without_extension_v)
    texto_fisico = 'físico'


vx_positions = velocity_data[:, 0, :]
vy_positions = velocity_data[:, 1, :]
time_steps = np.arange(graphCycleStart, graphCycleEnd, 1)
if (fisico == 1 and show_real_cycle == 0):
    time_steps = time_steps-begin_alg_time
    form_cycle = form_cycle-begin_alg_time
    obj_cycle = obj_cycle-begin_alg_time

if (fisico == 0):
    form_cycle = form_cycle+1

if (show_in_seconds == 1):
    time_steps = time_steps*TIME_STEP/1000
    form_cycle = form_cycle*TIME_STEP/1000
    obj_cycle = obj_cycle*TIME_STEP/1000
#print(time_steps)
plt.figure(figsize=(3.8*1.5, 4.8*1.5))
# plotting the points 
# trajectory
plt.xlim(-1.9, 1.9)  # Set the x-axis limits (from 0 to 6)
plt.ylim(-2.4, 2.4)  # Set the y-axis limits (from 0 to 6)

factor_m = 0.0003528 # m por punto de scatter
diam_agente = l_f #diametro promedio agentes

num_agents = x_positions.shape[1]  # Get the number of agents
print(vx_positions.shape[1])
print(graphCycleStart)
print(NStart)
print(N)
NStart = NStart - 1
agent_number = N-NStart
labels = [f'Agente {i + 1}' for i in range(NStart,num_agents)] 
#labels = [f'Agente {i}' for i in range(NStart,N+1)] 
#NStart_calc = NStart-1
#print(x_positions[:,NStart:N])

plt.plot(x_positions[graphCycleStart:graphCycleEnd,NStart:N], y_positions[graphCycleStart:graphCycleEnd,NStart:N], linestyle='--', zorder=4, label=labels)
plt.scatter(x_positions[graphCycleStart,NStart:N], y_positions[graphCycleStart,NStart:N], marker='o', facecolor='none', edgecolor='red', label='Pos Iniciales', zorder=2, s = diam_agente/factor_m)
plt.scatter(x_positions[-1,NStart:N], y_positions[-1,NStart:N], marker='o', color='green', label='Pos Finales', zorder=4, s = diam_agente/factor_m)
plt.scatter(x_posObsAct, y_posObsAct, marker='o', color='purple', label='Obstáculos', zorder=3, s = sizeO/factor_m) # s para convertir a m
plt.scatter(x_pObjVec, y_pObjVec, marker='*', color='yellow', label='Objetivo', zorder=2, s = 0.1/factor_m) 


# naming the x axis
plt.xlabel('Eje x (m)')
# naming the y axis
plt.ylabel('Eje y (m)')
  
# giving a title to my graph
plt.title(f'Trayectoria de agentes en {texto_fisico}')

legend = plt.legend(markerscale=0.5)
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.31, 1))
plt.grid()
# Your plot commands here
plt.savefig(f'finaltrials/{filename_without_extension}/traj_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/traj_{filename_without_extension}.png', format='png', bbox_inches='tight')
# Example usage

print_latex_figure(f'traj_{filename_without_extension}.eps', f'Trayectoria de los {agent_number} agentes en el escenario '+f'{extracted_value}, '+ f'{virtualtext}.', f'traj_{filename_without_extension}', "0.8")
    
plt.figure(figsize=(3.8*1.5, 4.8*1.5))
# plotting the points 
# trajectory
plt.xlim(-1.9, 1.9)  # Set the x-axis limits (from 0 to 6)
plt.ylim(-2.4, 2.4)  # Set the y-axis limits (from 0 to 6)

# Scatter plot for the center of mass at every index
plt.plot(np.mean(x_positions[graphCycleStart:graphCycleEnd, NStart:], axis=1), np.mean(y_positions[graphCycleStart:graphCycleEnd, NStart:], axis=1), linestyle='--', color='black', label='C.M. Form', zorder=5)

# Scatter plot for obstacles, objective, initial positions, and final positions
plt.scatter(x_posObsAct, y_posObsAct, marker='o', color='purple', label='Obstáculos', zorder=3, s=sizeO/factor_m)  # s para convertir a m
plt.scatter(x_pObjVec, y_pObjVec, marker='*', color='yellow', label='Objetivo', zorder=2, s=0.1/factor_m)
plt.scatter(x_positions[graphCycleStart,NStart:N], y_positions[graphCycleStart,NStart:N], marker='o', facecolor='none', edgecolor='red', label='Pos Iniciales', zorder=2, s = diam_agente/factor_m)
plt.scatter(x_positions[-1, NStart:N], y_positions[-1, NStart:N], marker='o', color='green', label='Pos Finales', zorder=4, s=diam_agente/factor_m)
# naming the x axis
plt.xlabel('Eje x (m)')

# naming the y axis
plt.ylabel('Eje y (m)')

# giving a title to the graph
plt.title(f'Trayectoria del centro de masa de la formación en {texto_fisico}')

# Add legend with smaller fonts
legend = plt.legend(markerscale=0.5)
for text in legend.get_texts():
    text.set_fontsize(7)

# Add grid
plt.grid()
legend = plt.legend(markerscale=0.5)
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.31, 1))

coordinate_success = graphCycleStart

for coordinate in x_positions[graphCycleStart:graphCycleEnd]:
    #print(x_positions[coordinate_success, NStart])
    if (abs(np.mean(x_positions[coordinate_success, NStart:])-x_pObjVec)<0.5 and abs(np.mean(y_positions[coordinate_success, NStart:])-y_pObjVec)<0.5):
        print((coordinate_success-graphCycleStart)*TIME_STEP/1000)
        #print("******************************************************************************")
        break
    
    coordinate_success = coordinate_success+1


# Save the plot
plt.savefig(f'finaltrials/{filename_without_extension}/cm_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/cm_{filename_without_extension}.png', format='png', bbox_inches='tight')

print_latex_figure(f'cm_{filename_without_extension}.eps', "Trayectoria del centro de masa de la formación en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'cm_{filename_without_extension}', "0.8")
if (combined_fv == 1):
    print_latex_figure_two(f'traj_{filename_without_extension}.eps',f'traj_{formatted_file}.eps', f'Trayectoria de los {agent_number} agentes en el escenario '+ f'{extracted_value}, corrida {extracted_number} en físico (izquierda) y simulación (derecha).', f'traj_{filename_without_extension}', "0.49")
    print_latex_figure_two(f'cm_{filename_without_extension}.eps',f'cm_{formatted_file}.eps', f'Trayectoria del centro de masa de la formación en el escenario {extracted_value}, corrida {extracted_number} en físico (izquierda) y simulación (derecha).', f'traj_{filename_without_extension}', "0.49")


plt.figure()
plt.plot(time_steps,normV_data[graphCycleStart:graphCycleEnd])
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
plt.ylim([-40, 40])
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
plt.ylabel('Velocidad (m/s)')
# giving a title to my graph
plt.title('Norma de la velocidad de la formación')
legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.26, 1))
plt.savefig(f'finaltrials/{filename_without_extension}/normV_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/normV_{filename_without_extension}.png', format='png', bbox_inches='tight')

plt.figure()
plt.plot(time_steps,formation_mse_data[graphCycleStart:graphCycleEnd])
plt.axhline(y=1, color='pink', linestyle='--', label='Límite = 1')
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
plt.ylabel('Velocidad (m/s)')
# giving a title to my graph
plt.title('Error Cuadrático Medio de la formación')
legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.26, 1))
plt.savefig(f'finaltrials/{filename_without_extension}/mse_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/mse_{filename_without_extension}.png', format='png', bbox_inches='tight')

print_latex_figure_two(f'normV_{filename_without_extension}.eps',f'mse_{filename_without_extension}.eps', "Histórico de norma de velocidad de la formación y error cuadrático medio en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'normVmse_{filename_without_extension}', "0.49")

if (combined_fv == 1):
    print_latex_figure_two(f'normV_{formatted_file}.eps',f'mse_{formatted_file}.eps', f'Histórico de norma de velocidad de la formación y error cuadrático medio en el escenario {extracted_value}, corrida {extracted_number}, en simulación.', f'normVmse_{formatted_file}', "0.49")


plt.figure()

# velocityHist in x
plt.plot(time_steps,np.sqrt(vx_positions[graphCycleStart:graphCycleEnd,NStart:N]**2+vy_positions[graphCycleStart:graphCycleEnd,NStart:N]**2), label = labels)
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
plt.ylim([-20, 20])
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
plt.ylabel('V (m/s)')
  
# giving a title to my graph
plt.title('Velocidades')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.26, 1))

plt.grid()
# Your plot commands here
plt.savefig(f'finaltrials/{filename_without_extension}/vel_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/vel_{filename_without_extension}.png', format='png', bbox_inches='tight')


plt.figure()

# velocityHist in x
plt.plot(time_steps,vx_positions[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
plt.ylim([-20, 20])
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
plt.ylabel('Vx (m/s)')
  
# giving a title to my graph
plt.title('Velocidades en X')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.26, 1))

plt.grid()
# Your plot commands here
plt.savefig(f'finaltrials/{filename_without_extension}/xvel_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/xvel_{filename_without_extension}.png', format='png', bbox_inches='tight')

plt.figure()

# velocityHist in y
plt.plot(time_steps,vy_positions[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
plt.ylim([-20, 20])
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
plt.ylabel('Vy (m/s)')
  
# giving a title to my graph
plt.title('Velocidades en Y')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.26, 1))

plt.grid()
plt.savefig(f'finaltrials/{filename_without_extension}/yvel_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/yvel_{filename_without_extension}.png', format='png', bbox_inches='tight')

print_latex_figure_two(f'xvel_{filename_without_extension}.eps',f'yvel_{filename_without_extension}.eps', "Histórico de velocidades de los agentes en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'vel_{filename_without_extension}', "0.49")

if (combined_fv == 1):
    print_latex_figure_two(f'xvel_{formatted_file}.eps',f'yvel_{formatted_file}.eps', "Histórico de velocidades de los agentes en el escenario "+f'{extracted_value}, '+ f'corrida {extracted_number}, en simulación.', f'vel_{formatted_file}', "0.49")

plt.figure()

phi = np.zeros([2,N])
phi_data = []
#print(rot_data)

for cyc in range(0, total_cycle):
    #print((rot_data[cyc][0][1]))
    
    if (fisico == 0):
        r_f = 0.0205
        l_f = 0.0355
        a_f = 0.0355
    elif (fisico == 1):   
        r_f = 0.017
        l_f = 0.0485
        a_f = 0.0485
    for argc in range(NStart,num_agents):
        v = (velocity_data[cyc][0][argc])*(math.cos(rot_data[cyc][0][argc]*math.pi/180)) + (velocity_data[cyc][1][argc])*(math.sin(rot_data[cyc][0][argc]*math.pi/180))
        w = (velocity_data[cyc][0][argc])*(-math.sin(rot_data[cyc][0][argc]*math.pi/180)/a_f) + (velocity_data[cyc][1][argc])*(math.cos(rot_data[cyc][0][argc]*math.pi/180)/a_f)
        
        # Cálculo de velocidades de las ruedas   
        phi_r = (v+(w*l_f))/r_f
        # print(phi_r)
        phi_l = (v-(w*l_f))/r_f
        # print(phi_l)
        
        # Truncar velocidades a la velocidad maxima
        if(phi_r > 0):
            if(phi_r > MAX_SPEED):
                phi_r = MAX_SPEED
        else:
            if(phi_r < -MAX_SPEED):
                phi_r = -MAX_SPEED
                
        if(phi_l > 0):
            if(phi_l > MAX_SPEED):
                phi_l = MAX_SPEED
        else:
            if(phi_l < -MAX_SPEED):
                phi_l = -MAX_SPEED
        
        if (fisico == 0):
            phi_r = phi_r*60/(2*math.pi)
            phi_l = phi_l*60/(2*math.pi)
        phi[0][argc] = phi_r
        phi[1][argc] = phi_l
        phi_data.append(phi.copy())
phi_data_array = np.array(phi_data)

phi_r_data = phi_data_array[:, 0, :]
#print(phi_r_data)
phi_l_data = phi_data_array[:, 1, :]

plt.plot(time_steps,phi_r_data[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
plt.ylim([-70, 70])
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
plt.ylabel('Phi R (rpm)')
  
# giving a title to my graph
plt.title('Velocidades R')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((0.99, 1))
plt.savefig(f'finaltrials/{filename_without_extension}/phiR_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/phiR_{filename_without_extension}.png', format='png', bbox_inches='tight')

plt.figure()
plt.plot(time_steps,phi_l_data[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle}')
plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle}')
plt.ylim([-70, 70])
# naming the x axis
plt.xlabel(f'{escala_temp}')
# naming the y axis
 
# giving a title to my graph
plt.title('Velocidades L')

legend = plt.legend()
for text in legend.get_texts():
    text.set_fontsize(7)

plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((0.99, 1))
plt.savefig(f'finaltrials/{filename_without_extension}/phiL_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
plt.savefig(f'finaltrials/{filename_without_extension}/phiL_{filename_without_extension}.png', format='png', bbox_inches='tight')

print_latex_figure_two(f'phiL_{filename_without_extension}.eps',f'phiR_{filename_without_extension}.eps', "Histórico de velocidades en las ruedas de los agentes en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'phi_{filename_without_extension}', "0.49")

if (combined_fv == 1):
    print_latex_figure_two(f'phiL_{formatted_file}.eps',f'phiR_{formatted_file}.eps', "Histórico de velocidades en las ruedas de los agentes en el escenario "+f'{extracted_value}, '+ f'corrida {extracted_number}, en simulación.', f'phi_{formatted_file}', "0.49")


# function to show the plot
if (show_images == 1):
    plt.show()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(3.8*1.5, 4.8*1.5))
ax.set_xlim(-1.9, 1.9)
ax.set_ylim(-2.4, 2.4)

# Initialize the scatter plots for the agents, obstacles, and goal
scatter_agents = ax.scatter([], [], marker='o', color ='green', label='Agentes', zorder=5, s = diam_agente/factor_m)
scatter_goal = ax.scatter([], [], marker='*', color='yellow', label='Objetivo', zorder=2, s = 0.1/factor_m)
scatter_obstacles = ax.scatter([], [], marker='o', color='purple', label='Obstáculos', zorder=3, s = sizeO/factor_m)

real_time_text = ax.text(1.03, 0.8, '', transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))


"""
total_frames = len(np.arange(graphCycleStart, graphCycleEnd, 8))

snapshot_frame_1 = begin_alg_time
snapshot_frame_2 = total_frames // 3
snapshot_frame_3 = 2 * (total_frames // 3)
snapshot_frame_4 = total_frames - 1
"""

# Plot the initial positions
scatter_agents.set_offsets(np.column_stack([x_positions[graphCycleStart:graphCycleEnd, NStart:N], y_positions[graphCycleStart:graphCycleEnd, NStart:N]]))
scatter_goal.set_offsets(np.column_stack([x_positions_obj[graphCycleStart:graphCycleEnd], y_positions_obj[graphCycleStart:graphCycleEnd]]))
scatter_obstacles.set_offsets(np.column_stack([x_positions_obs[graphCycleStart:graphCycleEnd], y_positions_obs[graphCycleStart:graphCycleEnd]]))

# Function to update the scatter plots in each animation frame
def update(frame):
    scatter_agents.set_offsets(np.column_stack([x_positions[frame, NStart:N], y_positions[frame, NStart:N]]))
    scatter_goal.set_offsets(np.column_stack([x_positions_obj[frame], y_positions_obj[frame]]))
    scatter_obstacles.set_offsets(np.column_stack([x_positions_obs[frame], y_positions_obs[frame]]))
    # Update the real-time timer in the title
        # Save equally spaced snapshots
    """    
    if (snapframes == 1):
        if frame == snapshot_frame_1:
            plt.savefig(f'finaltrials/{filename_without_extension}/snap1_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
            plt.savefig(f'finaltrials/{filename_without_extension}/snap1_{filename_without_extension}.png', format='png', bbox_inches='tight')
        elif frame == snapshot_frame_2:
            plt.savefig(f'finaltrials/{filename_without_extension}/snap2_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
            plt.savefig(f'finaltrials/{filename_without_extension}/snap2_{filename_without_extension}.png', format='png', bbox_inches='tight')
        elif frame == snapshot_frame_3:
            plt.savefig(f'finaltrials/{filename_without_extension}/snap3_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
            plt.savefig(f'finaltrials/{filename_without_extension}/snap3_{filename_without_extension}.png', format='png', bbox_inches='tight')
        elif frame == snapshot_frame_4:
            plt.savefig(f'finaltrials/{filename_without_extension}/snap4_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
            plt.savefig(f'finaltrials/{filename_without_extension}/snap4_{filename_without_extension}.png', format='png', bbox_inches='tight')
    """
    real_time_seconds = frame
    if (fisico == 1 and show_real_cycle == 0):
        real_time_seconds = frame - begin_alg_time
    if (show_in_seconds == 1):
        real_time_seconds = real_time_seconds * TIME_STEP/1000
        #plt.title(f'Trayectorias - Tiempo Real: {real_time_seconds:.2f} segundos')
        real_time_text.set_text(f'Tiempo Real: \n{real_time_seconds:.2f} s')
    else:
        real_time_seconds = frame
        #plt.title(f'Trayectorias - Tiempo Real: {real_time_seconds} ciclos')
        real_time_text.set_text(f'Tiempo Real: \n{real_time_seconds} ciclos')


# Create the animation
animation = FuncAnimation(fig, update, frames=np.arange(graphCycleStart, graphCycleEnd, 8), interval = 50, blit=False)

# Display the plot
plt.xlabel('Eje x (m)')
plt.ylabel('Eje y (m)')
plt.title('Trayectorias')
legend = plt.legend(markerscale=0.5)
for text in legend.get_texts():
    text.set_fontsize(7)

# Generating the output GIF filename based on the input filename
output_gif_filename = f'finaltrials/{filename_without_extension}/animation_{filename_without_extension}.gif'
# Saving the animation with the dynamically generated filename
animation.save(output_gif_filename, writer='Pillow')
plt.subplots_adjust(right=0.8)
legend.set_bbox_to_anchor((1.3, 1))
plt.grid()
if (show_images == 1):
    plt.show()


