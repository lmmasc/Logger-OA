@echo off
REM Script para generar el ejecutable legacy de Windows 7 x86.

cd /d %~dp0\..

if not exist .venv-win7-x86\Scripts\python.exe (
  echo No existe .venv-win7-x86. Ejecuta antes scripts\setup-windows-legacy.bat C:\Python38-32\python.exe
  exit /b 1
)

.venv-win7-x86\Scripts\python.exe -c "import platform, struct, sys; assert sys.version_info[:2] == (3, 8), 'El entorno legacy debe usar Python 3.8'; assert struct.calcsize('P') * 8 == 32, 'El entorno legacy debe ser de 32 bits'; print('Build legacy con:', platform.python_version(), struct.calcsize('P') * 8)"
if errorlevel 1 exit /b %errorlevel%

REM Generar src\version.py desde git (fallback a 0.0.0-dev)
for /f "delims=" %%a in ('git describe --tags --always --dirty 2^>NUL') do set GIT_VERSION=%%a
if "%GIT_VERSION%"=="" set GIT_VERSION=0.0.0-dev
(
  echo APP_NAME = "Logger OA"
  echo APP_VERSION = "%GIT_VERSION%"
) > src\version.py

if exist dist\LoggerOA-win7-x86.exe del /f /q dist\LoggerOA-win7-x86.exe
if exist dist\LoggerOA-win7-x86 rmdir /s /q dist\LoggerOA-win7-x86

.venv-win7-x86\Scripts\python.exe -m PyInstaller --noconfirm LoggerOA.win7-x86.spec
if errorlevel 1 exit /b %errorlevel%

echo Build legacy generado en dist\LoggerOA-win7-x86.exe