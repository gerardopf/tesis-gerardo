""" optimization v1 SUPERVISOR """

# librerías
from controller import Robot, Supervisor
import numpy as np
import random
import math
import pickle
import keyboard
import time
from funVel import Fmatrix
import funciones
from multiprocessing import shared_memory, Lock
from funciones_conjunto import *

print("inicio de configuracion...")
# memoria compartida para intercambio de datos entre supervisor y agente
shm1 = shared_memory.SharedMemory(name="my_shared_memory1", create=True, size=1024)
shm2 = shared_memory.SharedMemory(name="my_shared_memory2", create=True, size=4096)

# lock para permitir lectura y escritura de uno a la vez
lock = Lock()
TIME_STEP = 64 # paso de simulación 64 ms
supervisor = Supervisor() # instancia de supervisor

# archivo para simular una corrida en físico
initial_conditions_file = 'run1.npz' 
r_initial_conditions = 1 # 0: nueva simulación | 1: simular escenario físico

# archivo para guardar una nueva corrida en físico
new_run_file = 'run3.npz'

""" modo real o simulación """
fisico = 0               # 0 Webots | 1 Robotat
r_obs = 0                # 0: obstáculos virtuales | 1: obstáculos reales (markers)
r_obj = 0                # 0: objetivo virtual | 1: objetivo real (marker)
r_webots_visual = 0      # 0: NO ver objetivo y obstáculos en tiempo real | 1: ver objetivo y obstáculos en tiempo real
MAX_SPEED = 30           # velocidad máxima de ruedas (rpm)

""" matriz de formación """
form_shape = 1    # 1: triángulo | 2: hexágono alargado
rigidity_level = 8 # valores entre 1 y 8 (1 es el menos rígido)

""" Desfases de markers """
# desfases de markers en quaterniones: 1*,2,3,4,5,6,7,8,9*,10,11,12,13,14,15,16,17,18,19,20,21,22
# *los larkers no estaban disponibles, se utilizó el desfase encontrado por José Alejandro R.
desfases_file = 'nueva_calibracion_markers_1_al_22.npy' 
desfases = np.load(desfases_file) 
desfases_euler = quat2eul(desfases,'zyx')
print("archivo desfases euler: \n", desfases_euler)

""" Agentes """
agents_marker_list = [2,6,7]
NMax = 10  # número máximo de agentes que la formación puede tener
NStart = 1 # primer agente
N = len(agents_marker_list)	# último agente

""" obstáculos y objetivo """
obj_marker_list = [20]
obj_marker = obj_marker_list[0]        # marker del objetivo 

obs_marker_list = [11,12,13]
quantOMax = 3 # máximo de obstáculos
obs_active = 1        # 0: SIN obstáculos | 1: CON obstáculos
obs_start_marker = 1 # marker del primer obstáculo

# optitrack marcadores 
robotat_markers = agents_marker_list + obj_marker_list + obs_marker_list
robotat_markers_len = len(robotat_markers)
print("todos los markers: ", robotat_markers)
print("agentes: ", agents_marker_list)
print("objetivo: ", obj_marker_list)
print("obstáculos: ", obs_marker_list)

print("NStart: ", NStart)
print("N: ", N)

""" radar """
r = 0.07	# radio para evitar colisiones (cm)
R = 4	# rango del radar de detección de agentes (m)

""" posiciones iniciales """
initial_pos_setup = 1 # posiciones iniciales | 0: ALEATORIO | 1: PLANIFICADO
setup_shape = 0         # 0: posición inicial LÍNEA | 1: posición inicial CÍRCULO
setup_shape_space = 1.5 # espacio a cubrir con las posiciones iniciales (m)

setup_starting_point = np.array([-1.0, -1.5]) # punto inicial para las posiciones iniciales

agent_setup = 5 # configuración de agentes

formation_edge = 0.3 # separación entre agentes en metros (arista del grafo de formación)

""" obtener configuraciones de la corrida en físico """
if (r_initial_conditions == 1):
    initial_data = np.load(initial_conditions_file)
    real_begin_alg_time = initial_data['begin_alg_time']
    r_obs = initial_data['r_obs']
    r_obj = initial_data['r_obj']
    form_shape = initial_data['form_shape']
    rigidity_level = initial_data['rigidity_level']
    NMax = initial_data['NMax']
    N = initial_data['N']
    NStart = initial_data['NStart']
    r = initial_data['r']
    R = initial_data['R']
    obs_active = initial_data['obs_active']
    obj_marker = initial_data['obj_marker']
    obs_start_marker = initial_data['obs_start_marker']
    robotat_markers = -1
    setup_shape = initial_data['setup_shape']
    setup_shape_space = initial_data['setup_shape_space']
    setup_starting_point = initial_data['setup_starting_point']
    agent_setup = initial_data['agent_setup']
    initial_pos_setup = initial_data['initial_pos_setup']
    
