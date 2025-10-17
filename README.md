# AutoVision-Deteccion-Para-Automoviles
Sistema de procesamiento digital de imágenes con OpenCV para detección de carretera, basado en operadores punto, regionales y transformaciones de color

# Detección y Realce de Líneas de Carretera con Python y OpenCV

Este proyecto implementa un conjunto de **operadores punto y regionales** para el **procesamiento digital de imágenes**, con el objetivo de **mejorar un video y resaltar las líneas de la carretera**, como parte de una simulación de sistemas de **visión para conducción autónoma**.

# Objetivo del proyecto

El propósito principal de este trabajo es apoyar la detección visual de las líneas que delimitan la carretera en un video mediante técnicas de procesamiento de imágenes, estas técnicas permiten aclarar, ecualizar y suavizar las regiones relevantes de cada fotograma, reduciendo el ruido y aumentando el contraste, con el fin de facilitar la detección de las líneas que guían el vehículo.

# Descripción general del programa

El programa lee un video cuadro por cuadro, aplica una serie de transformaciones secuenciales sobre cada imagen, y genera un nuevo video procesado con las líneas de la carretera resaltadas, para ello, se utilizan diferentes operadores punto y regionales, implementados manualmente y no con funciones automáticas de OpenCV, con el fin de demostrar el conocimiento y aplicación de los fundamentos de procesamiento digital.


# Funcionalidades principales

1. Operadores punto
Estos operadores modifican la intensidad de los píxeles de manera independiente:
- Ecualización de histograma: mejora el contraste global del video al ecualizar el canal de luminancia (V) en el espacio HSV.  
- Corrección gamma personalizada: ajusta la saturación y brillo mediante una función no lineal para destacar mejor las marcas blancas y amarillas de la carretera.

2. Operadores regionales
Estos operadores consideran una vecindad de píxeles:
- Suavizado con kernel personalizado: reduce el ruido y suaviza bordes mediante una máscara ponderada definida manualmente.
- Binarización de imagen: convierte la imagen procesada en blanco y negro para resaltar las zonas de alto contraste, correspondientes a las líneas del pavimento.

3. Máscara y recorte de región de interés (ROI)
Se aplica una máscara rectangular sobre la parte inferior del video, de modo que el procesamiento se concentre únicamente en el área de la carretera, ignorando elementos irrelevantes del entorno (cielo, autos, edificios, etc.).

4. Pipeline de procesamiento
1. Lectura del video con OpenCV.  
2. Aplicación de ecualización, gamma y suavizado.  
3. Enmascaramiento de la región de interés.  
4. Conversión a escala de grises y binarización.  
5. Recorte del área procesada.  
6. Visualización y almacenamiento del resultado en un nuevo video.

Tecnologías utilizadas

- Python
- OpenCV — para captura, filtrado y escritura de video.
- NumPy — para operaciones matriciales y creación de kernels personalizados.
- Matplotlib — para visualización y análisis de resultados.
- tqdm — para mostrar una barra de progreso durante el procesamiento.

Para correr el archivo o el programa se debe hacer a través de la terminal en este caso proporcionando el camino al archivo de video usando el parámetro --video_path. 

Por lo que primero debe poner el python, después incluir la ruta donde esta el archivo .py y seguidamente -v para el llamado del video y después va la ruta del video, para que así pueda también entrar el video y comenzar el progreso, en este caso quedaría la forma quedaría algo así.

PS C:\Users\> python “Ruta del archivo .py” -v “Ruta del video”

Por ejemplo:

PS C:\Users\m> python "C:\Users\m\Documents\Proceso.py" -v "C:\Users\m\Documents\Procesamiento lineas.mp4"

Nota: Para que sea mas eficiente ambos archivos deben estar en una misma carpeta. 
