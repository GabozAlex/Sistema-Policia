# Sistema de Bienestar y Protección Social — Gestión Policial

Aplicación de escritorio para el registro y gestión de funcionarios policiales, desarrollada con Python 3 y Tkinter. Permite administrar datos personales, laborales, de vivienda y grupo familiar de cada funcionario, con control de acceso por roles, auditoría de acciones y exportación de fichas.

## ¿Por qué este programa?

Este sistema nace de la necesidad de digitalizar y centralizar la información socioeconómica de los funcionarios policiales. Originalmente los datos se manejaban en planillas físicas y archivos dispersos, lo que dificultaba la consulta, actualización y generación de reportes. El programa busca:

- Unificar en un solo lugar todos los datos relevantes del funcionario (personales, laborales, vivienda, familia).
- Facilitar la búsqueda y consulta rápida de información.
- Controlar el acceso según el rol del usuario para proteger la información sensible.
- Llevar un registro de auditoría de todas las acciones realizadas.
- Permitir la exportación de fichas individuales para trámites o reportes.

## Funcionalidades

### Gestión de Funcionarios
- **Registro**: formulario con pestañas para datos personales, laborales, plan de vivienda, estado de la vivienda y grupo familiar.
- **Consulta**: tabla con búsqueda por cédula, nombre o apellido.
- **Modificación**: edición completa de cualquier funcionario existente.
- **Desactivación/Restauración**: eliminación lógica (soft delete) que oculta el registro sin perder los datos. Posibilidad de restaurarlo.

### Roles de Usuario
| Rol | Permisos |
|-----|----------|
| Visor | Solo lectura |
| Editor | Ver y crear |
| Modificador | Ver, crear y modificar |
| SubAdmin | Ver, crear, modificar, desactivar, restaurar y ver auditoría |
| Admin | Acceso total (incluye gestión de usuarios) |

### Vistas del Sistema
- **Inicio**: listado de todos los funcionarios con filtro de activos/inactivos.
- **Ver Datos**: ficha completa con scroll, organizada por secciones.
- **Registrar/Editar**: formulario con 5 pestañas.
- **Auditoría**: registro cronológico de todas las acciones (admin y subadmin).
- **Gestión de Usuarios**: alta y baja de cuentas de usuario (solo admin).

### Exportación
Desde la ficha de cada funcionario:
- **Imprimir**: envía a impresora del sistema (vía `lpr` en Linux, `notepad /p` en Windows).
- **Exportar PDF**: genera un PDF con todos los datos del funcionario.
- **Guardar TXT**: guarda un archivo de texto plano.

### Seguridad
- Inicio de sesión obligatorio con usuario y contraseña.
- Roles con permisos granulares (ver, crear, modificar, eliminar).
- Auditoría de todas las acciones: creación, modificación, desactivación.
- Eliminación lógica: los datos nunca se pierden, solo se ocultan.

### Otras Características
- Edad auto-calculada a partir de la fecha de nacimiento.
- Selectores de fecha con combo de día/mes/año.
- Checkboxes y radios para datos estructurados.
- Modo de prueba con base de datos separada (`DB_MODE=test`).
- Interfaz moderna con ttk tema "clam", sidebar con iconos y hover.

## Tecnologías

- **Python 3.10+**
- **Tkinter** (ttk, tema "clam")
- **SQLite 3** (base de datos embebida)
- **fpdf2** (generación de PDF)

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Sistema-Policia

# Instalar dependencias
pip install fpdf2

# Ejecutar
python3 src/ui.py
```

### Modo de Prueba

Usa una base de datos separada para no afectar los datos reales:

```bash
DB_MODE=test python3 src/ui.py
```

## Estructura del Proyecto

```
Sistema-Policia/
├── src/
│   ├── ui.py              # Interfaz gráfica (Tkinter)
│   ├── logic.py           # Lógica de negocio, DB, modelos, roles
│   └── data/
│       ├── funcionarios.db           # Base de datos producción
│       └── funcionarios_prueba.db    # Base de datos prueba
├── USUARIOS.txt            # Credenciales de usuarios preconfigurados
└── README.md
```

## Usuarios Preconfigurados

Los siguientes usuarios se crean automáticamente al iniciar el programa por primera vez (ver `USUARIOS.txt` para credenciales completas):

- `visor` — Solo lectura
- `editor` — Ver y crear
- `modificador` — Ver, crear y modificar
- `subadmin` — Sub-administrador
- `admin` — Acceso total

## Licencia

Uso interno. Desarrollado para la gestión de bienestar social de funcionarios policiales.
