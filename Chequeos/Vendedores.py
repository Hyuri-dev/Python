import tkinter as tk

vendedores = [ 
  "julio", "Victor","jefferson","mario", "luis"
]

primer_vendedor = vendedores.index[0]
# vendedores.append(input("Ingrese un nuevo vendedor"))

# print(vendedores)

main = tk.Tk()
listado_vendedores = tk.Label(main, text= vendedores)
listado_vendedores.pack()
main.mainloop()