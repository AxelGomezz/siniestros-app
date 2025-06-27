import sqlite3

# Crea / conecta la base de datos
conn = sqlite3.connect("database/siniestros.db")

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

#Confirma los cambios
conn.commit()

#Cierra la conexion
conn.close()