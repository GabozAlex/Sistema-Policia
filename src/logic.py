import sqlite3
import os
import sys
from datetime import datetime

DB_NAME = "funcionarios_prueba.db" if os.environ.get("DB_MODE") == "test" else "funcionarios.db"

if getattr(sys, "frozen", False):
    # PyInstaller congelado: la BD debe vivir fuera de la carpeta temporal (_MEIPASS)
    if os.name == "nt":
        _base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        _base_dir = os.path.join(os.path.expanduser("~"), ".local", "share")
    DATA_DIR = os.path.join(_base_dir, "SistemaPolicia", "data")
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
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
        CREATE TABLE IF NOT EXISTS catalogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor TEXT NOT NULL,
            detalle TEXT DEFAULT '',
            orden INTEGER DEFAULT 0,
            activo INTEGER DEFAULT 1,
            UNIQUE(tipo, valor)
        );
        CREATE TABLE IF NOT EXISTS operadora_prefijos (
            prefijo TEXT PRIMARY KEY,
            operadora TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS funcionarios (
            cedula TEXT PRIMARY KEY,
            nombre TEXT, apellido TEXT, fecha_nacimiento TEXT, edad TEXT,
            telefono TEXT, operadora TEXT, peso TEXT, altura TEXT, genero TEXT, estado_civil TEXT, residencia TEXT,
            residencia_municipio TEXT, residencia_pueblo TEXT,
            jerarquia TEXT, lugar_presta_servicio TEXT, tiempo_servicio TEXT, salario_mensual TEXT,
            terreno_propio TEXT, ubicacion_terreno TEXT, condicion_vivienda TEXT,
            necesidad_vivienda TEXT, organismo_publico TEXT, organismo_privado TEXT,
            gestion_organismo_oficial TEXT, fecha_gestion TEXT,
            tenencia_tierra TEXT, ambiente_vivienda TEXT, tiempo_ocupacion TEXT,
            servicio_vivienda_disponible TEXT, materiales_vivienda TEXT, servicio_comunidad TEXT,
            posee_vivienda TEXT, tenencia_tierra_otra TEXT,
            ingreso_trabajador TEXT DEFAULT '0',
            ingreso_familiar_adicional TEXT DEFAULT '0',
            total_ingreso_familiar TEXT DEFAULT '0',
            egreso_grupo_familiar TEXT DEFAULT '0',
            disponibilidad_economica TEXT DEFAULT '0',
            activo INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS familiares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_cedula TEXT REFERENCES funcionarios(cedula),
            nombre TEXT, apellido TEXT, parentesco TEXT, edad TEXT,
            genero TEXT, estado_civil TEXT, nivel_educacion TEXT,
            profesion_oficio TEXT, lugar_trabajo TEXT, ingreso_mensual TEXT, observacion TEXT
        );
        CREATE TABLE IF NOT EXISTS egresos_mensuales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_cedula TEXT REFERENCES funcionarios(cedula),
            rubro TEXT NOT NULL,
            monto TEXT DEFAULT '0',
            observacion TEXT DEFAULT ''
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
    # Sembrar catálogos
    cursor.executescript("""
        INSERT OR IGNORE INTO catalogos (tipo, valor, detalle, orden) VALUES
        ('estado_civil', 'Soltero/a', '', 1),
        ('estado_civil', 'Casado/a', '', 2),
        ('estado_civil', 'Divorciado/a', '', 3),
        ('estado_civil', 'Viudo/a', '', 4),
        ('estado_civil', 'Separado/a', '', 5),
        ('estado_civil', 'Unión libre / Pareja de hecho', '', 6),
        ('jerarquia', 'Oficial', '', 1),
        ('jerarquia', 'Oficial Agregado', '', 2),
        ('jerarquia', 'Oficial Jefe', '', 3),
        ('jerarquia', 'Supervisor', '', 4),
        ('jerarquia', 'Supervisor Agregado', '', 5),
        ('jerarquia', 'Supervisor Jefe', '', 6),
        ('jerarquia', 'Comisionado', '', 7),
        ('jerarquia', 'Comisionado Agregado', '', 8),
        ('jerarquia', 'Comisionado Jefe', '', 9),
        ('lugar_servicio', 'Sede Central', 'Av. Simón Bolívar, La Asunción (Arismendi)', 1),
        ('lugar_servicio', 'Estación Arismendi', 'La Asunción', 2),
        ('lugar_servicio', 'Base Boca del Río', 'Calle Las Marinas, Península de Macanao', 3),
        ('lugar_servicio', 'Base Boca de Pozo', 'Parroquia San Francisco, Península de Macanao', 4),
        ('lugar_servicio', 'Comando García', 'Calle Principal, Villa Rosa, Fajardo', 5),
        ('lugar_servicio', 'Estación Díaz', 'Urbanismo Carcanapiral, municipio Díaz', 6),
        ('lugar_servicio', 'Estación Tubores', 'C. Colón, Punta de Piedras', 7),
        ('lugar_servicio', 'Base Sabanamar', 'Porlamar (municipio Mariño)', 8);

        INSERT OR IGNORE INTO catalogos (tipo, valor, detalle, orden) VALUES
        ('parentesco', 'Jefe/a', '', 1),
        ('parentesco', 'Cónyuge/pareja', '', 2),
        ('parentesco', 'Hijo/a', '', 3),
        ('parentesco', 'Nieto/a', '', 4),
        ('parentesco', 'Padre/madre', '', 5),
        ('parentesco', 'Hermano/a', '', 6),
        ('parentesco', 'Otro pariente', '', 7),
        ('parentesco', 'No pariente', '', 8),
        ('nivel_educacion', 'Sin estudios', '', 1),
        ('nivel_educacion', 'Básica', '', 2),
        ('nivel_educacion', 'Media', '', 3),
        ('nivel_educacion', 'Técnico superior', '', 4),
        ('nivel_educacion', 'Universitario', '', 5),
        ('nivel_educacion', 'Maestría/Doctorado', '', 6),
        ('profesion', 'Medicina / Salud', '', 1),
        ('profesion', 'Ingeniería', '', 2),
        ('profesion', 'Derecho', '', 3),
        ('profesion', 'Administración / Contaduría', '', 4),
        ('profesion', 'Educación', '', 5),
        ('profesion', 'Arquitectura / Urbanismo', '', 6),
        ('profesion', 'Ciencias Básicas (Biología, Física, Química, etc.)', '', 7),
        ('profesion', 'Humanidades / Letras / Artes', '', 8),
        ('profesion', 'Ciencias Sociales (Sociología, Psicología, Trabajo Social, etc.)', '', 9),
        ('profesion', 'Agronomía / Zootecnia', '', 10),
        ('profesion', 'Otra', '', 11),
        ('condicion_vivienda', 'Buena', '', 1),
        ('condicion_vivienda', 'Regular', '', 2),
        ('condicion_vivienda', 'Mala (requiere reparaciones menores)', '', 3),
        ('condicion_vivienda', 'Muy mala / inhabitable', '', 4),
        ('municipio', 'Antolín del Campo', '', 1),
        ('municipio', 'Arismendi', '', 2),
        ('municipio', 'Antonio Díaz', '', 3),
        ('municipio', 'García', '', 4),
        ('municipio', 'Gómez', '', 5),
        ('municipio', 'Maneiro', '', 6),
        ('municipio', 'Marcano', '', 7),
        ('municipio', 'Mariño', '', 8),
        ('municipio', 'Península de Macanao', '', 9),
        ('municipio', 'Tubores', '', 10),
        ('municipio', 'Villalba', '', 11),
        ('pueblo', 'La Plaza de Paraguachí', 'Antolín del Campo', 1),
        ('pueblo', 'Paraguachí', 'Antolín del Campo', 2),
        ('pueblo', 'La Asunción', 'Arismendi', 3),
        ('pueblo', 'Atamo', 'Arismendi', 4),
        ('pueblo', 'San Juan Bautista', 'Antonio Díaz', 5),
        ('pueblo', 'La Guardia', 'Antonio Díaz', 6),
        ('pueblo', 'Playa El Yaque', 'Antonio Díaz', 7),
        ('pueblo', 'El Valle del Espíritu Santo', 'García', 8),
        ('pueblo', 'Villa Rosa', 'García', 9),
        ('pueblo', 'Las Guevaras', 'García', 10),
        ('pueblo', 'Santa Ana', 'Gómez', 11),
        ('pueblo', 'Tacarigua', 'Gómez', 12),
        ('pueblo', 'Pedro González', 'Gómez', 13),
        ('pueblo', 'Altagracia', 'Gómez', 14),
        ('pueblo', 'El Maco', 'Gómez', 15),
        ('pueblo', 'Pampatar', 'Maneiro', 16),
        ('pueblo', 'Los Robles', 'Maneiro', 17),
        ('pueblo', 'El Pilar', 'Maneiro', 18),
        ('pueblo', 'Juan Griego', 'Marcano', 19),
        ('pueblo', 'Los Millanes', 'Marcano', 20),
        ('pueblo', 'Porlamar', 'Mariño', 21),
        ('pueblo', 'Bella Vista', 'Mariño', 22),
        ('pueblo', 'Boca de Río', 'Península de Macanao', 23),
        ('pueblo', 'Boca de Pozo', 'Península de Macanao', 24),
        ('pueblo', 'Punta de Piedras', 'Tubores', 25),
        ('pueblo', 'El Guamache', 'Tubores', 26),
        ('pueblo', 'San Pedro de Coche', 'Villalba', 27);
        
        INSERT OR IGNORE INTO operadora_prefijos (prefijo, operadora) VALUES
        ('412', 'Digitel'), ('422', 'Digitel'),
        ('414', 'Movistar'), ('424', 'Movistar'),
        ('416', 'Movilnet'), ('426', 'Movilnet');
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

    # Migration: add missing columns to existing databases
    conn = _get_connection()
    cursor = conn.cursor()
    for stmt in (
        "ALTER TABLE funcionarios ADD COLUMN activo INTEGER DEFAULT 1",
        "ALTER TABLE funcionarios ADD COLUMN posee_vivienda TEXT",
        "ALTER TABLE funcionarios ADD COLUMN tenencia_tierra_otra TEXT",
        "ALTER TABLE funcionarios ADD COLUMN ingreso_trabajador TEXT DEFAULT '0'",
        "ALTER TABLE funcionarios ADD COLUMN ingreso_familiar_adicional TEXT DEFAULT '0'",
        "ALTER TABLE funcionarios ADD COLUMN total_ingreso_familiar TEXT DEFAULT '0'",
        "ALTER TABLE funcionarios ADD COLUMN egreso_grupo_familiar TEXT DEFAULT '0'",
        "ALTER TABLE funcionarios ADD COLUMN disponibilidad_economica TEXT DEFAULT '0'",
        "ALTER TABLE funcionarios ADD COLUMN operadora TEXT",
        "ALTER TABLE funcionarios ADD COLUMN genero TEXT",
        "ALTER TABLE funcionarios ADD COLUMN residencia_municipio TEXT",
        "ALTER TABLE funcionarios ADD COLUMN residencia_pueblo TEXT",
        "ALTER TABLE funcionarios ADD COLUMN municipio TEXT",
        "ALTER TABLE funcionarios ADD COLUMN pueblo TEXT",
        """CREATE TABLE IF NOT EXISTS egresos_mensuales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_cedula TEXT REFERENCES funcionarios(cedula),
            rubro TEXT NOT NULL,
            monto TEXT DEFAULT '0',
            observacion TEXT DEFAULT ''
        )""",
        "CREATE TABLE IF NOT EXISTS catalogos (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT NOT NULL, valor TEXT NOT NULL, detalle TEXT DEFAULT '', orden INTEGER DEFAULT 0, activo INTEGER DEFAULT 1, UNIQUE(tipo, valor))",
        "CREATE TABLE IF NOT EXISTS operadora_prefijos (prefijo TEXT PRIMARY KEY, operadora TEXT NOT NULL)"
    ):
        try:
            cursor.execute(stmt)
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


# Rubros fijos de la distribución del ingreso familiar
RUBROS_EGRESO = [
    "Vivienda propia", "Alquiler", "Alimentación", "Condominio",
    "Luz", "Agua", "Teléfono", "Gas", "Transporte",
    "Enseres personales", "Educación", "Medicina",
    "Capacidad de ahorro", "Compras a créditos", "Otros",
]


def _parse_monto(valor):
    try:
        return float(str(valor or "0").replace(",", "").strip() or 0)
    except (ValueError, TypeError):
        return 0.0


def calcular_balance(ingreso_trabajador, ingreso_familiar_adicional, egresos):
    """Retorna (total_ingreso, egreso_total, disponibilidad). egresos: lista de montos o dicts."""
    total_ingreso = _parse_monto(ingreso_trabajador) + _parse_monto(ingreso_familiar_adicional)
    egreso_total = 0.0
    for e in egresos:
        monto = e.get("monto", 0) if isinstance(e, dict) else e
        egreso_total += _parse_monto(monto)
    disponibilidad = total_ingreso - egreso_total
    return total_ingreso, egreso_total, disponibilidad


def cargar_egresos(cedula):
    """Lista de dicts {rubro, monto, observacion} para un funcionario (vacío si no hay)."""
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT rubro, monto, observacion FROM egresos_mensuales WHERE funcionario_cedula = ? ORDER BY id",
        (cedula,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"rubro": r["rubro"], "monto": r["monto"] or "0",
             "observacion": r["observacion"] or ""} for r in rows]


def _guardar_egresos_cursor(cursor, cedula, egresos):
    """Reemplaza egresos usando un cursor existente (evita bloqueo de BD)."""
    cursor.execute("DELETE FROM egresos_mensuales WHERE funcionario_cedula = ?", (cedula,))
    for e in egresos:
        cursor.execute(
            "INSERT INTO egresos_mensuales (funcionario_cedula, rubro, monto, observacion) VALUES (?, ?, ?, ?)",
            (cedula, e.get("rubro", ""), str(e.get("monto", "0") or "0"),
             e.get("observacion", "") or ""),
        )


def guardar_egresos(cedula, egresos):
    """Reemplaza todos los egresos del funcionario. egresos: lista de dicts {rubro, monto, observacion}."""
    _crear_tablas()
    conn = _get_connection()
    cursor = conn.cursor()
    _guardar_egresos_cursor(cursor, cedula, egresos)
    conn.commit()
    conn.close()


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
        self.residencia_municipio = ""
        self.residencia_pueblo = ""
        self.operadora = ""
        self.genero = ""
        self.grupo_familiar = []
        self.activo = 1
        # Atributos opcionales con valor por defecto para evitar AttributeError
        self.jerarquia = ""
        self.lugar_presta_servicio = ""
        self.tiempo_servicio = ""
        self.salario_mensual = ""
        self.terreno_propio = ""
        self.ubicacion_terreno = ""
        self.condicion_vivienda = ""
        self.municipio = ""
        self.pueblo = ""
        self.necesidad_vivienda = ""
        self.organismo_publico = ""
        self.organismo_privado = ""
        self.gestion_organismo_oficial = ""
        self.fecha_gestion = ""
        self.posee_vivienda = ""
        self.tenencia_tierra = ""
        self.tenencia_tierra_otra = ""
        self.ambiente_vivienda = ""
        self.tiempo_ocupacion = ""
        self.servicio_vivienda_disponible = ""
        self.materiales_vivienda = ""
        self.servicio_comunidad = ""
        self.ingreso_trabajador = "0"
        self.ingreso_familiar_adicional = "0"
        self.total_ingreso_familiar = "0"
        self.egreso_grupo_familiar = "0"
        self.disponibilidad_economica = "0"
        self.egresos_mensuales = []

    def balance_socioeconomico(self, ingreso_trabajador, ingreso_familiar_adicional,
                               total_ingreso_familiar, egreso_grupo_familiar,
                               disponibilidad_economica, egresos=None):
        self.ingreso_trabajador = ingreso_trabajador or "0"
        self.ingreso_familiar_adicional = ingreso_familiar_adicional or "0"
        self.total_ingreso_familiar = total_ingreso_familiar or "0"
        self.egreso_grupo_familiar = egreso_grupo_familiar or "0"
        self.disponibilidad_economica = disponibilidad_economica or "0"
        if egresos is not None:
            self.egresos_mensuales = list(egresos)

    def agregar_familiar(self, familiar):
        self.grupo_familiar.append(familiar)

    def datos_laborales(self, jerarquia, lugar_presta_servicio, tiempo_servicio, salario_mensual):
        self.jerarquia = jerarquia
        self.lugar_presta_servicio = lugar_presta_servicio
        self.tiempo_servicio = tiempo_servicio
        self.salario_mensual = salario_mensual

    def plan_vivienda(self, terreno_propio, ubicacion_terreno, condicion_vivienda, municipio, pueblo, necesidad_vivienda, organismo_publico, organismo_privado, gestion_organismo_oficial, fecha_gestion):
        self.terreno_propio = terreno_propio
        self.ubicacion_terreno = ubicacion_terreno
        self.condicion_vivienda = condicion_vivienda
        self.municipio = municipio
        self.pueblo = pueblo
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
        f.activo = row["activo"]
        f.residencia_municipio = row["residencia_municipio"] or ""
        f.residencia_pueblo = row["residencia_pueblo"] or ""
        f.datos_laborales(
            row["jerarquia"] or "", row["lugar_presta_servicio"] or "",
            row["tiempo_servicio"] or "", row["salario_mensual"] or ""
        )
        f.plan_vivienda(
            row["terreno_propio"] or "", row["ubicacion_terreno"] or "",
            row["condicion_vivienda"] or "", row["municipio"] or "", row["pueblo"] or "",
            row["necesidad_vivienda"] or "", row["organismo_publico"] or "",
            row["organismo_privado"] or "", row["gestion_organismo_oficial"] or "",
            row["fecha_gestion"] or ""
        )
        f.estado_vivienda(
            row["tenencia_tierra"] or "", row["ambiente_vivienda"] or "",
            row["tiempo_ocupacion"] or "", row["servicio_vivienda_disponible"] or "",
            row["materiales_vivienda"] or "", row["servicio_comunidad"] or ""
        )
        f.posee_vivienda = row["posee_vivienda"] or "" if "posee_vivienda" in row.keys() else ""
        f.tenencia_tierra_otra = row["tenencia_tierra_otra"] or "" if "tenencia_tierra_otra" in row.keys() else ""
        f.operadora = row["operadora"] or "" if "operadora" in row.keys() else ""
        f.genero = row["genero"] or "" if "genero" in row.keys() else ""
        keys = row.keys()
        f.ingreso_trabajador = (row["ingreso_trabajador"] or "0") if "ingreso_trabajador" in keys else "0"
        f.ingreso_familiar_adicional = (row["ingreso_familiar_adicional"] or "0") if "ingreso_familiar_adicional" in keys else "0"
        f.total_ingreso_familiar = (row["total_ingreso_familiar"] or "0") if "total_ingreso_familiar" in keys else "0"
        f.egreso_grupo_familiar = (row["egreso_grupo_familiar"] or "0") if "egreso_grupo_familiar" in keys else "0"
        f.disponibilidad_economica = (row["disponibilidad_economica"] or "0") if "disponibilidad_economica" in keys else "0"
        cursor.execute(
            "SELECT rubro, monto, observacion FROM egresos_mensuales WHERE funcionario_cedula = ? ORDER BY id",
            (f.cedula,),
        )
        f.egresos_mensuales = [
            {"rubro": r["rubro"], "monto": r["monto"] or "0", "observacion": r["observacion"] or ""}
            for r in cursor.fetchall()
        ]

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
        activo_val = existing["activo"] if existing else getattr(f, "activo", 1)
        cursor.execute("""
            INSERT OR REPLACE INTO funcionarios (
                cedula, nombre, apellido, fecha_nacimiento, edad, telefono, operadora, genero, peso, altura,
                estado_civil, residencia, residencia_municipio, residencia_pueblo,
                jerarquia, lugar_presta_servicio, tiempo_servicio,
                salario_mensual, terreno_propio, ubicacion_terreno, condicion_vivienda, municipio, pueblo,
                necesidad_vivienda, organismo_publico, organismo_privado,
                gestion_organismo_oficial, fecha_gestion, tenencia_tierra, ambiente_vivienda,
                tiempo_ocupacion, servicio_vivienda_disponible, materiales_vivienda, servicio_comunidad,
                posee_vivienda, tenencia_tierra_otra,
                ingreso_trabajador, ingreso_familiar_adicional, total_ingreso_familiar,
                egreso_grupo_familiar, disponibilidad_economica,
                activo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f.cedula, f.nombre, f.apellido, f.fecha_nacimiento, f.edad, f.telefono, getattr(f, "operadora", ""), getattr(f, "genero", ""), f.peso,
            f.altura, f.estado_civil, f.residencia,
            getattr(f, "residencia_municipio", "") or "", getattr(f, "residencia_pueblo", "") or "",
            getattr(f, "jerarquia", None), getattr(f, "lugar_presta_servicio", None),
            getattr(f, "tiempo_servicio", None), getattr(f, "salario_mensual", None),
            getattr(f, "terreno_propio", None), getattr(f, "ubicacion_terreno", None),
            getattr(f, "condicion_vivienda", None), getattr(f, "municipio", None), getattr(f, "pueblo", None),
            getattr(f, "necesidad_vivienda", None),
            getattr(f, "organismo_publico", None), getattr(f, "organismo_privado", None),
            getattr(f, "gestion_organismo_oficial", None), getattr(f, "fecha_gestion", None),
            getattr(f, "tenencia_tierra", None), getattr(f, "ambiente_vivienda", None),
            getattr(f, "tiempo_ocupacion", None), getattr(f, "servicio_vivienda_disponible", None),
            getattr(f, "materiales_vivienda", None), getattr(f, "servicio_comunidad", None),
            getattr(f, "posee_vivienda", None), getattr(f, "tenencia_tierra_otra", None),
            getattr(f, "ingreso_trabajador", "0") or "0",
            getattr(f, "ingreso_familiar_adicional", "0") or "0",
            getattr(f, "total_ingreso_familiar", "0") or "0",
            getattr(f, "egreso_grupo_familiar", "0") or "0",
            getattr(f, "disponibilidad_economica", "0") or "0",
            activo_val,
        ))

        egresos = getattr(f, "egresos_mensuales", None)
        if egresos is not None:
            _guardar_egresos_cursor(cursor, f.cedula, egresos)

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



