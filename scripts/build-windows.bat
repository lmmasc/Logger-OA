@echo off
REM Script para generar el ejecutable en Windows

cd /d %~dp0\..
.venv-windows\Scripts\pyinstaller src\main.py --onefile --name LoggerOA --icon=assets\app_icon.ico
