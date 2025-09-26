# services/siniestros.py
import sqlite3
import os

# --------------------------
# Conexión a la base de datos
# --------------------------
def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "database", "siniestros.db")

    # Verifica si la DB existe
    first_time = not os.path.exists(db_path)

    # Se conecta (esto también crea el archivo si no existe)
    conn = sqlite3.connect(db_path)

    # Si es la primera vez, crea las tablas necesarias
    if first_time:
        cur = conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS siniestros (
            id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            patente TEXT,
            descripcion TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            siniestro_id INTEGER NOT NULL,
            file_name TEXT,
            file_type TEXT,
            location TEXT NOT NULL,
            FOREIGN KEY (siniestro_id) REFERENCES siniestros(id)
        );
        """)
        conn.commit()

    return conn



# --------------------------
# CLIENTES
# --------------------------
def create_client(name: str) -> int:
    """Crea un cliente y devuelve su id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (name) VALUES (?)", (name,))
    conn.commit()
    client_id = cur.lastrowid
    conn.close()
    return client_id

def get_client_by_name(name: str):
    """Devuelve (id, name) si existe, o None si no existe."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM clients WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row  # (id, name) o None

def get_or_create_client(name: str) -> int:
    """Si el cliente existe, devuelve su id; si no, lo crea y lo devuelve."""
    row = get_client_by_name(name)
    if row:
        return row[0]
    return create_client(name)

def list_client():
    """Mantengo tu función original (devuelve lista de tuplas)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    conn.close()
    return rows


# --------------------------
# SINIESTROS
# --------------------------
def create_siniestro(client_id: int, date: str, patente: str, descripcion: str) -> int:
    """
    Crea un nuevo siniestro y devuelve su id.
    - date: 'YYYY-MM-DD' (guardado como TEXT en SQLite)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO siniestros (client_id, date, patente, descripcion)
        VALUES (?, ?, ?, ?)
    """, (client_id, date, patente, descripcion))
    conn.commit()
    siniestro_id = cur.lastrowid
    conn.close()
    return siniestro_id

def list_siniestros(limit: int | None = None, query: str | None = None, order: str = "date DESC"):
    """
    Devuelve lista de siniestros como diccionarios: {id, patente, fecha, cliente}
    - limit: limita la cantidad de filas (p. ej. últimos 4)
    - query: filtra por patente, nombre de cliente o fecha (LIKE)
    - order: campo de ordenamiento (por defecto date DESC)
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT s.id, s.patente, s.date, c.name AS cliente
    FROM siniestros s
    JOIN clients c ON c.id = s.client_id
    """
    params = []
    conditions = []

    if query:
        q = f"%{query}%"
        conditions.append("(s.patente LIKE ? OR c.name LIKE ? OR s.date LIKE ?)")
        params.extend([q, q, q])

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # ⚠️ 'order' viene con valor por defecto seguro; no interpolar input del usuario sin validar
    sql += f" ORDER BY {order}"

    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [{"id": r[0], "patente": r[1], "fecha": r[2], "cliente": r[3]} for r in rows]

def get_siniestro(siniestro_id: int):
    """Devuelve un siniestro con su cliente: {id, patente, fecha, cliente, descripcion} o None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.patente, s.date, c.name AS cliente, s.descripcion
        FROM siniestros s
        JOIN clients c ON c.id = s.client_id
        WHERE s.id = ?
    """, (siniestro_id,))
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    return {"id": r[0], "patente": r[1], "fecha": r[2], "cliente": r[3], "descripcion": r[4]}

def list_siniestros_raw():
    """Tu versión original (para debug): devuelve tuplas de la tabla siniestros."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM siniestros")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_siniestro(siniestro_id: int) -> None:
    """Elimina un siniestro y sus archivos asociados en DB (NO borra físicamente los archivos)."""
    conn = get_connection()
    cur = conn.cursor()

    # Primero borrar archivos asociados (DB)
    cur.execute("DELETE FROM files WHERE siniestro_id = ?", (siniestro_id,))

    # Luego borrar el siniestro
    cur.execute("DELETE FROM siniestros WHERE id = ?", (siniestro_id,))

    conn.commit()
    conn.close()


# --------------------------
# ARCHIVOS
# --------------------------
def create_file(siniestro_id: int, file_name: str, file_type: str, location: str) -> int:
    """Crea un registro de archivo y devuelve su id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO files (siniestro_id, file_name, file_type, location)
        VALUES (?, ?, ?, ?)
    """, (siniestro_id, file_name, file_type, location))
    conn.commit()
    file_id = cur.lastrowid
    conn.close()
    return file_id

def list_files(siniestro_id: int):
    """Devuelve lista de tuplas de archivos del siniestro dado."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, siniestro_id, file_name, file_type, location
        FROM files
        WHERE siniestro_id = ?
    """, (siniestro_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def list_last_siniestros(limit=4):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, s.patente, c.name AS cliente, s.date
        FROM siniestros s
        JOIN clients c ON s.client_id = c.id
        ORDER BY s.date DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    # Convertir a lista de diccionarios (igual que tus datos dummy)
    return [
        {"id": r[0], "patente": r[1], "cliente": r[2], "fecha": r[3]}
        for r in rows
    ]
