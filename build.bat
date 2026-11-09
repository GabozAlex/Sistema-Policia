@echo off
REM ============================================
REM Script para generar el ejecutable de
REM Sistema de Bienestar y Proteccion Social
REM ============================================
cd /d "%~dp0"
title Generando ejecutable de SistemaPolicia...

echo [1/3] Instalando dependencias...
pip install pyinstaller fpdf2 Pillow

echo.
echo [2/3] Generando ejecutable...
set ICON_ARG=
if exist "src\assets\icons\app.ico" set ICON_ARG=--icon "src\assets\icons\app.ico"
pyinstaller --onefile --noconsole --name "SistemaPolicia" --add-data "src\assets;assets" %ICON_ARG% src/ui.py

echo.
echo [3/3] Listo!
echo ============================================
echo Ejecutable creado en: dist\SistemaPolicia.exe
echo La base de datos se crea automaticamente
echo al abrir el programa por primera vez.
echo ============================================
pause
