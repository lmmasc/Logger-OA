#!/bin/bash
# Script para generar el ejecutable en Mac

cd "$(dirname "$0")/.."
rm -f LoggerOA.spec
rm -rf build dist *.spec
# Incluir recursos y módulos necesarios en el binario
.venv-mac/bin/pyinstaller src/main.py \
  --name LoggerOA \
  --windowed \
  --onefile \
  --noconfirm \
  --icon=assets/app_icon.icns \
  --name LoggerOA \
  --paths src \
  --add-data "assets:assets" \
  --add-data "src/config:src/config" \
  --add-data "src/domain:src/domain" \
  --add-data "src/infrastructure:src/infrastructure" \
  --add-data "src/interface_adapters:src/interface_adapters" \
  --add-data "src/interface_adapters/ui/themes:src/interface_adapters/ui/themes" \
  --add-data "src/interface_adapters/ui/views:src/interface_adapters/ui/views" \
  --add-data "src/application:src/application" \
  --add-data "src/utils:src/utils" \
  --add-data "src/translation:src/translation" \
  --add-data "src/main.py:src/main.py" \
  --hidden-import PySide6 \
  --hidden-import shiboken6 \
  --hidden-import translation.es.all_keys \
  --hidden-import translation.en.all_keys \