""" parámetros pololu FÍSICO """
r_f = 0.017
l_f = 0.0485
a_f = 0.0485

""" parámetros epuck SIMULACIÓN """
if (fisico == 0):
    MAX_SPEED = 6.28 # rad/s
    r_f = 0.0205
    l_f = 0.0355
    a_f = 0.0355
    
    
""" algunas variables y banderas """
setup_pos = np.zeros((NMax, 6)) # guarda la pose de cada agente (x, y, z, eulx, euly, eulz)
NStart = NStart - 1
total_agent_number = N-NStart # número de agentes
total_agent_weight = (total_agent_number)/NMax # peso de la formación
begin_alg_time = -1 # valor arbitrario para inicializar la variable
obs_start_marker = obs_start_marker - 1 
obj_marker = obj_marker - 1

# no utilizar markers en SIMULACIÓN
if (r_obj == 0):
    obj_marker = -1
if (r_obs == 0):
    obs_start_marker = -1
    
trajectory = []
velocityHist = []
normVHist = []
objHist = []
obsHist = []
formation_mseHist = []
rotHist = []
PosRealAgents = 0
RotRealAgents = 0 
form_cycle = -1
obj_cycle = -1
obj_success_cycle = -1
obj_success = 0
agents_pose = []
obj_cont = 0
ciclo = 0 
 
""" configuración de marcas de posiciones iniciales """
if (r_initial_conditions == 0):
    # línea
    if (setup_shape == 0):
        for i in range(NStart, N):
            setup_pos[i, 0] = setup_starting_point[0] + i * 0.3 # x-coordenada
            setup_pos[i, 1] = setup_starting_point[1] # y-coordenada
            setup_pos[i, 2] = 0.5 # z-coordenada
    # círculo
    elif (setup_shape == 1):
        for i in range(NStart, N):
            angle = 2 * np.pi * i / (total_agent_number) # ángulo para cada marcador
            setup_shape_radius = setup_shape_space/2 # radio del círculo 
            setup_pos[i, 0] = setup_starting_point[0] + setup_shape_radius * np.cos(angle) # x-coordenada
            setup_pos[i, 1] = setup_starting_point[1] + setup_shape_radius * np.sin(angle) # y-coordenada
            setup_pos[i, 2] = 0.5 # z-coordenada

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
    
""" obtener poses y aplicar desfases ROBOTAT"""
if (fisico == 1):
    try:
        robotat = robotat_connect()
    except:
        print("CONFIGURACIÓN: Error al conectar con el robotat")
    agents_pose = update_data(robotat,robotat_markers)
    #print("poses marcadores: \n", agents_pose)
    # aplicar desfases
    index = 0
    for marker in robotat_markers:
        agents_pose[index, 3] = agents_pose[index, 3] - desfases_euler[marker-1, 3]
        index = index + 1
        print("desfase marker ", marker, ": ", desfases_euler[marker-1, 3])
    print("pose con desfases ", agents_pose)

""" Arena """
arena = supervisor.getFromDef("Arena")
size = arena.getField("floorSize")
sizeVec = size.getSFVec2f() # vector con el tamaño de la arena

""" obstáculos """
cantO = len(obs_marker_list)  # cantidad de obstáculos a usar
Obstaculos = [] # obstacle obj list
posObs = []     # obstacle positions list
posObsAct = np.empty([2,cantO])
sizeObsIn = np.empty([2,cantO])

# inicialización de obstáculos
for i in range(0, cantO):
    obstacle_name = f"Obs{i}"
    obstacle = supervisor.getFromDef(obstacle_name)
    pos_obstacle = obstacle.getField("translation")
    Obstaculos.append(obstacle)
    posObs.append(pos_obstacle)
    posObsAct[0][i] = posObs[i].getSFVec3f()[0]
    posObsAct[1][i] = posObs[i].getSFVec3f()[1]

# distancia mínima preferida entre agente y obstáculo (m)   
safety_distance = 0.04 

# tamaño del obstáculo
sizeO = 1*Obstaculos[0].getField("majorRadius").getSFFloat()+1*Obstaculos[0].getField("minorRadius").getSFFloat()+ safety_distance

""" objetivo """
objetivo = supervisor.getFromDef("OBJ")
pObj = objetivo.getField("translation")
pObjVec = pObj.getSFVec3f()

""" inicializar agentes, obstáculos y objetivos """
Agents = []           # list of agent objects
PosTodos = []         # list of agent object positions
RotTodos = []         # list of agent object rotation

