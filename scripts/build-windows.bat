@echo off
REM Script para generar el ejecutable en Windows

cd /d %~dp0\..

if not exist .venv\Scripts\python.exe (
  echo No existe .venv. Ejecuta antes scripts\setup-windows-modern.bat
  exit /b 1
)

.venv\Scripts\python.exe -c "import platform, struct, sys; print('Build moderno con:', platform.python_version(), struct.calcsize('P') * 8)"
if errorlevel 1 exit /b %errorlevel%

REM Generar src\version.py desde git (fallback a 0.0.0-dev)
for /f "delims=" %%a in ('git describe --tags --always --dirty 2^>NUL') do set GIT_VERSION=%%a
if "%GIT_VERSION%"=="" set GIT_VERSION=0.0.0-dev
(
  echo APP_NAME = "Logger OA"
  echo APP_VERSION = "%GIT_VERSION%"
) > src\version.py

if exist dist\LoggerOA.exe del /f /q dist\LoggerOA.exe
if exist build\LoggerOA rmdir /s /q build\LoggerOA

.venv\Scripts\pyinstaller --noconfirm LoggerOA.spec
if errorlevel 1 exit /b %errorlevel%

echo Build moderno generado en dist\LoggerOA.exe
