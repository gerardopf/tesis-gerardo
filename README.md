# ESTADO DEL PROGRAMA

El algoritmo funciona correctamente

- Se realiza la etapa 0, 1, 2 y 3

- Los agentes siguen a la formación y al líder

- La formación si llega al objetivo

- La formación puede evadir obstáculos y a los agentes entre sí (incluye obstáculos dinámicos)

- La generación de gráficas está funcionando

# BITÁCORA DE CAMBIOS 
Verificar si el agente ya está en la posición inicial

Se cambió la distancia de 0.05 a 0.07 metros
Se volvió a colocar la distancia en 0.05 metros

Se actualizaron medidas de la arena
X: 3.81 m, se usó 3.8 m en webots
Y: 4.81 m, se usó 4.8 m en webots

Se cambió el signo de velocidad (se eliminó el negativo -1)

V[0][g] = 1*(E0)*TIME_STEP/1000
V[1][g] = 1*(E1)*TIME_STEP/1000 

Se cambió el signo del peso elcálculo de las velocidades para la ETAPA 3 (en el loop principal)

Se cambió la distancia para el objetivo cumplido

De 0.5 a 0.2 metros

Se agregó el guardado de datos en archivo .npz al terminar la corrida

La corrida en físico ya se detiene al llegar al objetivo y cumplir con un error de formación

Se agregó un if fisico == 1 elif fisico == 0, esto se colocó donde se realizaron los cambios de signo con el fin de que la simulación volviera a funcionar ya que luego de los cambios, únicamente funcionaba la corrida en físico y, los agentes en la simulación, divergían



# Cambios sin probar 
Se cambió la condición para detener simulación
- Error de formación en 0.1 (antes 0.01)     
- Probado en simulación

    
# DEFICIENCIAS

Los agentes se mueven muy despacio

La distancia entre el líder y la formación podría reducirse
Hay que verificar la distancia para evasión de obstáculos

Los agentes pierden mucho tiempo en buscar como evadir el obstáculo

Cuando estamos en la ETAPA 3 el líder se detiene mucho para esperar a la formación y la formación siempre está en constante movimiento y a veces se mantienen girando 


# COSAS QUE FALTAN

Dejar obsoleta la variable: obs_start_marker

Probar cambiar la cantidad de obstáculos


# PROBLEMAS

Cuando el líder llega al objetivo los agentes paran pero a veces un agente no le llegan las velocidades a cero


A veces el líder se aleja mucho de la formación


# COSAS A LIMPIAR EN CÓDIGO

El agent setup 4 que es una versión obsoleta del 5

# ---------- Optimización con NumPy ----------

Se están reemplazando ciclos for en el loop principal por operaciones de matrices con NumPy.

- NumPy es más eficiente computacionalmente y ahorramos tiempo dentro del loop.

- NumPy está implementado en C

# Cambios realizados (probados)

1- Se eliminó el ciclo for para aplicar los desfases de los markers y se reemplazó por una suma matricial de NumPy (probado, se tuvo que cambiar el signo a resta de desfases porque lo coloqué mal anteriormente)

2- Dentro del loop principal, se sustituyeron 'if' por 'elif' que son excluyentes como las condiciones si son en físico o no, y las condiciones de 'cambio' para las etapas del algoritmo

3- Se modificaron los 'print' con 'f"...{}"' formato de cadena

4- En el cálculo de formation_mse se colocó la variable formation_matrix en lugar de volver a calcular la matriz de formación

5- Se creó una versión optimizada para la función del cálculo de la distancia entre agentes (DistBetweenAgentsOptimized). Ya no se utilizan ciclos for anidados, se utilizan operaciones con NumPy. 

6- Se eliminó la importación de librería en el archivo FunVel -> from controller import Robot, Motor, Supervisor, Node

7- Se creó una versión optimizada para la función que calcula el error de la formación (FormationErrorOptimized). Utilizar operaciones con NumPy en lugar de ciclos for anidados. 

# Cambios realizados (NO probados)

# Ideas para probar

- En el programa de agente, enviar velocidad a las ruedas solo si es diferente a la velocidad anterior (esto para evitar saturar el envío de datos)

# Observaciones

- Parece que el cambio de las funciones en cuanto a tiempo no es muy significativa al utilizar pocos agentes (2 o 3), pero al utilizar más agentes si puede haber ahorro de tiempo computacional más grande (hay que probarlo con corridas reales ya que solo se tiene el tiempo en pruebas de algoritmos)


