@echo off
REM Crea o actualiza el entorno virtual legacy para Windows 7 x86 en .venv-win7-x86.
REM Uso: scripts\setup-windows-legacy.bat C:\Python38-32\python.exe

cd /d %~dp0\..

set PYTHON_CMD=%~1
if "%PYTHON_CMD%"=="" (
  echo Debes indicar el ejecutable de Python 3.8 x86.
  echo Ejemplo: scripts\setup-windows-legacy.bat C:\Python38-32\python.exe
  exit /b 1
)

%PYTHON_CMD% -c "import platform, struct, sys; assert sys.version_info[:2] == (3, 8), 'Se requiere Python 3.8'; assert struct.calcsize('P') * 8 == 32, 'Se requiere Python de 32 bits'; print('Python legacy valido:', platform.python_version(), struct.calcsize('P') * 8)"
if errorlevel 1 exit /b %errorlevel%

%PYTHON_CMD% -m venv .venv-win7-x86
if errorlevel 1 exit /b %errorlevel%

.venv-win7-x86\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 exit /b %errorlevel%

.venv-win7-x86\Scripts\python.exe -m pip install -r requirements-dev-legacy.txt
exit /b %errorlevel%