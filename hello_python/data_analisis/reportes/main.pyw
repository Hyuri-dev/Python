import pandas as pd
import ttkbootstrap as ttk
import datetime

# Este script funciona para poder extraer el valor total a pagar de un impuesto especifico
ruta = r"C:\programacion\Python\hello_python\data_analisis\reportes\archivos\LibrodeVentasI.V.A.Bs.TXT"

df = pd.read_csv(ruta, sep="\t", encoding="latin1", decimal=",", thousands=".") 
# Creamos el df con el archivo que se quiere leer basandonos en ciertas especificaciones como el tipo de decimal , miles y el codificado

date_now = datetime.datetime.now()

filtro_col_total = float(df["Total Incluyendo I.V.A(16%)"].sum())

calculo_declaracion = round(round((filtro_col_total / 780), 2) * 0.01, 2)

print(filtro_col_total)
print(f"El monto en bolivares es de: {calculo_declaracion}$ a la fecha de hoy {date_now.strftime("%x")}")




#UI from message

root = ttk.Window(themename="cosmo")
root.geometry("300x100")

title= ttk.Label(root, text=f"Cantidad a declarar hoy", font=("Helvetica" , 16, "bold"))
title.pack()

label_date = ttk.Label(root, text=f"{date_now.strftime("%x")}", font=("Helvetica" , 16, "bold"), foreground="#004385")
label_date.pack()

monto_declarar = ttk.Label(root, text= str(f"{calculo_declaracion}$"), font=("Helvetica" , 20, "bold"))
monto_declarar.pack()

root.mainloop()





# filtro_col_total.sum()

# print(filtro_col_total)