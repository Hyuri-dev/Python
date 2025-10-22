# -*- coding: utf-8 -*-
import cv2
import pytesseract as tsr
from matplotlib import pyplot as plt

# --- CONFIGURACIÓN ---
# Si Tesseract no está en tu PATH, descomenta la siguiente línea y pon la ruta a tu ejecutable.
# tsr.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img_path = r'C:\Users\Jefferson\desarrollo python\hello_python\Python\hello_python\OCR\assets\captcha.png'

# --- 1. CARGA DE LA IMAGEN ---
# Se lee la imagen en formato BGR de OpenCV.
img_original = cv2.imread(img_path)

# Comprobación para asegurar que la imagen se cargó correctamente.
if img_original is None:
    raise FileNotFoundError(f"No se pudo leer la imagen en la ruta: {img_path}")

# --- 2. PRE-PROCESAMIENTO DE LA IMAGEN ---

# Paso 2.1: Convertir a escala de grises.
# Este es el primer paso fundamental para simplificar la imagen.
gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

# Paso 2.2: Umbralización (Binarización).
# ¡Este es el paso más crucial para los CAPTCHAs!
# Convierte la imagen a blanco y negro puros, eliminando la mayoría del ruido de fondo.
# THRESH_BINARY_INV invierte los colores (texto blanco, fondo negro).
# THRESH_OTSU calcula automáticamente el mejor valor de umbral para separar el texto del fondo.
_, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Paso 2.3: Eliminación de ruido (Opcional pero recomendado).
# Aplicamos un filtro de mediana para eliminar el ruido de tipo "sal y pimienta" (puntos pequeños).
# Un kernel de 3x3 es usualmente un buen punto de partida.
denoised_image = cv2.medianBlur(binary_image, 3)


# --- 3. EXTRACCIÓN DE TEXTO CON TESSERACT OCR ---

# Configuración de Tesseract para optimizar la lectura de CAPTCHAs.
# --psm 7: Trata la imagen como una única línea de texto. Es ideal para CAPTCHAs.
#    Otras opciones útiles:
#    --psm 8: Trata la imagen como una única palabra.
#    --psm 6: Asume un bloque uniforme de texto (el predeterminado, malo para CAPTCHAs).
# -c tessedit_char_whitelist=...: Limita los caracteres que Tesseract puede reconocer.
#    Ejemplo si el CAPTCHA solo tiene números: '-c tessedit_char_whitelist=0123456789'
#    Ejemplo si solo tiene letras mayúsculas: '-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
custom_config = r'--psm 7'

# Se pasa la imagen pre-procesada (binaria y sin ruido) a Tesseract.
extracted_text = tsr.image_to_string(denoised_image, config=custom_config)

# Limpieza final del texto extraído (eliminar saltos de línea y espacios extra).
final_text = "".join(extracted_text.split()).strip()


# --- 4. MOSTRAR RESULTADOS ---
print(f"Texto extraído: {final_text}")

# Visualización de los pasos del proceso para depuración.
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title('1. Imagen Original')
plt.imshow(cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title('2. Escala de Grises')
plt.imshow(gray, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title('3. Imagen Binarizada (Umbral)')
plt.imshow(binary_image, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title('4. Imagen Final (Sin Ruido)')
plt.imshow(denoised_image, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()