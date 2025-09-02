import customtkinter as ctk

class AddSiniestroWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar nuevo siniestro")
        self.geometry("400x400")
        self.resizable(False, False)

        label = ctk.CTkLabel(self, text="Formulario de nuevo siniestro")
        label.pack(pady=10)