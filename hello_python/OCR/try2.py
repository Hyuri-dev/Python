import cv2
import pytesseract as tsr
from matplotlib import pyplot as plt




img_path = r'C:\Users\Jefferson\desarrollo python\hello_python\Python\hello_python\OCR\assets\libro.jpg'

img_read = cv2.imread(img_path)

img_rgb = cv2.cvtColor(img_read, cv2.COLOR_BGR2RGB)

# Preprocesado
gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)



# OCR
text = tsr.image_to_string(img_rgb, lang='eng')
print('Extracted:', text)


# Mostrar la imagen en una ventana. cv2.imshow requiere un nombre de ventana y la matriz
cv2.imshow('Gray', gray)
# Esperar a que el usuario presione una tecla y cerrar ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()