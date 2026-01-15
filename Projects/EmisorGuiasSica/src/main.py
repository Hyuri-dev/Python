import ttkbootstrap as ttk
import controllers.guias.controllers_guias as controllers_guias

conexion = controllers_guias.conexion



# Frontend del app
root = ttk.Window(themename ="cosmo")
root.title("Emisor Guias SICA")
root.geometry("320x550")
root.iconbitmap(r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\assets\images\python-logo.png")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(4, weight=1)

scrollbar = ttk.Scrollbar(root)
scrollbar.grid(row=1, column=2, sticky="ns")

lbl = ttk.Label(root, text= "Emisor de Guías SICA", anchor="center", font = ("Arial", 20, "bold"))
lbl.grid(row = 0 , column = 0, columnspan = 2 , sticky = "we" , pady = 5)

#Datos de la factura
frame_datos = ttk.Labelframe(root, text="Datos de la factura", padding=20)
frame_datos.grid(row=1, column=0, columnspan=2, sticky="we", padx=10)

label_factura = ttk.Label(frame_datos, text="Factura:")
label_factura.pack(pady=5, fill = "x")

entry_factura = ttk.Entry(frame_datos)
entry_factura.pack(pady=5, fill="x")

label_codigo_Sunagro = ttk.Label(frame_datos, text="Código Sunagro:")
label_codigo_Sunagro.pack(pady=5, fill = "x")

entry_codigo_Sunagro = ttk.Entry(frame_datos)
entry_codigo_Sunagro.pack(pady=5, fill="x")

#Datos del conductor
frame_datos_conductor = ttk.Labelframe(root, text = "Datos del conductor", padding = 20)
frame_datos_conductor.grid(row = 2 , column = 0 , columnspan = 2 , sticky = "we", padx = 10)

label_conductor = ttk.Label(frame_datos_conductor, text="Chofer:")
label_conductor.pack(pady=5, fill = "x")

menu_conductor = ttk.Combobox(frame_datos_conductor, state="readonly")
menu_conductor.pack(pady=5, fill = "x")

label_camion = ttk.Label(frame_datos_conductor, text="Camión:")
label_camion.pack(pady=5, fill = "x")

menu_camion = ttk.Combobox(frame_datos_conductor, state="readonly")
menu_camion.pack(pady=5, fill = "x")

controllers_guias.llenar_combobox_chofer(conexion , menu_conductor)
controllers_guias.llenar_combobox_vehiculo(conexion, menu_camion)


#Boton de generar guia
btn_generar = ttk.Button(root, text="Generar")
btn_generar.grid(row=3, column=0, pady=10, padx=5, sticky="e")

#Boton de limpiar
btn_limpiar = ttk.Button(root, text="Limpiar")
btn_limpiar.grid(row=3, column=1, pady=10, padx=5, sticky="w")

#Boton listado de los datos
btn_datos = ttk.Button(root,text="Datos", command=controllers_guias.data_window)
btn_datos.grid(row=4 , column=0, columnspan= 2, pady=10, padx=5, sticky="we")



root.mainloop()