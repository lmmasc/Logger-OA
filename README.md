# Logger OA v2

Aplicación de escritorio multiplataforma para la gestión de concursos y operaciones de radioaficionados OA (Perú), con arquitectura desacoplada, interfaz moderna y soporte para importación de datos desde PDF.

---

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Características Principales](#características-principales)
- [Arquitectura y Estructura](#arquitectura-y-estructura)
- [Dependencias](#dependencias)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Guía de Uso](#guía-de-uso)
- [Licencia](#licencia)

---

## Descripción General
Logger OA v2 es una aplicación de escritorio para registrar, consultar y gestionar concursos y operaciones de radioaficionados OA (Perú). Permite llevar un control detallado de contactos, concursos, operadores y actividades, con soporte para temas claro/oscuro, persistencia en SQLite, importación de operadores desde PDF y una interfaz moderna basada en PySide6 (Qt).

---

## Características Principales
- **Gestión de concursos y operaciones**: Registro, consulta y exportación de logs.
- **Base de datos local**: Persistencia en SQLite, sin dependencias externas.
- **Importación desde PDF**: Extracción automática de operadores OA desde listados oficiales en PDF.
- **Feedback visual en importación**: Durante la importación desde PDF se muestra un diálogo de espera traducido y, al finalizar, un resumen detallado (total, nuevos, actualizados, deshabilitados, rehabilitados).
- **Interfaz moderna**: UI con PySide6, soporte para temas claro/oscuro y cambio de idioma (internacionalización).
- **Arquitectura desacoplada**: Basada en Clean Architecture para facilitar mantenimiento y escalabilidad.
- **Soporte multiplataforma**: Funciona en Linux, Windows y macOS.

---

## Arquitectura y Estructura
El proyecto sigue los principios de Clean Architecture, separando responsabilidades en capas bien definidas:

```
src/
  main.py                  # Punto de entrada de la aplicación
  domain/                  # Entidades y lógica de negocio pura
    entities/              # Modelos de dominio (Operador, Concurso, Contacto, etc.)
    repositories/          # Interfaces de repositorios
    use_cases/             # Casos de uso del dominio
  application/             # Casos de uso y lógica de aplicación
    use_cases/             # Casos de uso específicos (gestión, actualización, importación desde PDF, etc.)
  infrastructure/          # Implementaciones técnicas
    db/                    # Acceso y gestión de base de datos SQLite
    pdf/                   # Extracción y procesamiento de PDF
    repositories/          # Repositorios concretos
  interface_adapters/      # Adaptadores de interfaz
    ui/                    # Interfaz gráfica (PySide6)
      views/               # Vistas principales (Welcome, LogOps, LogContest, etc.)
      dialogs/             # Diálogos y ventanas auxiliares (incl. feedback visual)
      themes/              # Temas visuales (claro/oscuro)
    controllers/           # Controladores de UI
  config/                  # Configuración, rutas y settings
  translation/             # Internacionalización y traducciones
  utils/                   # Utilidades puras
assets/                    # Recursos gráficos (iconos, GIFs de feedback, etc.)
tests/                     # Pruebas unitarias y de integración
```

### Diagrama de Capas (Clean Architecture)

```
[ UI / Interface Adapters ] <--> [ Application ] <--> [ Domain ] <--> [ Infrastructure ]
```

---

## Modularización y Arquitectura de la UI

La interfaz gráfica principal (`MainWindow`) está dividida en módulos temáticos para facilitar el mantenimiento y la escalabilidad. Los archivos con prefijo `main_window_` agrupan la lógica de acciones, diálogos, configuración, gestión de vistas y ventanas secundarias:

```
interface_adapters/ui/
  main_window.py                  # Clase principal de la ventana
  main_window_actions.py          # Handlers de acciones del menú
  main_window_dialogs.py          # Diálogos personalizados
  main_window_config.py           # Configuración y actualización de UI
  main_window_view_management.py  # Gestión de vistas y navegación
  main_window_db_window.py        # Gestión de ventana de base de datos
```

---

## Dependencias

**Principales:**
- [PySide6](https://doc.qt.io/qtforpython/) (>=6.9.2): Interfaz gráfica Qt para Python.
- [pdfplumber](https://github.com/jsvine/pdfplumber): Extracción de datos desde PDF.
- [sqlite3](https://docs.python.org/3/library/sqlite3.html): Base de datos embebida (incluida en Python).

**Desarrollo:**
- pyinstaller: Generación de ejecutables standalone.

Instalación automática desde `requirements.txt` y `requirements-dev.txt`.

---

## Instalación y Ejecución

1. Clona el repositorio y accede a la carpeta del proyecto:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd "Logger OA v2"
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
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

## Guía de Uso

1. **Inicio**: Al abrir la aplicación, se muestra la pantalla de bienvenida.
2. **Gestión de Operadores**: Importa operadores OA desde PDF oficiales (menú: Importar PDF), consulta y edita la base de datos local. Al finalizar la importación, se muestra un resumen detallado de la operación.
3. **Gestión de Concursos y Operaciones**: Crea, edita y exporta logs de concursos y operaciones.
4. **Temas e Idioma**: Cambia entre tema claro/oscuro y selecciona idioma desde el menú principal.
5. **Persistencia**: Todos los datos se guardan automáticamente en la base SQLite local.

---

## Pruebas

Las pruebas unitarias y de integración se encuentran en la carpeta `tests/` y utilizan `pytest`.

Para ejecutar todas las pruebas:
```bash
pytest
```

---

## Internacionalización y Traducciones

El sistema de traducciones es modular y extensible. Los archivos de traducción se encuentran en `src/translation/<idioma>/` y están organizados por secciones (`ui.py`, `menu.py`, `messages.py`, etc.).

Para agregar un nuevo idioma:
1. Crea una carpeta en `src/translation/` con el código del idioma (ej: `fr/` para francés).
2. Copia y adapta los archivos de traducción existentes.
3. El loader central (`translations.py`) combinará automáticamente los módulos.

---

## Scripts de Build Multiplataforma

En la carpeta `scripts/` hay scripts para generar ejecutables en Linux, macOS y Windows usando PyInstaller:
- `build-linux.sh`
- `build-mac.sh`
- `build-windows.bat`

Ejecuta el script correspondiente para generar el ejecutable standalone.

---

## Contribución

¡Contribuciones son bienvenidas! Para colaborar:
- Sigue la arquitectura y estilo modular del proyecto.
- Usa `pytest` para pruebas.
- Reporta bugs o solicita mejoras vía issues en el repositorio.
- Antes de hacer un pull request, asegúrate de que las pruebas pasen y la documentación esté actualizada.

---

## Requisitos del Sistema
- Python >= 3.10
- Linux, Windows o macOS
- Recomendado: entorno virtual para aislar dependencias

---

## Licencia

MIT
