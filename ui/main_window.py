# main_window.py
from services.siniestros import list_siniestros, get_or_create_client, create_siniestro, create_file, get_siniestro, list_files, list_last_siniestros
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import tkinter.filedialog as fd
import os, shutil, mimetypes
from tkinter import messagebox as mb
  # para adjuntar archivos en la vista de carga

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_DIR = os.path.join(BASE_DIR, "archivos siniestros")
os.makedirs(FILES_DIR, exist_ok=True)

# (Opcional) cuando conectes el back:
# from services.siniestros import list_siniestros, create_siniestro, create_file, list_files, create_client

# =========================
# Config global de la app
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk(fg_color="#0A0A0A")
window.title("Gestor de Siniestros")
window.geometry("1024x640")
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

# =========================
#    MAIN FRAME (derecha)
# =========================
main_frame = ctk.CTkFrame(window, fg_color="#242424")
main_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
main_frame.grid_rowconfigure(1, weight=1)   # zona de contenido dinámico
main_frame.grid_columnconfigure(0, weight=1)

# ---------- SEARCH BAR ----------
search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
search_frame.grid_columnconfigure(0, weight=1)  # que el entry se estire

img_search = CTkImage(light_image=Image.open("icons/search.png"), size=(20, 20))

def on_search_click(event=None):
    query = search_entry.get().strip()
    if query:
        clear_and_mount(render_list_siniestros, query=query)
    else:
        clear_and_mount(render_list_siniestros)

# Entry
search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="Buscar por cliente, patente o fecha",
    width=700,
    border_width=0
)
search_entry.grid(row=0, column=0, sticky="ew", padx=6, pady=6)
search_entry.bind("<Return>", on_search_click)  # <-- bind después de definir la función

# Botón lupa
search_button = ctk.CTkButton(
    search_frame,
    text="",
    image=img_search,
    width=44,
    height=36,
    fg_color="#161616",
    hover_color="#5e5bad",
    command=on_search_click  # <-- usar la misma función
)
search_button.grid(row=0, column=1, padx=6, pady=6)

# ---------- CONTENIDO DINÁMICO ----------
content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

def clear_and_mount(view_fn, *args, **kwargs):
    """Limpia y monta la vista que se pase como función (recibe parent)."""
    for w in content_frame.winfo_children():
        w.destroy()
    view_fn(content_frame, *args, **kwargs)

# =========================
#         VISTAS
# =========================
def render_home(parent):
    """Inicio: últimos siniestros (tabla minimal)."""
    quick = ctk.CTkFrame(parent, fg_color="transparent")
    quick.pack(fill="both", expand=True, padx=0, pady=0)

    title = ctk.CTkLabel(quick, text="Últimos siniestros", font=("Roboto", 16, "bold"))
    title.grid(row=0, column=0, sticky="w", pady=(0, 6))

    table = ctk.CTkFrame(quick, fg_color="#2A2A2A", corner_radius=8)
    table.grid(row=1, column=0, sticky="nsew")
    quick.grid_rowconfigure(1, weight=1)
    quick.grid_columnconfigure(0, weight=1)

    header = ctk.CTkFrame(table, fg_color="#252525", corner_radius=8)
    header.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
    for i, col in enumerate(("Patente", "Cliente", "Fecha")):
        ctk.CTkLabel(header, text=col, font=("Roboto", 12, "bold"))\
            .grid(row=0, column=i, sticky="w", padx=(10 if i == 0 else 6, 6), pady=6)
    header.grid_columnconfigure(0, weight=2)
    header.grid_columnconfigure(1, weight=5)
    header.grid_columnconfigure(2, weight=2)

    body = ctk.CTkScrollableFrame(table, fg_color="#2A2A2A", corner_radius=8)
    body.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
    table.grid_rowconfigure(1, weight=1)
    table.grid_columnconfigure(0, weight=1)

    rows = list_last_siniestros(limit=4)


    for r, dato in enumerate(rows):
        row_btn = ctk.CTkButton(
            body, text="", height=38,
            fg_color="#333333" if r % 2 == 0 else "#303030",
            hover_color="#3d3b6e", corner_radius=6
        )
        row_btn.grid(row=r, column=0, sticky="ew", padx=6, pady=4)
        body.grid_columnconfigure(0, weight=1)

        row_btn.grid_columnconfigure(0, weight=2)
        row_btn.grid_columnconfigure(1, weight=5)
        row_btn.grid_columnconfigure(2, weight=2)

        ctk.CTkLabel(row_btn, text=dato["patente"], font=("Roboto", 12))\
            .grid(row=0, column=0, sticky="w", padx=(10, 6))
        ctk.CTkLabel(row_btn, text=dato["cliente"], font=("Roboto", 12))\
            .grid(row=0, column=1, sticky="w", padx=6)
        ctk.CTkLabel(row_btn, text=dato["fecha"], font=("Roboto", 12))\
            .grid(row=0, column=2, sticky="w", padx=6)

        row_btn.configure(command=lambda d=dato: clear_and_mount(render_detalle_siniestro, d))


