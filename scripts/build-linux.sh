#!/bin/bash
# Script para generar el ejecutable en Linux

set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/python ]; then
  echo "No existe .venv. Crea antes el entorno moderno e instala requirements-dev-modern.txt"
  exit 1
fi

.venv/bin/python -c "import platform, struct; print('Build Linux con:', platform.python_version(), struct.calcsize('P') * 8)"

# Generar version.py desde git (fallback a 0.0.0-dev)
GIT_VERSION=$(git describe --tags --always --dirty 2>/dev/null || echo "0.0.0-dev")
echo "APP_NAME = \"Logger OA\"" > src/version.py
echo "APP_VERSION = \"${GIT_VERSION}\"" >> src/version.py

rm -f dist/LoggerOA
rm -rf build/LoggerOA

# Incluir recursos y módulos necesarios en el binario Linux.
.venv/bin/pyinstaller src/main.py \
  --onefile \
  --name LoggerOA \
  --icon=assets/app_icon.png \
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
  --hidden-import translation.en.all_keys

echo "Build Linux generado en dist/LoggerOA"
