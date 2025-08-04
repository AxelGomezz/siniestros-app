import customtkinter as ctk

# Configuraciones globales
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# window principal
window = ctk.CTk()
window.title("Gestor de Siniestros")
window.geometry("900x600")
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

"""# Encabezado
header = ctk.CTkLabel(window, text="Gestor de Siniestros", font=("Arial", 20))
header.grid(row=0, column=0, columnspan=2, pady=10)

# Sidebar
sidebar = ctk.CTkFrame(window, width=200)
sidebar.grid(row=1, column=0, sticky="ns", padx=10, pady=10)

btn_inicio = ctk.CTkButton(sidebar, text="Inicio")
btn_inicio.pack(pady=10)

btn_cargar = ctk.CTkButton(sidebar, text="Cargar siniestro")
btn_cargar.pack(pady=10)

btn_ver = ctk.CTkButton(sidebar, text="Ver siniestros")
btn_ver.pack(pady=10)

# Área principal
main_frame = ctk.CTkFrame(window)
main_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
"""

# ===================================================================================
#                                     HEADER MAIN 
# ===================================================================================
#Header Frame
header_frame = ctk.CTkFrame(window, height=100)
header_frame.grid(row=0, column=0, sticky="nwe", columnspan=2)

#Header-search Frame
search_entry = ctk.CTkEntry(window, width=600, height=50, placeholder_text="Buscar por patente, cliente o fecha") 
search_entry.grid(row=0, column=1, sticky="n", padx=(5,20), pady=(5, 20))

#Btn "Add New"
btn_add_siniestro = ctk.CTkButton(window, height=50, width=40 ,text="+ Agregar Nuevo")
btn_add_siniestro.grid(row=0, column=0, sticky="en", padx=(60,5), pady=(5, 20))

# ===================================================================================
#                                   SECTION MAIN
# ===================================================================================

#Section main
section_frame = ctk.CTkFrame(window)
section_frame.grid_columnconfigure(0, weight=1)
section_frame.grid(row = 1, column=0, sticky="nsew", columnspan=2)

#Section text
section_text = ctk.CTkLabel(section_frame, text="Ultimos siniestros cargados", font=ctk.CTkFont(size=24, weight="bold"))
section_text.grid(row=0, column=0, sticky="nsew", pady=(10,5), padx=10)

#last uploaded box
last_uploaded_box = ctk.CTkFrame(section_frame, height=400 , corner_radius=10)
last_uploaded_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Ejecutar app
window.mainloop()