def render_list_siniestros(parent, query: str | None = None):
    """Listado completo de siniestros con diseño más vistoso y ancho completo."""
    wrapper = ctk.CTkFrame(parent, fg_color="transparent")
    wrapper.pack(fill="both", expand=True)

    # ---------- Título ----------
    titulo = "Todos los siniestros" if not query else f"Resultados para: {query}"
    title = ctk.CTkLabel(wrapper, text=titulo, font=("Roboto", 18, "bold"))
    title.pack(anchor="w", padx=10, pady=(0, 10))

    # ---------- Contenedor scroll ----------
    table = ctk.CTkScrollableFrame(wrapper, fg_color="#1E1E1E", corner_radius=10)
    table.pack(fill="both", expand=True, padx=10, pady=5)
    table.grid_columnconfigure(0, weight=1)

    # ---------- Encabezado ----------
    header = ctk.CTkFrame(table, fg_color="#3b447d", corner_radius=6)
    header.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 4))
    header.grid_columnconfigure(0, weight=2)
    header.grid_columnconfigure(1, weight=5)
    header.grid_columnconfigure(2, weight=2)

    ctk.CTkLabel(header, text="Patente", text_color="white",
                 font=("Roboto", 13, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    ctk.CTkLabel(header, text="Cliente", text_color="white",
                 font=("Roboto", 13, "bold")).grid(row=0, column=1, padx=10, pady=8, sticky="w")
    ctk.CTkLabel(header, text="Fecha", text_color="white",
                 font=("Roboto", 13, "bold")).grid(row=0, column=2, padx=10, pady=8, sticky="w")

    # ---------- Filas ----------
    rows = list_siniestros(order="date DESC")

    if query:
        q = query.lower()
        rows = [r for r in rows if q in r["patente"].lower() or q in r["cliente"].lower() or q in r["fecha"].lower()]

    for r, dato in enumerate(rows, start=1):
        bg_color = "#2d2d2d" if r % 2 else "#242424"
        row_frame = ctk.CTkFrame(table, fg_color=bg_color, corner_radius=6)
        row_frame.grid(row=r, column=0, sticky="ew", padx=6, pady=3)
        row_frame.grid_columnconfigure(0, weight=2)
        row_frame.grid_columnconfigure(1, weight=5)
        row_frame.grid_columnconfigure(2, weight=2)

        # Labels de info
        ctk.CTkLabel(row_frame, text=dato["patente"], font=("Roboto", 12))\
            .grid(row=0, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(row_frame, text=dato["cliente"], font=("Roboto", 12))\
            .grid(row=0, column=1, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(row_frame, text=dato["fecha"], font=("Roboto", 12))\
            .grid(row=0, column=2, padx=10, pady=8, sticky="w")

        # Hover effect + click en toda la fila
        def open_detail(_e=None, d=dato):
            clear_and_mount(render_detalle_siniestro, d)

        row_frame.bind("<Button-1>", open_detail)
        for child in row_frame.winfo_children():
            child.bind("<Button-1>", open_detail)



def render_cargar_siniestro(parent):
    """Formulario de alta."""
    global entry_cliente, entry_fecha, entry_patente, txt_desc, selected_files
    form = ctk.CTkFrame(parent, fg_color="#2A2A2A", corner_radius=10)
    form.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(form, text="Cargar nuevo siniestro", font=("Roboto", 16, "bold"))\
        .grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 8))

    labels = ["Cliente", "Fecha (YYYY-MM-DD)", "Patente", "Descripción"]
    for i, label in enumerate(labels, start=1):
        ctk.CTkLabel(form, text=label).grid(row=i, column=0, sticky="e", padx=10, pady=6)

    entry_cliente = ctk.CTkEntry(form, width=360)
    entry_fecha   = ctk.CTkEntry(form, width=360, placeholder_text="2025-09-23")
    entry_patente = ctk.CTkEntry(form, width=360)
    txt_desc      = ctk.CTkTextbox(form, width=360, height=100)

    entry_cliente.grid(row=1, column=1, sticky="w", padx=10, pady=6)
    entry_fecha.grid(  row=2, column=1, sticky="w", padx=10, pady=6)
    entry_patente.grid(row=3, column=1, sticky="w", padx=10, pady=6)
    txt_desc.grid(     row=4, column=1, sticky="w", padx=10, pady=6)

    selected_files = []

    def seleccionar_archivos():
        files = fd.askopenfilenames(title="Seleccionar archivos del siniestro")
        if files:
            selected_files.clear()
            selected_files.extend(files)
            files_label.configure(text=f"{len(selected_files)} archivo(s) seleccionado(s)")

    files_btn = ctk.CTkButton(form, text="Adjuntar archivos", command=seleccionar_archivos)
    files_btn.grid(row=5, column=0, sticky="e", padx=10, pady=10)

    files_label = ctk.CTkLabel(form, text="Ningún archivo seleccionado")
    files_label.grid(row=5, column=1, sticky="w", padx=10, pady=10)
    
    btn_guardar = ctk.CTkButton(
        form,
        text="Guardar siniestro",
        fg_color="#5e5bad",
        hover_color="#3b447d",
        command=guardar
    )
    btn_guardar.grid(row=6, column=0, columnspan=2, pady=10)

def guardar():
    try:
        cliente = entry_cliente.get().strip()
        fecha   = entry_fecha.get().strip()
        patente = entry_patente.get().strip()
        desc    = txt_desc.get("1.0", "end").strip()

        if not cliente or not fecha or not patente:
            mb.showerror("Campos obligatorios", "Completá Cliente, Fecha y Patente.")
            return

        # 1) Crear cliente si no existe
        client_id = get_or_create_client(cliente)

        # 2) Crear siniestro
        siniestro_id = create_siniestro(client_id, fecha, patente, desc)

        # 3) Guardar archivos seleccionados
        dest_dir = os.path.join(FILES_DIR, str(siniestro_id))
        os.makedirs(dest_dir, exist_ok=True)

        for src_path in selected_files:
            fname = os.path.basename(src_path)
            dest_path = os.path.join(dest_dir, fname)

            shutil.copy2(src_path, dest_path)

            mime, _ = mimetypes.guess_type(dest_path)
            mime = mime or ""

            rel_path = os.path.relpath(dest_path, BASE_DIR)

            create_file(siniestro_id, fname, mime, rel_path)

        mb.showinfo("Éxito", "Siniestro cargado correctamente.")

        # 4) Mostrar detalle del siniestro recién creado
        clear_and_mount(
            render_detalle_siniestro,
            {"id": siniestro_id, "cliente": cliente, "patente": patente, "fecha": fecha}
        )

    except Exception as e:
        mb.showerror("Error al guardar", f"Ocurrió un problema:\n{e}")



def render_detalle_siniestro(parent, dato: dict):
    """Detalle reutilizable (desde Inicio y Listado)."""
    wrapper = ctk.CTkFrame(parent, fg_color="transparent")
    wrapper.pack(fill="both", expand=True, padx=10, pady=10)

    header = ctk.CTkFrame(wrapper, fg_color="transparent")
    header.pack(fill="x", pady=(0, 6))

    ctk.CTkLabel(header, text=f"Detalle — {dato.get('patente','—')}", font=("Roboto", 16, "bold"))\
        .pack(side="left")

    ctk.CTkButton(header, text="← Volver", width=90,
                  command=lambda: clear_and_mount(render_list_siniestros))\
        .pack(side="right")

    panel = ctk.CTkFrame(wrapper, fg_color="#2A2A2A", corner_radius=10)
    panel.pack(fill="x", pady=6)

    grid = ctk.CTkFrame(panel, fg_color="transparent")
    grid.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(grid, text=f"Cliente:  {dato.get('cliente','—')}").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    ctk.CTkLabel(grid, text=f"Patente:  {dato.get('patente','—')}").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    ctk.CTkLabel(grid, text=f"Fecha:    {dato.get('fecha','—')}").grid(  row=2, column=0, sticky="w", padx=6, pady=4)

    files_box = ctk.CTkFrame(wrapper, fg_color="#2A2A2A", corner_radius=10)
    files_box.pack(fill="both", expand=True, pady=10)
    ctk.CTkLabel(files_box, text="Archivos adjuntos", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=(10,4))

    # --- Archivos adjuntos reales ---
    files = list_files(dato["id"])  # devuelve [(id, siniestro_id, fname, ftype, location), ...]

    for f in files:
        file_id, siniestro_id, fname, ftype, location = f
        ctk.CTkButton(
            files_box,
            text=f"📄 {fname}",
            height=34,
            fg_color="#333333",
            hover_color="#3d3b6e",
            anchor="w",
            command=lambda path=os.path.join(BASE_DIR, location): os.startfile(path)
        ).pack(fill="x", padx=10, pady=4)


# =========================
#        SIDEBAR (izq)
# =========================
sidebar = ctk.CTkFrame(window, width=280, fg_color="#161616", corner_radius=0)
sidebar.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

appname = ctk.CTkLabel(sidebar, text="CustomSiniestrosApp", font=("Roboto", 16), anchor="center")
appname.pack(fill="x", pady=10, padx=10)

img_home = CTkImage(light_image=Image.open("icons/home.png"), size=(20, 20))
btn_home = ctk.CTkButton(sidebar, width=200, height=36, text="Inicio",
                         image=img_home, compound="left", anchor="w",
                         fg_color="#161616", hover_color="#5e5bad",
                         command=lambda: clear_and_mount(render_home))
btn_home.pack(pady=6)

img_files = CTkImage(light_image=Image.open("icons/folder.png"), size=(20, 20))
btn_ver = ctk.CTkButton(sidebar, width=200, height=36, text="Ver siniestros",
                        image=img_files, compound="left", anchor="w",
                        fg_color="#161616", hover_color="#5e5bad",
                        command=lambda: clear_and_mount(render_list_siniestros))
btn_ver.pack(pady=6)

spacer = ctk.CTkFrame(sidebar, fg_color="#161616")
spacer.pack(fill="both", expand=True)

img_load = CTkImage(light_image=Image.open("icons/plus.png"), size=(20, 20))
btn_cargar = ctk.CTkButton(sidebar, width=200, height=42, corner_radius=10, text="Cargar siniestro",
                           image=img_load, compound="left",
                           fg_color="#5e5bad", hover_color="#3b447d",
                           command=lambda: clear_and_mount(render_cargar_siniestro))
btn_cargar.pack(pady=10)

# =========================
#   Mostrar Inicio al abrir
# =========================
clear_and_mount(render_home)

# =========================
#        Run app
# =========================
window.mainloop()
