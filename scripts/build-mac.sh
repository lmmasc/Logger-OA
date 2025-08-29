#!/bin/bash
# Script para generar el ejecutable en Mac

cd "$(dirname "$0")/.."
.venv-mac/bin/pyinstaller src/main.py --onefile --name LoggerOA --icon=assets/app_icon.icns
