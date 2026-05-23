import sqlite3
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_NAME = "funcionarios_prueba.db" if os.environ.get("DB_MODE") == "test" else "funcionarios.db"
DB_FILE = os.path.join(DATA_DIR, DB_NAME)


def _get_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def _crear_tablas():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            cedula TEXT PRIMARY KEY,
            nombre TEXT, apellido TEXT, fecha_nacimiento TEXT, edad TEXT,
            telefono TEXT, peso TEXT, altura TEXT, estado_civil TEXT, residencia TEXT,
            jerarquia TEXT, lugar_presta_servicio TEXT, tiempo_servicio TEXT, salario_mensual TEXT,
            terreno_propio TEXT, ubicacion_terreno TEXT, condicion_vivienda TEXT,
            necesidad_vivienda TEXT, organismo_publico TEXT, organismo_privado TEXT,
            gestion_organismo_oficial TEXT, fecha_gestion TEXT,
            tenencia_tierra TEXT, ambiente_vivienda TEXT, tiempo_ocupacion TEXT,
            servicio_vivienda_disponible TEXT, materiales_vivienda TEXT, servicio_comunidad TEXT,
            activo INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS familiares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_cedula TEXT REFERENCES funcionarios(cedula),
            nombre TEXT, apellido TEXT, parentesco TEXT, edad TEXT,
            genero TEXT, estado_civil TEXT, nivel_educacion TEXT,
            profesion_oficio TEXT, lugar_trabajo TEXT, ingreso_mensual TEXT, observacion TEXT
        );
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT,
            rol TEXT
        );
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT, accion TEXT, detalle TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                       ("admin", "admin123", "admin"))
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                       ("visor", "visor123", "viewer"))
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                       ("editor", "editor123", "editor"))
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                       ("modificador", "mod123", "modifier"))
    conn.commit()
    conn.close()

    # Migration: ensure 'subadmin' role is allowed in usuarios table
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='usuarios'")
    schema = cursor.fetchone()
    if schema and "CHECK" in schema[0].upper():
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios_new (
                username TEXT PRIMARY KEY,
                password TEXT,
                rol TEXT
            );
            INSERT INTO usuarios_new SELECT * FROM usuarios;
            DROP TABLE usuarios;
            ALTER TABLE usuarios_new RENAME TO usuarios;
        """)
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                   ("subadmin", "sub123", "subadmin"))
    conn.commit()
    conn.close()

    # Migration: add activo column if missing
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE funcionarios ADD COLUMN activo INTEGER DEFAULT 1")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass


# --- Funcionario ---

class Funcionario():
    def __init__(self, cedula, nombre, apellido, fecha_nacimiento, edad, telefono, peso, altura, estado_civil, residencia):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.telefono = telefono
        self.peso = peso
        self.altura = altura
        self.estado_civil = estado_civil
        self.residencia = residencia
        self.grupo_familiar = []

    def agregar_familiar(self, familiar):
        self.grupo_familiar.append(familiar)

    def datos_laborales(self, jerarquia, lugar_presta_servicio, tiempo_servicio, salario_mensual):
        self.jerarquia = jerarquia
        self.lugar_presta_servicio = lugar_presta_servicio
        self.tiempo_servicio = tiempo_servicio
        self.salario_mensual = salario_mensual

    def plan_vivienda(self, terreno_propio, ubicacion_terreno, condicion_vivienda, necesidad_vivienda, organismo_publico, organismo_privado, gestion_organismo_oficial, fecha_gestion):
        self.terreno_propio = terreno_propio
        self.ubicacion_terreno = ubicacion_terreno
        self.condicion_vivienda = condicion_vivienda
        self.necesidad_vivienda = necesidad_vivienda
        self.gestion_organismo_oficial = gestion_organismo_oficial
        self.organismo_publico = organismo_publico
        self.organismo_privado = organismo_privado
        self.fecha_gestion = fecha_gestion

    def estado_vivienda(self, tenencia_tierra, ambiente_vivienda, tiempo_ocupacion, servicio_vivienda_disponible, materiales_vivienda, servicio_comunidad):
        self.tenencia_tierra = tenencia_tierra
        self.ambiente_vivienda = ambiente_vivienda
        self.tiempo_ocupacion = tiempo_ocupacion
        self.servicio_vivienda_disponible = servicio_vivienda_disponible
        self.materiales_vivienda = materiales_vivienda
        self.servicio_comunidad = servicio_comunidad


class Familiar():
    def __init__(self, nombre, apellido, parentesco, edad, genero, estado_civil, nivel_educacion, profesion_oficio, lugar_trabajo, ingreso_mensual, observacion):
        self.nombre = nombre
        self.apellido = apellido
        self.parentesco = parentesco
        self.edad = edad
        self.genero = genero
        self.estado_civil = estado_civil
        self.nivel_educacion = nivel_educacion
        self.profesion_oficio = profesion_oficio
        self.lugar_trabajo = lugar_trabajo
        self.ingreso_mensual = ingreso_mensual
        self.observacion = observacion


def cargar_funcionarios(incluir_inactivos=False):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM funcionarios"
    if not incluir_inactivos:
        query += " WHERE activo = 1"
    query += " ORDER BY cedula"

    cursor.execute(query)
    rows = cursor.fetchall()

    funcionarios = []
    for row in rows:
        f = Funcionario(
            row["cedula"], row["nombre"], row["apellido"],
            row["fecha_nacimiento"], row["edad"], row["telefono"],
            row["peso"], row["altura"], row["estado_civil"], row["residencia"]
        )
        f._activo = row["activo"]
        fields_laborales = ["jerarquia", "lugar_presta_servicio", "tiempo_servicio", "salario_mensual"]
        if row["jerarquia"]:
            f.datos_laborales(*(row[c] for c in fields_laborales))

        fields_vivienda = ["terreno_propio", "ubicacion_terreno", "condicion_vivienda", "necesidad_vivienda",
                          "organismo_publico", "organismo_privado", "gestion_organismo_oficial", "fecha_gestion"]
        if row["terreno_propio"]:
            f.plan_vivienda(*(row[c] for c in fields_vivienda))

        fields_estado = ["tenencia_tierra", "ambiente_vivienda", "tiempo_ocupacion",
                        "servicio_vivienda_disponible", "materiales_vivienda", "servicio_comunidad"]
        if row["tenencia_tierra"]:
            f.estado_vivienda(*(row[c] for c in fields_estado))

        cursor.execute("SELECT * FROM familiares WHERE funcionario_cedula = ?", (f.cedula,))
        for fam_row in cursor.fetchall():
            fam = Familiar(
                fam_row["nombre"], fam_row["apellido"], fam_row["parentesco"],
                fam_row["edad"] if fam_row["edad"] else "",
                fam_row["genero"], fam_row["estado_civil"],
                fam_row["nivel_educacion"], fam_row["profesion_oficio"],
                fam_row["lugar_trabajo"],
                fam_row["ingreso_mensual"] if fam_row["ingreso_mensual"] else "",
                fam_row["observacion"]
            )
            f.agregar_familiar(fam)

        funcionarios.append(f)

    conn.close()
    return funcionarios


def guardar_funcionarios(funcionarios):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()

    for f in funcionarios:
        cursor.execute("SELECT activo FROM funcionarios WHERE cedula = ?", (f.cedula,))
        existing = cursor.fetchone()
        activo_val = existing["activo"] if existing else getattr(f, '_activo', 1)
        cursor.execute("""
            INSERT OR REPLACE INTO funcionarios (
                cedula, nombre, apellido, fecha_nacimiento, edad, telefono, peso, altura,
                estado_civil, residencia, jerarquia, lugar_presta_servicio, tiempo_servicio,
                salario_mensual, terreno_propio, ubicacion_terreno, condicion_vivienda,
                necesidad_vivienda, organismo_publico, organismo_privado,
                gestion_organismo_oficial, fecha_gestion, tenencia_tierra, ambiente_vivienda,
                tiempo_ocupacion, servicio_vivienda_disponible, materiales_vivienda, servicio_comunidad,
                activo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f.cedula, f.nombre, f.apellido, f.fecha_nacimiento, f.edad, f.telefono, f.peso,
            f.altura, f.estado_civil, f.residencia,
            getattr(f, "jerarquia", None), getattr(f, "lugar_presta_servicio", None),
            getattr(f, "tiempo_servicio", None), getattr(f, "salario_mensual", None),
            getattr(f, "terreno_propio", None), getattr(f, "ubicacion_terreno", None),
            getattr(f, "condicion_vivienda", None), getattr(f, "necesidad_vivienda", None),
            getattr(f, "organismo_publico", None), getattr(f, "organismo_privado", None),
            getattr(f, "gestion_organismo_oficial", None), getattr(f, "fecha_gestion", None),
            getattr(f, "tenencia_tierra", None), getattr(f, "ambiente_vivienda", None),
            getattr(f, "tiempo_ocupacion", None), getattr(f, "servicio_vivienda_disponible", None),
            getattr(f, "materiales_vivienda", None), getattr(f, "servicio_comunidad", None),
            activo_val,
        ))

        cursor.execute("DELETE FROM familiares WHERE funcionario_cedula = ?", (f.cedula,))
        for fam in f.grupo_familiar:
            cursor.execute("""
                INSERT INTO familiares (
                    funcionario_cedula, nombre, apellido, parentesco, edad, genero,
                    estado_civil, nivel_educacion, profesion_oficio, lugar_trabajo,
                    ingreso_mensual, observacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f.cedula, fam.nombre, fam.apellido, fam.parentesco, fam.edad, fam.genero,
                fam.estado_civil, fam.nivel_educacion, fam.profesion_oficio, fam.lugar_trabajo,
                fam.ingreso_mensual, fam.observacion
            ))

    conn.commit()
    conn.close()


def eliminar_funcionario(cedula, usuario=None):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE funcionarios SET activo = 0 WHERE cedula = ?", (cedula,))
    conn.commit()
    conn.close()
    if usuario:
        registrar_auditoria(usuario, "ELIMINAR",
                            f"Funcionario cedula {cedula} marcado como inactivo")


def restaurar_funcionario(cedula, usuario=None):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE funcionarios SET activo = 1 WHERE cedula = ?", (cedula,))
    conn.commit()
    conn.close()
    if usuario:
        registrar_auditoria(usuario, "RESTAURAR",
                            f"Funcionario cedula {cedula} restaurado")


# --- Usuarios ---

def verificar_login(username, password):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?",
                   (username, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"username": row["username"], "rol": row["rol"]}
    return None


def crear_usuario(username, password, rol):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                   (username, password, rol))
    conn.commit()
    conn.close()


def eliminar_usuario(username):
    if username == "admin":
        return False
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return True


def obtener_usuarios():
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, rol FROM usuarios ORDER BY username")
    rows = cursor.fetchall()
    conn.close()
    return [{"username": r["username"], "rol": r["rol"]} for r in rows]


# --- Auditoria ---

def registrar_auditoria(usuario, accion, detalle):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO auditoria (usuario, accion, detalle) VALUES (?, ?, ?)",
                   (usuario, accion, detalle))
    conn.commit()
    conn.close()


def obtener_auditoria(limite=100):
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auditoria ORDER BY fecha DESC LIMIT ?", (limite,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r["id"], "usuario": r["usuario"], "accion": r["accion"],
             "detalle": r["detalle"], "fecha": r["fecha"]} for r in rows]


ROLES = {
    "viewer": {"ver": True, "crear": False, "modificar": False, "eliminar": False},
    "editor": {"ver": True, "crear": True, "modificar": False, "eliminar": False},
    "modifier": {"ver": True, "crear": True, "modificar": True, "eliminar": False},
    "subadmin": {"ver": True, "crear": True, "modificar": True, "eliminar": True},
    "admin": {"ver": True, "crear": True, "modificar": True, "eliminar": True},
}