PosTodosVec = []      # list of agent positions (vector itself)
RotTodosVec = []      # list of agent rotations (vector itself)

initialPositions = [] # list of initial positions object
posIniPos = []        # list of initial positions object positions
posIniPosVec = []     # list of initial positions positions (vector itself)

# agentes y marcas de posiciones iniciales 
for i in range(0, NMax):
    inipos_name = f"IniPos{i+1}"
    inipos = supervisor.getFromDef(inipos_name)
    inipos_pos = inipos.getField("translation")
    inipos_pos_vec = inipos_pos.getSFVec3f()
    initialPositions.append(inipos)
    posIniPos.append(inipos_pos)
    posIniPosVec.append(inipos_pos_vec)
    agent_name = f"Agent{i+1}"
    agent = supervisor.getFromDef(agent_name)
    agent_pos = agent.getField("translation")
    agent_rot = agent.getField("rotation")
    pos_todos_vec = agent_pos.getSFVec3f()
    rot_todos_vec = agent_rot.getSFVec3f()
    Agents.append(agent)
    PosTodos.append(agent_pos)
    RotTodos.append(agent_rot)
    PosTodosVec.append(pos_todos_vec)
    RotTodosVec.append(rot_todos_vec)
    
# asignar posiciones aleatorias a los AGENTES
X = np.empty([2,N])
for a in range(0, NMax):
    if a in range(NStart,N):
        X[0,a] = random.uniform(sizeVec[1]/2-0.5,-sizeVec[1]/2+0.5) # 0.4 m para que el agente no esté sobre el muro
        X[1,a] = random.uniform(sizeVec[0]/2-0.5,-sizeVec[0]/2+0.5)
print("Posiciones aleatorias X: \n",X)
    
# revisión de posiciones aleatorias  
cW1 = 2 # contador (agente sobre agente)
while(cW1 > 1 or cW2 > 1):
    cW1 = 0
    cW2 = 0
    # verificar intersección entre agentes
    contR = 1 # contador de intersección
    while(contR > 0):
        contR = 0
        for i in range(NStart+1, N):
            for j in range(NStart+1, N-i):
                resta = math.sqrt((X[0,i]-X[0,i+j])**2+(X[1,i]-X[1,i+j])**2)	# diferencia entre posiciones
                if(abs(resta) < r):
                    X[0,i+j] = random.uniform(sizeVec[1]/2-0.4,-sizeVec[1]/2+0.4)
                    X[1,i+j] = random.uniform(sizeVec[0]/2-0.4,-sizeVec[0]/2+0.4) # intersección detectada
                    contR = contR+1
        cW1 = cW1+1
    # verrificar intersección con obstáculos
    contRO = 1 # contador intersección con obstáculo
    while(contRO > 0):
        contRO = 0
        for i in range(NStart,N):
            for j in range(1,cantO):
                # distancia entre agente y obstáculo acle
                resta = math.sqrt((X[0,i]-posObs[j].getSFVec3f()[1])**2 + (X[1,i]-posObs[j].getSFVec3f()[0])**2)	
                # cambio a nueva posición
                if(abs(resta) < sizeO):
                    X[0,i+j] = random.uniform(sizeVec[1]/2-0.4,-sizeVec[1]/2+0.4)
                    X[1,i+j] = random.uniform(sizeVec[0]/2-0.4,-sizeVec[0]/2+0.4)
                    contRO = contRO + 1 # intersección detectada
        cW2 = cW2 + 1        
Xi = X
print("Posiciones aleatorias modificadas Xi: \n", Xi)


# inicializar OBSTÁCULOS fuera del mapa si no están activos
for i in range(0, quantOMax):
    if (obs_active == 0):
        posObs[i].setSFVec3f([-sizeVec[0], i*0.9, -6.39203e-05])

# obtener posición de OBSTÁCULOS virtuales
if (r_obs == 0):
    for obs in range(0,cantO):
        posObsAct[0][obs] = posObs[obs].getSFVec3f()[0]
        posObsAct[1][obs] = posObs[obs].getSFVec3f()[1]

# obtener posiciones de obstáculos y objetivos reales del ROBOTAT
try:
    if (fisico == 1):
        if (r_obs == 1):
            for obs in range(0,cantO):
                x_obs = agents_pose[len(agents_pose)-cantO+obs, 0]
                y_obs = agents_pose[len(agents_pose)-cantO+obs, 1]
                posObsAct[0][obs] = x_obs
                posObsAct[1][obs] = y_obs
                posObs[obs].setSFVec3f([x_obs, y_obs, -6.39203e-05])
        if (r_obj == 1):
            pObjVec[0] = agents_pose[len(agents_pose)-cantO-1,0]
            pObjVec[1] = agents_pose[len(agents_pose)-cantO-1,1]
