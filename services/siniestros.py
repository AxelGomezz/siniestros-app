import sqlite3
import os

def get_connection():
    #dirname = carpeta actual || abspath(__file__) = Ruta absoluta archivo actual
    base_dir = os.path.dirname(os.path.abspath(__file__))

    #join une las rutas (base_dir y "...")
    db_path = os.path.join(base_dir, "../database/siniestros.db")
    return sqlite3.connect(db_path)


# -------- CLIENTES --------


def create_client(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO clients (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def list_client():
    conn = get_connection()
    cursor = conn.cursor()

    #ejecuta la consulta guardando los resultados en memoria.
    cursor.execute("SELECT * FROM clients")
    list = cursor.fetchall() #recupera los resultados de la ultima consulta ejecutada

    conn.close()

    return list


#-------- SINIESTROS --------

def create_siniestro(client_id, date, patente, descripcion):
    #Crea un nuevo siniestro relacionado a un cliente existente
    conn = get_connection()
    cursor = conn.cursor()

    #inserta siniestro en la tabla
    cursor.execute("""
        INSERT INTO siniestros (client_id, date, patente, descripcion) 
        VALUES (?,?,?,?)""",
        (client_id, date, patente, descripcion))

    conn.commit()
    conn.close()


def list_siniestros():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM siniestros")
    list = cursor.fetchall()

    conn.close()

    return list