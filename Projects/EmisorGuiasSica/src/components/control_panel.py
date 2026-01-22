import ttkbootstrap as ttk


class ControlPanel(ttk.Frame):
    def __init__(self, master, on_add=None, on_edit=None, on_delete=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Guardamos las funciones que se ejecutarán al presionar los botones
        self.on_add = on_add
        self.on_edit = on_edit
        self.on_delete = on_delete

        # Configuración de estilo y botones
        self.btn_add = ttk.Button(self, text="Agregar", bootstyle="success", command=self.on_add)
        self.btn_add.pack(side='left', padx=5)

        self.btn_edit = ttk.Button(self, text="Editar", bootstyle="info", command=self.on_edit)
        self.btn_edit.pack(side='left', padx=5)

        self.btn_delete = ttk.Button(self, text="Eliminar", bootstyle="danger", command=self.on_delete)
        self.btn_delete.pack(side='left', padx=5)