except:
    print("error")

# inicializar agentes y marcas de posiciones iniciales SIN USAR fuera del escenario
for b in range(0, NMax):
    if (b<NStart or b>=N):
        PosTodos[b].setSFVec3f([-sizeVec[0]+1, b*0.3, 0.3])
        posIniPos[b].setSFVec3f([-sizeVec[0]+1, b*0.3, -6.39203e-05])

# cargar posiciones iniciales para configurar el escenario (basados en archivo de condiciones iniciales)
if (r_initial_conditions == 1):
    PosRealAgents = initial_data['PosRealAgents']
    RotRealAgents = initial_data['RotRealAgents']
    PosRealIniPosVec = initial_data['posIniPosVec']
    posObsAct = initial_data['posObsAct']
    pObjVec = initial_data['pObjVec']
    obj_data = initial_data['obj_data']
    obs_data = initial_data['obs_data']

# inicializar obstáculos y objetivo (basados en archivo de condiciones iniciales)
if (r_initial_conditions == 1):
    for i in range(0, cantO):
        posObs[i].setSFVec3f([posObsAct[0,i], posObsAct[1,i], -6.39203e-05])
    pObj.setSFVec3f([pObjVec[0], pObjVec[1], 0.3])
    
# configurar marcas de posición inicial
for b in range(NStart, N):
    if (agent_setup == 1): # posición de agentes aleatoria
        PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])
        
    elif (agent_setup == 2): # marcas de inicio aleatorias
        posIniPos[b].setSFVec3f([X[1,b], X[0,b], 0.3])
        posIniPosVec[b] = posIniPos[b].getSFVec3f() 
                    
    elif (agent_setup == 3): # posición basada en configuración guardada
        with open('D:/AlejandroDigital/tesisAlejandro/codigo/comunicacion_pololu/first_setup.pickle','rb') as f:
            setup_pos = pickle.load(f)
        PosTodos[b].setSFVec3f([setup_pos[b,0], setup_pos[b,1], -6.39203e-05])
        
    elif (agent_setup == 4): # custom agent positioning (obsolete version of 5) 
        posIniPos[b].setSFVec3f([setup_pos[b,0],setup_pos[b,1], setup_pos[b,2]])
        posIniPosVec[b] = posIniPos[b].getSFVec3f()
        if (fisico == 0):  
            PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])
        elif (fisico == 1):#probarfisico 
            PosTodos[b].setSFVec3f([agents_pose[b,0], agents_pose[b,1], -6.39203e-05])
            RotTodos[b].setSFRotation([0, 0, 1, agents_pose[b,3]])
            PosTodosVec[b] = [agents_pose[b,0], agents_pose[b,1], -6.39203e-05]
            RotTodosVec[b] = [0, 0, 1, agents_pose[b,3]]
            
    elif (agent_setup == 5): # posicionamiento personalizado
        if (initial_pos_setup == 0):   # marcas de posición aleatorias
            posIniPos[b].setSFVec3f([X[1,b], X[0,b], 0.3])
        elif (initial_pos_setup == 1): # marcas de posición planificadas (línea o círculo)
            posIniPos[b].setSFVec3f([setup_pos[b,0],setup_pos[b,1], setup_pos[b,2]])
        
        # simulación  
        if (fisico == 0):
            if (r_initial_conditions == 0):  # marcas de posición aleatorias
                PosTodos[b].setSFVec3f([X[1,b], X[0,b], -6.39203e-05])
                if (initial_pos_setup == 1): # marcas de posición planificadas (línea o círculo)
                    PosTodos[b].setSFVec3f([setup_pos[b,0],setup_pos[b,1], -6.39203e-05])
                
            if (r_initial_conditions == 1): # replicar condiciones iniciales de la corrida en físico 
                PosTodos[b].setSFVec3f([PosRealAgents[b,0], PosRealAgents[b,1], -6.39203e-05])
                RotTodos[b].setSFRotation([0, 0, 1, RotRealAgents[b,3]])
                posIniPos[b].setSFVec3f([PosRealIniPosVec[b,0], PosRealIniPosVec[b,1], 0.3])    
        # físico
        if (fisico == 1):  #try elif later
            PosTodos[b].setSFVec3f([agents_pose[b,0], agents_pose[b,1], -6.39203e-05])
            RotTodos[b].setSFRotation([0, 0, 1, agents_pose[b,3]])
            PosTodosVec[b] = [agents_pose[b,0], agents_pose[b,1], -6.39203e-05]
            RotTodosVec[b] = [0, 0, 1, agents_pose[b,3]]
                     
        posIniPosVec[b] = posIniPos[b].getSFVec3f()
        print("marcas de posiciones iniciales: \n", posIniPosVec)
 
