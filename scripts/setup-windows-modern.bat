@echo off
REM Crea o actualiza el entorno virtual moderno en .venv.

cd /d %~dp0\..

set PYTHON_CMD=%~1
if "%PYTHON_CMD%"=="" set PYTHON_CMD=python

%PYTHON_CMD% -m venv .venv
if errorlevel 1 exit /b %errorlevel%

.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 exit /b %errorlevel%

.venv\Scripts\python.exe -m pip install -r requirements-dev-modern.txt
exit /b %errorlevel%