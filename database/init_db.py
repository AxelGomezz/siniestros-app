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

#Confirma los cambios
conn.commit()

#Cierra la conexion
conn.close()