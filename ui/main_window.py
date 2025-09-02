import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image

from add_siniestro_window import AddSiniestroWindow

# Configuraciones globales
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# window principal
window = ctk.CTk(fg_color="#0A0A0A")
    #window.overrideredirect(True)
window.title("Gestor de Siniestros")
window.geometry("900x600")
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

# Encabezado
#header = ctk.CTkLabel(window, text="Gestor de Siniestros", font=("Arial", 20))
#header.grid(row=0, column=0, columnspan=2, pady=10)

#================================================================================
#                                   SIDEBAR
#================================================================================
sidebar = ctk.CTkFrame(window, width=300, fg_color="#161616", corner_radius=0)
sidebar.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

#---------
#  TITLE
#---------
appname = ctk.CTkLabel(sidebar, text="CustomSiniestrosApp", font=("Roboto", 16), anchor="center")
appname.pack(fill="x", pady=10, padx=10)


#|--------------------|
#|     BUTTON HOME    |
#|--------------------|
img_home = CTkImage(light_image=Image.open("icons/home.png"), size=(20, 20)) #Image Charged

btn_home = ctk.CTkButton(
    sidebar,
    width=180,
    height=30,
    text="Inicio",
    image=img_home, 
    compound="left",
    anchor="w",
    fg_color="#161616", 
    hover_color="#5e5bad"
    )
btn_home.pack(pady=5)


#|--------------------|
#|    BUTTON FILES    |
#|--------------------|
img_files = CTkImage(light_image=Image.open("icons/folder.png"), size=(20,20))

btn_ver = ctk.CTkButton(
    sidebar,
    width=180,
    height=30,
    text="Ver siniestros",
    image=img_files,
    compound="left",
    anchor="w",
    fg_color="#161616",
    hover_color="#5e5bad"
    )
btn_ver.pack(pady=10)

#|--------|
#| SPACER |
#|--------|
spacer = ctk.CTkFrame(sidebar, fg_color="#161616")
spacer.pack(fill="both", expand=True)


#|-------------------|
#|    BUTTON LOAD    |
#|-------------------|
img_load = CTkImage(light_image=Image.open("icons/plus.png"), size=(20,20))

btn_cargar = ctk.CTkButton(
    sidebar,
    width=180,
    height=50,
    corner_radius=10,
    text="Cargar siniestro",
    image=img_load,
    compound="left",
    fg_color="#5e5bad",
    hover_color="#3b447d"
    )
btn_cargar.pack(pady=10)


# Área principal
main_frame = ctk.CTkFrame(window)
main_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)


# Ejecutar app
window.mainloop()