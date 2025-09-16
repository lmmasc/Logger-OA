@echo off
REM Script para generar el ejecutable en Windows

cd /d %~dp0\..
del /F LoggerOA.spec
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
  --hidden-import translation.es.ui ^
  --hidden-import translation.es.menu ^
  --hidden-import translation.es.log_ops ^
  --hidden-import translation.es.log_contest ^
  --hidden-import translation.es.table_headers ^
  --hidden-import translation.es.messages ^
  --hidden-import translation.es.forms ^
  --hidden-import translation.es.operator ^
  --hidden-import translation.es.import_summary ^
  --hidden-import translation.en.ui ^
  --hidden-import translation.en.menu ^
  --hidden-import translation.en.log_ops ^
  --hidden-import translation.en.log_contest ^
  --hidden-import translation.en.table_headers ^
  --hidden-import translation.en.messages ^
  --hidden-import translation.en.forms ^
  --hidden-import translation.en.operator ^
  --hidden-import translation.en.import_summary ^
