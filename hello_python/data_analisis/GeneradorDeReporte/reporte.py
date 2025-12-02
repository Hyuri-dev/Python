import csv
import os

# Nombre del archivo a generar
nombre_archivo = "Productosvendidos_PRUEBA.TXT"

# Datos simulados (Incluyendo los casos que tu script busca)
# Formato: Codigo, Descripcion, Cantidad, Pendiente, MontoBruto, ...
datos = [
    # Encabezados (Tal cual los espera tu script con names=...)
    ["Código", "Descripción", "Cantidad", "Pendiente", "Monto Bruto", "Descuentos", "I.V.A", "Costo", "Utilidad", "%Util", "Existencia"],
    
    # --- PASTA ALLEGRI ---
    ["001001", "PASTA ALLEGRI LARGA 1KG", "500,00", "0", "25.000,00", "0", "0", "20.000,00", "5.000,00", "20", "1000"],
    ["001002", "PASTA ALLEGRI CORTA PLUMAS", "200,00", "0", "10.000,00", "0", "0", "8.000,00", "2.000,00", "20", "500"],
    
    # --- PASTA HORIZONTE ---
    ["004001", "PASTA HORIZONTE LARGA 1KG", "1.200,00", "0", "48.000,00", "0", "0", "40.000,00", "8.000,00", "16", "200"],
    
    # --- PASTICHO ---
    ["001008", "PASTICHO ALLEGRI 250GR", "50,00", "0", "5.000,00", "0", "0", "4.000,00", "1.000,00", "20", "100"],
    ["003001", "PASTICHO MI CASA RAPIDO", "30,00", "0", "3.500,00", "0", "0", "3.000,00", "500,00", "15", "80"],
    
    # --- HARINAS ---
    ["002001", "HARINA DE TRIGO DULCE MAR", "100,00", "0", "4.500,00", "0", "0", "3.500,00", "1.000,00", "22", "150"],
    ["010005", "HARINA JUANA CLASICA", "600,00", "0", "18.000,00", "0", "0", "15.000,00", "3.000,00", "16", "400"],
    ["010015", "HARINA TRIGO ROBIN HOOD", "150,00", "0", "7.500,00", "0", "0", "6.000,00", "1.500,00", "20", "90"],
    
    # --- OTROS MONACA ---
    ["010002", "AVENA LASSIE HOJUELAS", "80,00", "0", "6.400,00", "0", "0", "5.000,00", "1.400,00", "21", "70"],
    ["010006", "ARROZ MONICA TIPO I", "300,00", "0", "12.000,00", "0", "0", "10.000,00", "2.000,00", "16", "600"],
    
    # --- ADOBO (Prueba por Código) ---
    ["010003", "ADOBO LA COMADRE COMP", "45,00", "0", "2.250,00", "0", "0", "1.800,00", "450,00", "20", "50"],
    
    # --- DEVOLUCIONES ---
    ["009001", "?SERRVICIOS O ITEM SIN EXISTENCIA", "-5,00", "0", "-500,00", "0", "0", "-400,00", "-100,00", "0", "0"],
    
    # --- PRODUCTO DE RELLENO (NO DEBE SALIR EN EL FILTRO) ---
]

# Escribir el archivo usando TAB como separador y codificación latin-1
try:
    with open(nombre_archivo, 'w', newline='', encoding='latin-1') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(datos)
    print(f"✅ Archivo '{nombre_archivo}' generado exitosamente.")
    print("Ahora cambia la ruta en tu script principal para apuntar a este archivo.")
except Exception as e:
    print(f"❌ Error al generar el archivo: {e}")