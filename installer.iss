; Script de Inno Setup para Sistema de Bienestar y Proteccion Social
; 1. Genera el .exe con build.bat (necesitas PyInstaller)
; 2. Abre este archivo con Inno Setup (https://jrsoftware.org/isinfo.php)
; 3. Compila y genera el instalador

[Setup]
AppName=Sistema de Bienestar y Proteccion Social
AppVersion=1.0
AppPublisher=GabozAlex
DefaultDirName={pf}\SistemaPolicia
DefaultGroupName=SistemaPolicia
UninstallDisplayIcon={app}\SistemaPolicia.exe
OutputDir=installer
OutputBaseFileName=Instalador_SistemaPolicia
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\SistemaPolicia.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SistemaPolicia"; Filename: "{app}\SistemaPolicia.exe"
Name: "{commondesktop}\SistemaPolicia"; Filename: "{app}\SistemaPolicia.exe"

[Run]
Filename: "{app}\SistemaPolicia.exe"; Description: "Ejecutar el programa"; Flags: postinstall nowait skipifsilent
