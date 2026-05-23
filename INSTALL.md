# Guía de Instalación para Windows 10

## Requisitos

- Windows 10 (64 bits)
- Conexión a internet
- Cuenta con permisos de administrador (solo para instalar Python)

---

## Paso 1: Instalar Python

1. Ve a https://www.python.org/downloads/
2. Descarga la última versión de Python 3 (ej: Python 3.12 o 3.13)
3. Ejecuta el instalador
4. **IMPORTANTE**: Marca la casilla **"Add Python to PATH"** al inicio
5. Haz clic en **"Install Now"** y espera a que termine

Para verificar que quedó bien instalado:
- Abre **Símbolo del sistema** (cmd)
- Escribe: `python --version`
- Debe mostrar algo como: `Python 3.12.x`

---

## Paso 2: Descargar el Programa

Abre el Símbolo del sistema y escribe:

```cmd
cd C:\
git clone https://github.com/GabozAlex/Sistema-Policia.git
```

Si no tienes `git` instalado:
1. Descarga el ZIP desde https://github.com/GabozAlex/Sistema-Policia
2. Extrae la carpeta en `C:\Sistema-Policia`

---

## Paso 3: Instalar Dependencia

En el Símbolo del sistema:

```cmd
pip install fpdf2
```

Si aparece un error, prueba con:

```cmd
python -m pip install fpdf2
```

---

## Paso 4: Ejecutar el Programa

```cmd
cd C:\Sistema-Policia
python src\ui.py
```

---

## Modo de Prueba

Si quieres usar una base de datos separada para hacer pruebas:

```cmd
cd C:\Sistema-Policia
set DB_MODE=test
python src\ui.py
```

Para volver al modo normal, cierra y vuelve a abrir el cmd antes de ejecutar.

---

## Usuarios del Sistema

Al ejecutar por primera vez se crean automáticamente estos usuarios:

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| visor | visor123 | Solo lectura |
| editor | editor123 | Ver y crear |
| modificador | mod123 | Ver, crear y modificar |
| subadmin | sub123 | Sub-administrador |
| admin | admin123 | Acceso total |

---

## Solución de Problemas

**"python no se reconoce como un comando"**
→ No marcaste "Add Python to PATH". Reinstala Python y asegúrate de marcar esa casilla.

**"pip no se reconoce como un comando"**
→ Prueba con `python -m pip` en lugar de `pip`.

**Error de importación "No module named 'fpdf'"**
→ Falta instalar fpdf2. Ejecuta `pip install fpdf2` nuevamente.

**La ventana se abre y se cierra inmediatamente**
→ Ejecuta desde el Símbolo del sistema para ver el mensaje de error.

---

## Crear un Acceso Directo (Opcional)

1. Crea un archivo de texto en el escritorio llamado `Sistema-Policia.bat`
2. Edítalo y pega:
```bat
@echo off
cd /d C:\Sistema-Policia
python src\ui.py
pause
```
3. Guarda el archivo. Al hacer doble clic se abrirá el programa.

---

## Opcional: Crear un Ejecutable Portable (.exe)

Si quieres llevar el programa a cualquier PC **sin instalar Python**:

1. En la PC con Windows, abre el Símbolo del sistema en la carpeta del proyecto
2. Ejecuta:
```cmd
build.bat
```
3. Esto instalará PyInstaller y generará `dist\SistemaPolicia.exe`
4. Ese .exe funciona en cualquier Windows 10 sin necesidad de Python ni dependencias

## Opcional: Crear un Instalador

Después de generar el .exe con el paso anterior:

1. Descarga e instala **Inno Setup** desde https://jrsoftware.org/isinfo.php
2. Abre el archivo `installer.iss` incluido en el proyecto
3. Haz clic en **Build → Compile**
4. El instalador se generará en la carpeta `installer\`

El instalador crea acceso directo en el escritorio y menú inicio, y permite desinstalar desde "Agregar o quitar programas" de Windows.
