import sqlite3

# Crea / conecta la base de datos
conn = sqlite3.connect("siniestros.db")

# crea el cursor con el cual se ejecutan comandos SQL
cursor = conn.cursor()

#Crea tabla clients
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
"""
)

#Crea tabla siniestros
cursor.execute("""
CREATE TABLE IF NOT EXISTS siniestros (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    patente TEXT,
    descripcion TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
)
"""
)

#Crea tabla files
cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    siniestro_id INTEGER NOT NULL,
    file_name TEXT,
    file_type TEXT,
    location TEXT NOT NULL,
    FOREIGN KEY (siniestro_id) REFERENCES siniestros(id)
)
""")


#Confirma los cambios
conn.commit()

#Cierra la conexion
conn.close()