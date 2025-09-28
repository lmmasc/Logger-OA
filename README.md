
## Licencia y condiciones de uso

Este software se distribuye bajo la licencia MIT. Puedes copiarlo, modificarlo y crear tus propias versiones, siempre y cuando **menciones a los desarrolladores originales** en los créditos:

- Miguel OA4BAU
- Raquel OA4EHN

No se aceptan sugerencias ni mejoras en este repositorio oficial. Eres libre de crear y distribuir tus propias versiones, respetando la mención a los autores.

**Disclaimer:** Este software se proporciona "tal cual", sin garantías de ningún tipo, expresas o implícitas. Los autores no se hacen responsables por daños, pérdidas o cualquier consecuencia derivada del uso del software. Úsalo bajo tu propio riesgo.
# Logger OA

![PySide6](https://img.shields.io/badge/UI-PySide6-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

Aplicación de escritorio multiplataforma para la gestión de concursos y operaciones de radioaficionados OA (Perú), con arquitectura desacoplada, interfaz moderna y soporte para importación de datos desde múltiples formatos y países.

---

## Tabla de Contenidos
- [Características principales](#características-principales)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)
- [Testing](#testing)
- [Licencia](#licencia)
- [Créditos / Autoría](#créditos--autoría)

---

## Características principales
- Gestión de concursos y operaciones de radioaficionados OA.
- Base de datos local SQLite, sin dependencias externas.
- Importación automática de operadores desde listados oficiales en PDF (Perú, Uruguay), Excel (Argentina, Chile) o CSV.
- Feedback visual en importación: diálogo de espera traducido y resumen detallado (total, nuevos, actualizados, deshabilitados, rehabilitados).
- Interfaz gráfica moderna con PySide6 (Qt), temas claro/oscuro y cambio de idioma.
- Arquitectura desacoplada basada en Clean Architecture.
- Scripts de build para Linux, Windows y macOS.
- Internacionalización modular y extensible.
- Pruebas unitarias y de integración con pytest.

---

## Requisitos previos
- **Python** >= 3.10
- **pip**
- **Linux, Windows o macOS**
- Recomendado: entorno virtual (`venv`)

### Dependencias principales
- `PySide6>=6.9.2`
- `pdfplumber`
- `reportlab`
- `sqlite3` (incluida en Python)

### Dependencias de desarrollo
- `pyinstaller` (para generar ejecutables)

---

## Instalación

1. Clona el repositorio y accede a la carpeta del proyecto:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd "Logger OA v2"
   ```
2. Crea y activa el entorno virtual correspondiente (según tu sistema operativo). Los scripts de build requieren estos nombres específicos:

  **Linux:**
  ```bash
  python3 -m venv .venv-linux
  source .venv-linux/bin/activate
  ```

  **macOS:**
  ```bash
  python3 -m venv .venv-mac
  source .venv-mac/bin/activate
  ```

  **Windows (cmd):**
  ```cmd
  python -m venv .venv-windows
  .venv-windows\Scripts\activate
  ```

  **Windows (PowerShell):**
  ```powershell
  python -m venv .venv-windows
  .venv-windows\Scripts\Activate.ps1
  ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   # Para desarrollo:
   pip install -r requirements-dev.txt
   ```
4. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```

---

## Uso

### Ejecución desde consola
```bash
python src/main.py
```

### Ejemplo de uso como módulo
```python
from src.application.use_cases.update_operators_from_pdf import update_operators_from_pdf
resultado = update_operators_from_pdf('BaseDocs/396528-radioaficionados_autorizados_al_24sep2025.pdf')
print(resultado)
```


### Acceso al Manual de Usuario
El manual de usuario completo está disponible desde la propia aplicación, en el menú **Ayuda > Manual de uso**.

### Ejemplo práctico: Importar operadores OA desde PDF
1. Abre la aplicación.
2. Ve al menú "Base de datos > Importar > Importar desde PDF" y selecciona el archivo oficial.
3. Al finalizar, se muestra un resumen detallado (total, nuevos, actualizados, deshabilitados, rehabilitados).

---

## Estructura del proyecto

El proyecto sigue los principios de Clean Architecture, separando responsabilidades en capas bien definidas:

```text
src/
  main.py                  # Punto de entrada de la aplicación
  domain/                  # Entidades y lógica de negocio pura
    entities/              # Modelos de dominio (Operador, Concurso, Contacto, etc.)
    repositories/          # Interfaces de repositorios
    use_cases/             # Casos de uso del dominio
  application/             # Casos de uso y lógica de aplicación
    use_cases/             # Gestión, importación desde PDF, etc.
  infrastructure/          # Implementaciones técnicas
    db/                    # Acceso y gestión de base de datos SQLite
    pdf/                   # Extracción y procesamiento de PDF
    repositories/          # Repositorios concretos
  interface_adapters/      # Adaptadores de interfaz
    ui/                    # Interfaz gráfica (PySide6)
      views/               # Vistas principales (Welcome, LogOps, LogContest, DBTableWindow, etc.)
      dialogs/             # Diálogos y ventanas auxiliares (incl. feedback visual)
      themes/              # Temas visuales (claro/oscuro)
    controllers/           # Controladores de UI
  config/                  # Configuración, rutas y settings
  translation/             # Internacionalización y traducciones
  utils/                   # Utilidades puras
assets/                    # Recursos gráficos (iconos, GIFs, etc.)
BaseDocs/                  # Documentos oficiales OA (PDF)
scripts/                   # Scripts de build multiplataforma
  build-linux.sh           # Build para Linux
  build-mac.sh             # Build para macOS
  build-windows.bat        # Build para Windows
tests/                     # Pruebas unitarias y de integración
```

### Diagrama de Capas (Clean Architecture)

```
[ UI / Interface Adapters ] <--> [ Application ] <--> [ Domain ] <--> [ Infrastructure ]
```

---

## Internacionalización y Traducciones

El sistema de traducciones es modular y extensible. Los archivos de traducción se encuentran en `src/translation/<idioma>/` y están organizados por subdiccionarios en un archivo all_keys.py (`ALL_KEYS_TRANSLATIONS` `UI_TRANSLATIONS MENUS_TRANSLATIONS` `TABLE_HEADERS_TRANSLATIONS`), etc.).

Para agregar un nuevo idioma:
1. Crea una carpeta en `src/translation/` con el código del idioma (ej: `fr/` para francés).
2. Copia y adapta el archivo de traducción existente.
3. El loader central (`translations.py`) combinará automáticamente los módulos.

---

## Scripts de Build Multiplataforma

En la carpeta `scripts/` hay scripts para generar ejecutables en Linux, macOS y Windows usando PyInstaller:
- `build-linux.sh`
- `build-mac.sh`
- `build-windows.bat`

Ejecuta el script correspondiente para generar el ejecutable standalone.

---


## Testing

Las pruebas unitarias y de integración se encuentran en la carpeta `tests/` y utilizan `pytest`.

Para ejecutar todas las pruebas:
```bash
pytest
```

---

## Créditos / Autoría

### Autores
- Miguel OA4BAU
- Raquel OA4EHN

### Colaboradores
- Moises OA4EFJ 

