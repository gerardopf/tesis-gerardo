# Prueba de optimización con NumPy

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


