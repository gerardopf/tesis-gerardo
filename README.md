# Prueba de optimización con NumPy

Se están reemplazando ciclos for en el loop principal por operaciones de matrices con NumPy.

- NumPy es más eficiente computacionalmente y ahorramos tiempo dentro del loop.

- NumPy está implementado en C

# Cambios realizados

- Se eliminó el ciclo for para aplicar los desfases de los markers y se reemplazó por una suma matricial de NumPy (sin probar)

- Dentro del loop principal, se sustituyeron 'if' por 'elif' que son excluyentes como las condiciones si son en físico o no, y las condiciones de 'cambio' para las etapas del algoritmo (sin probar)

- Se modificaron los 'print' con 'f"...{}"' formato de cadena (sin probar)

# Ideas para probar