""" variables actuales """
posActuales = np.zeros([2,N]) # posición de agentes
rotActuales = np.zeros([1,N]) # rotación de agentes
V = np.zeros([2,N]) # velocidad de agentes

""" matriz de formación """
formation_matrix = Fmatrix(form_shape,rigidity_level)
print("Matriz de formación: \n", formation_matrix)
print("Fin de configuracion...")

""" -------------- ETAPAS DEL ALGORITMO DE FORMACIÓN --------------

La variable "cambio" representa la etapa del algoritmo

Etapa 0: 
- Configuración de escenario
- Previo al algoritmo de formación
- Los agentes se mueven a la posición inicial del experimento
- Se espera hasta que todos los agentes lleguen a la posición inicial

Etapa 1:
- Los agentes de acercan entre sí hasta que las velocidades están por debajo de 0.5 m/s

Etapa 2:
- Los agentes se mueven a la formación designada.
- Para verificar la formación, se revisa que el error cuadrático promedio entre la formación actual y la formación deseada esté por debajo de 0.5
- Se inicializa la etapa 3

Etapa 3:
- El líder se mueve hacia el objetivo y los agentes de la formación lo siguen dejando que la formación lo alcance

 ------------------------------------------------------------------- """

""" -------------- MAIN LOOP --------------"""
# al cargar las condiciones iniciales, se salta la primera etapa ya que los robots
# ya aparecen en la posición de las marcas iniciales
cambio = 0
if (r_initial_conditions == 1):
    cambio = 1
    begin_alg_time = 0

