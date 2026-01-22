import ttkbootstrap as ttk

class VistaListado(ttk.Frame):
    def __init__(self, master,columnas,encabezados,anchos, **kwargs):
        super().__init__(master, **kwargs)
        
        self.treeview = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        self.treeview.pack(padx=10, pady=10 , fill="both", expand=True)
        
        for i , col in enumerate(columnas):
          self.treeview.heading(col, text=encabezados[i])
          self.treeview.column(col,width=anchos[i], anchor="center")
        
    def cargar_datos(self,filas):
      for fila in filas:
        self.treeview.insert("", "end", values=fila)
    
    def obtener_seleccion(self):
      item = self.treeview.focus()
      return self.treeview.item(item, 'values') if item else None