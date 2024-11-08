<img alt="Logo-UVG" height="50" src="https://github.com/user-attachments/assets/ca88dcc9-d874-4fad-83f9-fc9d2200c4e5">

# Optimización de un algoritmo de inteligencia de enjambre enfocado en sincronización y control de formaciones de sistemas robóticos multi-agente para escenarios con obstáculos móviles

![Static Badge](https://img.shields.io/badge/Estado-en%20desarrollo-purple)

Desarrollado en `Webots R2023b` y `Python 3.10.4`.

Resumen...

## Autor

Gerardo Paz Fuentes

Carné: 20173

### Información de contacto

Correo institucional: [paz20173@uvg.edu.gt](mailto:paz20173@uvg.edu.gt)

Correo alternativo: [gerardopaz322@gmail.com](mailto:gerardopaz322@gmail.com)

## Resumen de contenido

| Carpeta    | Contenido                                                                                                                     |
|------------|-------------------------------------------------------------------------------------------------------------------------------|
| documentos | Contiene el contenido el protocolo y la el trabajo escrito de tesis.                                                          |
| prototipo  | Contiene todos los recursos utilzados para realizar el proyecto. Incluye versiones de prueba y finales de códigos y gráficas. |

## Funcionamiento

### Etapas del algoritmo

El algoritmo consiste en las siguientes etapas para su ejecución:

- `Etapa 0`: movilización de los agentes hacia sus posiciones iniciales.
- `Etapa 1`: acercamiento de los agentes.
- `Etapa 2`: colocación de los agentes en su posición en la formación.
- `Etapa 3`: movilización de la formación hacia el objetivo.

### Configuración de escenarios

- Mínimo de agentes: `2`
- Máximo de agentes: `10`
- Mínimo de obstáculos: `0`
- Máximo de obstáculos: `3`
- Objetivos: `1`


## Requisitos para la ejecución del programa
- Webots R2023b
- Python 3.10.4

### Librerías de Python
- Keyboard - versión 0.13.5
- NumPy - versión 1.23.2
- SciPy - versión 1.13.0
