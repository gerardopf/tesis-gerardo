# Prueba de optimización con NumPy

Se están reemplazando ciclos for en el loop principal por operaciones de matrices con NumPy.

- NumPy es más eficiente computacionalmente y ahorramos tiempo dentro del loop.

- NumPy está implementado en C

# Cambios realizados

- Se eliminó el ciclo for para aplicar los desfases de los markers y se reemplazó por una suma matricial de NumPy (probado, se tuvo que cambiar el signo a resta de desfases porque lo coloqué mal anteriormente)

- Dentro del loop principal, se sustituyeron 'if' por 'elif' que son excluyentes como las condiciones si son en físico o no, y las condiciones de 'cambio' para las etapas del algoritmo (probado)

- Se modificaron los 'print' con 'f"...{}"' formato de cadena (probado)

- En el cálculo de formation_mse se colocó la variable formation_matriz en lugar de volver a calcular la matriz de formación (probado)

# Ideas para probar

- Para el calculo de la distancia entre agentes, no utilizar ciclos for anidados. Mejor utilizar operaicones matriciales con NumPy