# --- Catálogos y Operadoras ---

def cargar_catalogo(tipo):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT valor, detalle FROM catalogos WHERE tipo = ? AND activo = 1 ORDER BY orden", (tipo,))
    return [{"valor": r["valor"], "detalle": r["detalle"]} for r in cursor.fetchall()]

def valores_catalogo(tipo):
    return [r["valor"] for r in cargar_catalogo(tipo)]

def detalle_de_lugar(valor):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT detalle FROM catalogos WHERE tipo = 'lugar_servicio' AND valor = ?", (valor,))
    res = cursor.fetchone()
    conn.close()
    return res["detalle"] if res else valor

def lugar_por_detalle(detalle):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM catalogos WHERE tipo = 'lugar_servicio' AND detalle = ?", (detalle,))
    res = cursor.fetchone()
    conn.close()
    return res["valor"] if res else detalle

def agregar_catalogo(tipo, valor, detalle=""):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(orden), 0) + 1 FROM catalogos WHERE tipo = ?", (tipo,))
    orden = cursor.fetchone()[0]
    cursor.execute("INSERT INTO catalogos (tipo, valor, detalle, orden) VALUES (?, ?, ?, ?)",
                   (tipo, valor, detalle, orden))
    conn.commit()
    conn.close()

def eliminar_catalogo(tipo, valor):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM catalogos WHERE tipo = ? AND valor = ?", (tipo, valor))
    conn.commit()
    conn.close()


