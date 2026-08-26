import pandas as pd
import ttkbootstrap as ttk

# Este script funciona para poder extraer el valor total a pagar de un impuesto especifico
ruta = r"C:\programacion\Python\hello_python\data_analisis\reportes\archivos\LibrodeVentasI.V.A.Bs.TXT"

df = pd.read_csv(ruta, sep="\t", encoding="latin1", decimal=",", thousands=".") 
# Creamos el df con el archivo que se quiere leer basandonos en ciertas especificaciones como el tipo de decimal , miles y el codificado


filtro_col_total = float(df["Total Incluyendo I.V.A(16%)"].sum())

calculo_declaracion = round(round((filtro_col_total / 780), 2) * 0.01, 2)

print(filtro_col_total)
print(f"El monto en bolivares es de: {calculo_declaracion}$")

root = ttk.Window(themename="cosmo")
root.geometry("200x100")

msj = ttk.Label(root, text="Cantidad recaudada a declarar")
msj.pack()

monto_declarar = ttk.Label(root, text= str(calculo_declaracion))
monto_declarar.pack()

root.mainloop()





# filtro_col_total.sum()

# print(filtro_col_total)