print("Inicia ciclo principal...")
while supervisor.step(TIME_STEP) != 1:
    # SIMULACIÓN
    if (fisico == 0):
        # posición de objetivo y obstáculos VIRTUALES
        for obs in range(0, cantO):
            posObsAct[0][obs] = posObs[obs].getSFVec3f()[0]
            posObsAct[1][obs] = posObs[obs].getSFVec3f()[1]
        pObjVec = pObj.getSFVec3f()
        
    # FÍSICO
    if (fisico == 1):
        # pedir pose actual de markers
        try:
            agents_pose = update_data(robotat,robotat_markers)
            #print("poses marcadores: \n", agents_pose)
            # aplicar desfases
            index = 0
            for marker in robotat_markers:
                agents_pose[index, 3] = agents_pose[index, 3] - desfases_euler[marker-1, 3]
                index = index + 1
                #print("desfase marker ", marker, ": ", desfases_euler[marker-1, 3])
            #print("pose con desfases ", agents_pose)
        except:
            print("MAIN LOOP ERROR: Error al obtener poses de agentes, se usa pose anterior")
            agents_pose = agents_pose_old # usar posición anterior
        agents_pose_old = agents_pose
        
        # obtener posición actual de obstáculos REALES
        if (r_obs == 1):
            for obs in range(0,cantO):
                x_obs = agents_pose[len(agents_pose)-cantO+obs, 0]
                y_obs = agents_pose[len(agents_pose)-cantO+obs, 1]
                posObsAct[0][obs] = x_obs
                posObsAct[1][obs] = y_obs
                # actualizar webots en tiempo real
                if (r_webots_visual == 1):
                    posObs[obs].setSFVec3f([x_obs, y_obs, -6.39203e-05])
        # obtener posición actual de obstáculos VIRTUALES
        if (r_obs == 0):
            for obs in range(0,cantO):
                posObsAct[0][obs] = posObs[obs].getSFVec3f()[0]
                posObsAct[1][obs] = posObs[obs].getSFVec3f()[1]
        # obtener posición actual de objetivo REAL
        if (r_obj == 1):
            pObjVec[0] = agents_pose[len(agents_pose)-cantO-1,0]
            pObjVec[1] = agents_pose[len(agents_pose)-cantO-1,1]
            # actualizar webots en tiempo real
            if (r_webots_visual == 1):
                pObj.setSFVec3f([pObjVec[0], pObjVec[1], -6.39203e-05])
        # obtener posición actual de objetivo VIRTUAL
        if (r_obj == 0):
            pObjVec = pObj.getSFVec3f() 
        
    # actualizar la pose de los agentes
    for c in range(NStart, N):
        # SIMULACIÓN
        if (fisico == 0):
            posC = Agents[c].getField("translation")
            rotC = Agents[c].getField("rotation")
            posActuales[0][c] = posC.getSFVec3f()[0]    # x-coord
            posActuales[1][c] = posC.getSFVec3f()[1]    # y-coord
            rotActuales[0][c] = rotC.getSFVec3f()[3]*180/math.pi    # rotacion
        elif (fisico == 1):
            posActuales[0][c] = agents_pose[c][0]   # x-coord
            posActuales[1][c] = agents_pose[c][1]   # y-coord
            rotActuales[0][c] = agents_pose[c][3]+90    # rotacion compensada con 90 grados
        
        if (rotActuales[0][c] < 0):
            rotActuales[0][c] = rotActuales[0][c] + 360 # angulos siempre positivos
    
    # ----------- algoritmo de sincronización y control de formaciones -----------
    
    for g in range(NStart, N):
        E0 = 0
        E1 = 0
        for h in range(NStart, N):
            dist = np.asarray([posActuales[0][g]-posActuales[0][h], posActuales[1][g]-posActuales[1][h]]) # vector xi - xj   
            mdist = math.sqrt(dist[0]**2 + dist[1]**2)	 # norma euclidiana vector xi - xj
            dij = formation_edge*formation_matrix[g][h]	 # distancia deseada entre agentes i y j

            # agregar peso a la ecuación de consenso
            if(mdist == 0 or mdist >= R):
                w = 0
            else:
                if(cambio == 1 or cambio == 0):
                    w = 0.05*(mdist - (2*(r+0.05)))/(mdist - (r+0.05))**2 
                elif (cambio == 2 or cambio == 3):
                    if(dij == 0):	 # si la arista es igual a 0
                        w = 0.15*math.sinh(15*mdist-6)/mdist 		
                    else:
                        w = (4*(mdist - dij)*(mdist - r) - 2*(mdist - dij)**2)/(mdist*(mdist - r)**2)
            # aplicar el peso
            E0 = E0 + 5*w*dist[0]
            E1 = E1 + 5*w*dist[1]
            
        # evasión de colisiones con obstáculos
        for j in range(0,cantO):
            distO0 = posActuales[0,g] - posObsAct[0][j]
            distO1 = posActuales[1,g] - posObsAct[1][j]  
            mdistO = math.sqrt(distO0**2 + distO1**2) - sizeO
            if(abs(mdistO) < 0.0001):
                mdistO = 0.0001
            w = -1/(mdistO**2) # peso
            E0 = E0 + 0.6*w*distO0
            E1 = E1 + 0.6*w*distO1  
            
        # actualizar velocidades
        if (fisico == 1):
            V[0][g] = 1*(E0)*TIME_STEP/1000 
            V[1][g] = 1*(E1)*TIME_STEP/1000 
        elif (fisico == 0):
            V[0][g] = -1*(E0)*TIME_STEP/1000 
            V[1][g] = -1*(E1)*TIME_STEP/1000 
            
    
    # al acercarse a la posición deseada se cambia el control
    normV2 = 0
    # calcular norma de velocidad de agentes
    for m in range(NStart,N):
        nV2 = V[0][m]**2 + V[1][m]**2
        normV2 = normV2 + nV2
    normV = math.sqrt(normV2)
    print("normV: ", normV, " \n")
    
    # calcular matriz de adyacencia de la formación actual
    actual_adjacency = (1/formation_edge)*funciones.DistBetweenAgents(posActuales,NStart,N) 

    # calcular en error entre la formación actual y la deseada
    formation_mse = funciones.FormationError(actual_adjacency, Fmatrix(form_shape,rigidity_level),NStart,N)

    # ETAPA 2 -----> FORMACIÓN
    if(normV < 0.5 and cambio == 1):
        form_cycle = ciclo
        cambio = 2
        
    # ETAPA 3 -----> SEGUIR OBJETIVO
    elif(formation_mse < 0.5 and cambio == 2):
        obj_cycle = ciclo
        cambio = 3   
        
    # ETAPA 0 -----> COLOCARSE EN POSICIONES INICIALES
    if (cambio == 0):
        ready_ini_pos = 0
        cont_N = 0
        for obj in range(NStart,N):
            cont_N = cont_N + 1
            k_vel = 5
            dx = posActuales[0][obj]-posIniPosVec[obj][0]
            dy = posActuales[1][obj]-posIniPosVec[obj][1]
            if (fisico == 1):
                V[0][obj] = V[0][obj] + k_vel*dx
                V[1][obj] = V[1][obj] + k_vel*dy
            elif (fisico == 0):
                V[0][obj] = V[0][obj] - k_vel*dx
                V[1][obj] = V[1][obj] - k_vel*dy
               
            #print("\nagente: ", obj)
            #print("posx: ", posActuales[0][obj])
            #print("posx ini: ", posIniPosVec[obj][0])
            #print("dx: ", dx)
            #print("posy: ", posActuales[1][obj])
            #print("posy ini: ", posIniPosVec[obj][1])
            #print("dy: ", dy)
            # verificar si el agente ya está en la posición inicial
            if ((posActuales[0][obj]-posIniPosVec[obj][0])<0.05 and (posActuales[1][obj]-posIniPosVec[obj][1])<0.05):
                ready_ini_pos = ready_ini_pos + 1
        if (ready_ini_pos == cont_N):
            # cuando todos los agentes están en la posición inicial, comienza ETAPA 1
            begin_alg_time = ciclo
            cambio = 1
            if (fisico == 1):
                for b in range(NStart, N):
                    PosTodosVec[b] = [agents_pose[b,0], agents_pose[b,1], -6.39203e-05]
                    RotTodosVec[b] = [0, 0, 1, agents_pose[b,3]]
                PosRealAgents = np.array(PosTodosVec)
                RotRealAgents = np.array(RotTodosVec)  
        print("número de agentes: ", cont_N)
        print("No. agentes en marcas iniciales: ", ready_ini_pos)
        
    # ETAPA 3 -----> SEGUIMIENTO DEL OBJETIVO
    if (cambio == 3):
        # si el líder está a más de X metros del objetivo, espera a la formación
        if (abs(posActuales[0][NStart]-pObjVec[0]) > 0.7 or abs(posActuales[1][NStart]-pObjVec[1]) > 0.7):     
            if (fisico == 1):
                V[0][NStart] = V[0][NStart] + total_agent_weight*(1/(formation_mse))*(posActuales[0][NStart]-pObjVec[0])
                V[1][NStart] = V[1][NStart] + total_agent_weight*(1/(formation_mse))*(posActuales[1][NStart]-pObjVec[1])
            elif (fisico == 0):          
                V[0][NStart] = V[0][NStart] - total_agent_weight*(1/(formation_mse))*(posActuales[0][NStart]-pObjVec[0])
                V[1][NStart] = V[1][NStart] - total_agent_weight*(1/(formation_mse))*(posActuales[1][NStart]-pObjVec[1])
        # si el líder está a menos de X metros del objetivo, la constante es mayor y puede llamar a la formación más rápido
        elif (abs(posActuales[0][NStart]-pObjVec[0]) <= 0.7 or abs(posActuales[1][NStart]-pObjVec[1]) <= 0.7):
            if (fisico == 1):
                V[0][NStart] = V[0][NStart] + 10*(posActuales[0][NStart]-pObjVec[0])
                V[1][NStart] = V[1][NStart] + 10*(posActuales[1][NStart]-pObjVec[1])
            elif (fisico == 0):
                V[0][NStart] = V[0][NStart] - 10*(posActuales[0][NStart]-pObjVec[0])
                V[1][NStart] = V[1][NStart] - 10*(posActuales[1][NStart]-pObjVec[1])
        # si el líder está a X metros del objetivo, se cumplió la meta
        if (abs(posActuales[0][NStart]-pObjVec[0]) <= 0.2 and abs(posActuales[1][NStart]-pObjVec[1]) <= 0.2):
            obj_success = 1
            if (obj_cont == 0):
                obj_success_cycle = ciclo
            obj_cont = 1
            
    # ENVÍO DE DATOS DEL SUPERVISOR A CADA AGENTE
    lock.acquire()                                          # bloquear canal de comunicación
    pick_V = pickle.dumps(V)                                # guardar velocidades en archivo picke
    shm1.buf[:len(pick_V)] = pick_V                         # enviar velocidades a la memoria compartida
    pick_agents_pose = pickle.dumps(agents_pose)            # guardar poses de agentes en archivo picke
    shm2.buf[:len(pick_agents_pose)] = pick_agents_pose     # enviar poses a la memoria compartida
    lock.release()                                          # liberar canal de comunicación
    
    # guardar historial de la corrida
    trajectory.append(posActuales.copy())
    velocityHist.append(V.copy())
    normVHist.append(normV)
    objHist.append(pObjVec.copy())
    obsHist.append(posObsAct.copy())
    formation_mseHist.append(formation_mse)
    rotHist.append(rotActuales.copy())
    
    print("Ciclo: ", ciclo)
    print("ETAPA: ", cambio) 
    print("Error de formación: ", formation_mse)
    print(" ")
    ciclo = ciclo + 1     
    
    if obj_success == 1:
        print("Objetivo logrado")
    
    # presionar la tecla 'a' para terminar la corrida
    if keyboard.is_pressed('a') or obj_success == 1 and formation_mse < 0.01:
        print("Fin de la corrida -supervisor")
        V = np.zeros([2,N]) # velocidades en 0 de agentes
        
        # enviar datos a la memoria compartida
        lock.acquire()  
        pick_V = pickle.dumps(V)
        shm1.buf[:len(pick_V)] = pick_V
        pick_agents_pose = pickle.dumps(agents_pose)
        shm2.buf[:len(pick_agents_pose)] = pick_agents_pose
        
        # guardar datos relevantes
        trajectory_data = np.array(trajectory)  # trayectoria
        velocity_data = np.array(velocityHist)  # velocidades
        normV_data = np.array(normVHist)    # norma de velocidades 
        obj_data = np.array(objHist)    # posición de objetivos
        obs_data = np.array(obsHist)    # posición de obstáculos
        formation_mse_data = np.array(formation_mseHist)    # error cuadrático para formación
        rot_data = np.array(rotHist)    # rotación de agentes
        NStart = NStart + 1
        obs_start_marker = obs_start_marker + 1 
        obj_marker = obj_marker + 1
        
        # guardar datos en archivo .npz de la nueva corrida en físico
        if (fisico == 1 and r_initial_conditions == 0):
            print("Guardando datos de la corrida...")
            try:
                np.savez(new_run_file, trajectory_data = trajectory_data, # agents positions register of the run
                                           velocity_data = velocity_data, # agents velocities registrr of the run
                                           normV_data = normV_data,       # agents velocities norm register of the run
                                           obj_data = obj_data,           # objetive positions register of the run
                                           obs_data = obs_data,           # objetive positions register of the run 
                                           formation_mse_data = formation_mse_data, # mse register of the run
                                           rot_data = rot_data,           # rotation data register of the run
                                           total_cycle = ciclo,           # total of cycles of the run
                                           form_cycle = form_cycle,       # cycle when formation began its construction
                                           obj_cycle = obj_cycle,         # cycle when the leader began following the objective
                                           quantO = cantO,                # total quantity of obstacles
                                           posObsAct = posObsAct,         # last position of obstacles when the run ended
                                           sizeO = sizeO,                 # size of the obstacles
                                           NStart = NStart,               # first agent (lower limit of the interval of agents)
                                           N = N,                         # last agent (higher limit of the interval of agents)
                                           NMax = NMax,                   # maximum agent number that the formation shape can contain
                                           pObjVec = pObjVec,             # last position of objective when the run ended
                                           PosRealAgents = PosRealAgents, # position of the agents at the start of stage 1 (initial conditions)
                                           RotRealAgents = RotRealAgents, # rotation of the agents at the start of stage 1 (initial conditions)
                                           begin_alg_time = begin_alg_time, # cycle when the algorithm itself started (aka start of stage 1)
                                           posIniPosVec = posIniPosVec, # position of initial position marks
                                           fisico = fisico,               # physical (Robotat) or virtual (Webots) world run
                                           r_initial_conditions = r_initial_conditions, # real initial conditions active or not (fresh run)
                                           r_obs = r_obs,                 # real or virtual obstacles
                                           r_obj = r_obj,                 # real or virtual objective
                                           TIME_STEP = TIME_STEP,         # time step of the program
                                           agent_setup = agent_setup,     # agent setup used for the run
                                           obs_active = obs_active,       # obstacles active or not
                                           initial_pos_setup = initial_pos_setup, # initial position setup (random or not)
                                           r = r,                         # radio to consider to avoid collisions
                                           R = R,                         # Radar radio
                                           MAX_SPEED = MAX_SPEED,         # allowed maximum speed of agents wheels
                                           form_shape = form_shape,       # shape of the formation    
                                           rigidity_level = rigidity_level, # rigidity level of the formation 
                                           total_agent_number = total_agent_number, # total agent number of agents involved in the run
                                           obj_marker = obj_marker,       # Robotat marker used for the objetive in real life
                                           obs_start_marker = obs_start_marker, # Robotat starting marker used for the obstacles in real life
                                           setup_starting_point = setup_starting_point, # beginning of the initial positions shape
                                           setup_shape = setup_shape,     # initial positions shape
                                           setup_shape_space = setup_shape_space, # what space to cover with the initial positions
                                           formation_edge = formation_edge, # how long is the age of the formation
                                           r_f = r_f,                     # robot dimensions for unicycle model
                                           l_f = l_f,
                                           a_f = a_f,
                                           obj_success = obj_success,     # indicates if the objective was successful
                                           obj_success_cycle = obj_success_cycle) # objective success cycle      
            except e:
                print(e)
                print("Error al guardar los datos de la corrida")
    
        # desconectar del Robotat
        if (fisico == 1):
            robotat_disconnect(robotat)
        lock.release()
        break
    