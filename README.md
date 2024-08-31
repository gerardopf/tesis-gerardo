<h2> ESTADO DEL PROGRAMA</h2>

<ul>
    <li>El algoritmo ya funciona correctamente</li>
    <ul>
        <li>Se realiza la etapa 0, 1, 2 y 3 </li>
    </ul>
</ul>
    
El algoritmo ya funciona correctamente
    Se realiza la etapa 0, 1, 2 y 3 
    Los agentes siguen a la formación y al líder
    La formación si llega al objetivo 
    La formación si evade obstáculos y a los agentes
    
<h2>Vitácora de cambios</h2> 
Verificar si el agente ya está en la posición inicial
  Se cambió la distancia de 0.05 a 0.07
  Se volvió a colocar en 0.05 
        
Medidas de la arena, medidas del robotat:
  Y: 4.81 m, se puso 4.8
  X: 3.81 m, se puso 3.8
  Se ajustó el tamaño de la cuadrícula
        
        Se cambió el signo de velocidad (se eliminó el negativo -1)
        V[0][g] = 1*(E0)*TIME_STEP/1000 
        V[1][g] = 1*(E1)*TIME_STEP/1000 
        
    Se cambió el signo del peso en las velocidades de ETAPA 3 en el loop principal
    
    Se cambió la distancia para el objetivo cumplido
        de 0.5m a 0.2m
        
    Se agregó el guardado de datos en archivo .npz al terminar la corrida 
    
    La corrida en físico ya se detiene al llegar al objetivo y cumplir con un error de formación
    
    Se agrego un if fisico == 1 elif fisico == 0
        En donde se realizó los cambios de signo con el fin de que funciona la simulación de nuevo
        Probado en simulación y físico
        
Cambios sin probar:
            
    
    
********* Deficiencias *********

Se mueven muy despacio

La distancia entre el líder y la formación podría reducirse

Hay que verificar la distancia para evasión de obstáculos
  Los agentes si se evaden entre sí
  Los agentes parece que si evaden los obstáculos a una distancia buena
        
Cuando estamos en ETAPA 3:
  El líder se detiene mucho para esperar a la formación
  La formación siempre está en constante movimiento y a veces se mantienen girando
        
Cuando el líder llega al objetivo, los agentes YA paran
  A veces se queda un agente prendido
        
El error de formación para detener la corrida 
  Probar un valor más grande
        
Falta agregar la generación de gráficas
    
********* Problemas *********
