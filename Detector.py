import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm  # Importar la librería de progreso visual

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--video_path", required=True, help="path to video file")
args = vars(parser.parse_args())

capture = cv2.VideoCapture(args["video_path"])

if not capture.isOpened():
    print("Error del inicio del video")
    exit()

# Obtener propiedades del video
fps = int(capture.get(cv2.CAP_PROP_FPS))  # Cuadros por segundo
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # Ancho del frame
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Alto del frame

# Definir códec y crear VideoWriter para guardar el resultado
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec para formato AVI
out = cv2.VideoWriter("Salida.MP4", fourcc, fps, (width, height))

# Leer primer fotograma para definir la máscara
ret, frame = capture.read()

def crear_mascara_rectangular(frame, x1, y1, x2, y2):
    mask = np.zeros_like(frame)  # Máscara negra del mismo tamaño del frame
    cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)  # Dibujar el rectángulo en la máscara
    return mask

# Definir las coordenadas del rectángulo para la máscara
x1, y1 = 310, 420
x2, y2 = 1280, 660
mascara_rectangular = crear_mascara_rectangular(frame, x1, y1, x2, y2)

def recorte(image, x1, y1, x2, y2):
    return image[y1:y2, x1:x2]

#ECUALIZAR
def eq(image):
    # Convertir a HSV y ecualizar el canal V
    H, S, V = cv2.split(cv2.cvtColor(image, cv2.COLOR_RGB2HSV))
    eq_V = cv2.equalizeHist(V)
    image_eq = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2RGB)
    return image_eq    

#SATURACION DEL RESULTADO MEDIANTE FILTRO GAMMA
def sat_gamma(image, gamma=0.9):
    image_RGB_gamma = np.array(255 * (image / 255) ** gamma, dtype='uint8')
    return image_RGB_gamma

#SUAVIZADO PERSONALIZADO DEL RESULTADO
def suav(image):
    kernel = np.array([
        [6, 12, 6],
        [12, 24, 12],
        [6, 12, 6]
    ], dtype=np.float32) * float(1 / 96)
    output = cv2.filter2D(image, -1, kernel)
    return output

#REALIZAR LAS OPERACIONES
def trasf1(frame):
    frame = eq(frame)
    frame = cv2.bitwise_and(frame, mascara_rectangular)
    frame = sat_gamma(frame)
    frame = suav(frame)
    return frame

def trasf2(frame):
    #CONVERTIR A ESCALA DE GRISES EL RESULTADO
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #BINARIZAR PARA CIERTO RANGO AUN SIN DETERMINAR DE BLANCOS Y NEGRO
    ath = 200 
    output = np.where(frame_gray >= ath, 255, 0).astype(np.uint8)
    return output

# Inicializar la barra de progreso
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
progress_bar = tqdm(total=frame_count, desc="Procesando fotogramas", unit="fotograma", dynamic_ncols=True)

# While para leer frame por frame
while capture.isOpened():
    ret, frame = capture.read()
    
    if not ret:
        print("\nVideo finalizado. Cerrando programa automáticamente...")
        break  # Salimos del loop si ya no hay más fotogramas 
        
    cv2.imshow('Original Frame', frame) # Mostrar fotograma original
    frame_t1 = trasf1(frame) # Aplica la trasnformacion 1
    cv2.imshow('Procesado', frame_t1) # Mostrar fotograma procesado
    Eframe = trasf2(frame_t1) # Aplicar el transformacion 2
    Eframe_recortado = recorte(Eframe, x1, y1, x2, y2)  # Recorte rectangular
    cv2.imshow('Resultado Final', Eframe_recortado)  # Mostrar resultado final
    out.write(Eframe_recortado)  # Guardar el procesado en el video de salida
        
        # Guardar resultado en video
    out.write(Eframe_recortado)

    # Detectar tecla presionada
    key = cv2.waitKey(1) & 0xFF
    print(f"\rTecla presionada: {chr(key) if 32 <= key <= 126 else key}  ", end="")  # Sobrescribir línea en terminal

    if key == ord("z"):  # Salir con 'z'
        print("\nTecla 'z' detectada. Saliendo...")
        break

    # Actualizar barra de progreso solo si no se ha detenido
    progress_bar.update(1)

# Cerrar recursos
progress_bar.close()
capture.release()
out.release()
cv2.destroyAllWindows()
print("✅ Programa finalizado correctamente.")