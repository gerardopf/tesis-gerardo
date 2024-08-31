<h2> ESTADO DEL PROGRAMA</h2>
<ul>
    <li>El algoritmo ya funciona correctamente</li>
    <ul>
        <li>Se realiza la etapa 0, 1, 2 y 3 </li>
        <li>Los agentes siguen a la formación y al líder</li>
        <li>La formación si llega al objetivo</li>
        <li>La formación si evade obstáculos y a los agentes entre sí</li>
        <li>La formación evade obstáculos móviles y si llega al objetivo</li>
    </ul>
</ul>
    
<h2>Bitácora de cambios</h2> 
<ul>
    <li>Verificar si el agente ya está en la posición inicial</li>
    <ul>
        <li>Se cambió la distancia de 0.05 a 0.07 metros</li>
        <li>se volvió a colocar la distancia en 0.05 metros</li>
    </ul>
    <li>Se actualizaron medidas de la arena</li>
    <ul>
        <li>X: 3.81 m, se usó 3.8 m en webots</li>
        <li>Y: 4.81 m, se usó 4.8 m en webots</li>
    </ul>
    <li>Se cambió el signo de velocidad (se eliminó el negativo -1)</li>
    <ul>
        <li>V[0][g] = 1*(E0)*TIME_STEP/1000</li>
        <li>V[1][g] = 1*(E1)*TIME_STEP/1000 </li>
    </ul>
    <li>Se cambió el signo del peso elcálculo de las velocidades para la ETAPA 3 (en el loop principal)</li>
    <li>Se cambió la distancia para el objetivo cumplido</li>
    <ul>
        <li>De 0.5 a 0.2 metros</li>
    </ul>
    <li>Se agregó el guardado de datos en archivo .npz al terminar la corrida</li>
    <li>La corrida en físico ya se detiene al llegar al objetivo y cumplir con un error de formación</li>
    <li>Se agregó un if fisico == 1 elif fisico == 0</li>
    <ul>
        <li>Esto se colocó donde se realizaron los cambios de signo con el fin de que la simulación volviera a funcionar ya que luego de los cambios, únicamente funcionaba la corrida en físico y, los agentes en la simulación, divergían</li>
    </ul>
</ul>

<h3>Cambios sin probar</h3>
N/A           
    
<h2>Deficiencias</h2>
<ul>
    <li>Los agentes se mueven muy despacio</li>
    <li>La distancia entre el líder y la formación podría reducirse</li>
    <li>Hay que verificar la distancia para evasión de obstáculos</li>
    <ul>
        <li>Los agentes si se evaden entre sí</li>
        <li>Los agentes si evaden los obstáculos</li>
    </ul>
    <li>Cuando estamos en la ETAPA 3</li>
    <ul>
        <li>El líder se detiene mucho para esperar a la formación</li>
        <li>La formación siempre está en constante movimiento y a veces se mantienen girando </li>
    </ul>
</ul>

<h2>Cosas que faltan</h2>
<ul>
    <li>Dejar obsoleta la variable: obs_start_marker</li>
</ul>
<h2>Problemas</h2>
<ul>
    <li>Cuando el líder llega al objetivo</li>
    <ul>
        <li>Los agentes paran pero a veces un agente no le llegan las velocidades a cero</li>
    </ul>
    <li>Error de formación para detener la corrida</li>
    <ul>
        <li>Hay que probar algún valor diferente, ahorita es muy pequeño (0.01) y la formación tarda en llegar a ese error </li>
    </ul>
</ul>

<h2>Cosas a limpiar en código</h2>
El agent setup 4 que es una versión obsoleta del 5

