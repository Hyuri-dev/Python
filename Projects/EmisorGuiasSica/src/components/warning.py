import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox

class Warning():
    def __init__(self, master, on_add=None, on_edit=None, on_delete=None, **kwargs):
        super().__init__(master, **kwargs)
        self.warning = messagebox.showinfo()