# --- Normalizacion de cedula y telefono ---

def solo_digitos(valor):
    return "".join(c for c in str(valor or "") if c.isdigit())

def normalizar_cedula(valor):
    """Devuelve 'V-<hasta 8 digitos>' o '' si no hay digitos."""
    digitos = solo_digitos(valor)[:8]
    return f"V-{digitos}" if digitos else ""

def dividir_telefono(valor):
    """Separa (prefijo, abonado) de formatos 0412..., +58..., 412...
    Devuelve ('', '') si no hay digitos."""
    d = solo_digitos(valor)
    if d.startswith("58") and len(d) >= 12:
        d = d[2:]
    if len(d) == 11 and d.startswith("0"):
        d = d[1:]
    if len(d) >= 10:
        return d[:3], d[-7:]
    return "", d

def operadora_de_telefono(telefono):
    tel = "".join(filter(str.isdigit, telefono))
    if len(tel) >= 3:
        if tel.startswith("58"): tel = tel[2:]
        elif tel.startswith("0"): tel = tel[1:]
        prefijo = tel[0:3]
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT operadora FROM operadora_prefijos WHERE prefijo = ?", (prefijo,))
        res = cursor.fetchone()
        conn.close()
        return res["operadora"] if res else ""
    return ""

def cargar_operadoras():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prefijo, operadora FROM operadora_prefijos")
    return [{"prefijo": r["prefijo"], "operadora": r["operadora"]} for r in cursor.fetchall()]

def agregar_operadora(prefijo, operadora):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO operadora_prefijos (prefijo, operadora) VALUES (?, ?)", (prefijo, operadora))
    conn.commit()
    conn.close()

def eliminar_operadora(prefijo):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM operadora_prefijos WHERE prefijo = ?", (prefijo,))
    conn.commit()
    conn.close()


ROLES = {
    "viewer": {"ver": True, "crear": False, "modificar": False, "eliminar": False},
    "editor": {"ver": True, "crear": True, "modificar": False, "eliminar": False},
    "modifier": {"ver": True, "crear": True, "modificar": True, "eliminar": False},
    "subadmin": {"ver": True, "crear": True, "modificar": True, "eliminar": True},
    "admin": {"ver": True, "crear": True, "modificar": True, "eliminar": True},
}
