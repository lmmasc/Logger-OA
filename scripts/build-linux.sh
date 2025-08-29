#!/bin/bash
# Script para generar el ejecutable en Linux

cd "$(dirname "$0")/.."
.venv-linux/bin/pyinstaller src/main.py --onefile --name LoggerOA --icon=assets/app_icon.png
