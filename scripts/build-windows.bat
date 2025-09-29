@echo off
REM Script para generar el ejecutable en Windows

cd /d %~dp0\..
del /F LoggerOA.spec
REM Generar src\version.py desde git (fallback a 0.0.0-dev)
for /f "delims=" %%a in ('git describe --tags --always --dirty 2^>NUL') do set GIT_VERSION=%%a
if "%GIT_VERSION%"=="" set GIT_VERSION=0.0.0-dev
(
  echo APP_NAME = "Logger OA"
  echo APP_VERSION = "%GIT_VERSION%"
) > src\version.py

.venv-windows\Scripts\pyinstaller src\main.py ^
  --windowed ^
  --onefile ^
  --name LoggerOA ^
  --icon=assets\app_icon.ico ^
  --paths src ^
  --add-data "assets;assets" ^
  --add-data "src/config;src/config" ^
  --add-data "src/domain;src/domain" ^
  --add-data "src/infrastructure;src/infrastructure" ^
  --add-data "src/interface_adapters;src/interface_adapters" ^
  --add-data "src/interface_adapters/ui/themes;src/interface_adapters/ui/themes" ^
  --add-data "src/interface_adapters/ui/views;src/interface_adapters/ui/views" ^
  --add-data "src/application;src/application" ^
  --add-data "src/utils;src/utils" ^
  --add-data "src/translation;src/translation" ^
  --add-data "src/main.py;src/main.py" ^
  --hidden-import PySide6 ^
  --hidden-import shiboken6 ^
  --hidden-import translation.es.all_keys ^
  --hidden-import translation.en.all_keys ^
