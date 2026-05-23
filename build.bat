@echo off
REM ============================================
REM Script para generar el ejecutable de
REM Sistema de Bienestar y Proteccion Social
REM ============================================
title Generando ejecutable de SistemaPolicia...

echo [1/3] Instalando dependencias...
pip install pyinstaller fpdf2

echo.
echo [2/3] Generando ejecutable...
pyinstaller --onefile --noconsole --name "SistemaPolicia" src/ui.py

echo.
echo [3/3] Listo!
echo ============================================
echo Ejecutable creado en: dist\SistemaPolicia.exe
echo La base de datos se crea automaticamente
echo al abrir el programa por primera vez.
echo ============================================
pause
