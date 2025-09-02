
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
    use_cases/             # Casos de uso específicos (gestión, actualización, etc.)
  infrastructure/          # Implementaciones técnicas
    db/                    # Acceso y gestión de base de datos SQLite
    pdf/                   # Extracción y procesamiento de PDF
    repositories/          # Repositorios concretos
  interface_adapters/      # Adaptadores de interfaz
    ui/                    # Interfaz gráfica (PySide6)
      views/               # Vistas principales (Welcome, LogOps, LogContest, etc.)
      dialogs/             # Diálogos y ventanas auxiliares
      themes/              # Temas visuales (claro/oscuro)
    controllers/           # Controladores de UI
  config/                  # Configuración, rutas y settings
  translation/             # Internacionalización y traducciones
  utils/                   # Utilidades puras
tests/                     # Pruebas unitarias y de integración
```

### Diagrama de Capas (Clean Architecture)

```
[ UI / Interface Adapters ] <--> [ Application ] <--> [ Domain ] <--> [ Infrastructure ]
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
2. **Gestión de Operadores**: Importa operadores OA desde PDF oficiales (menú: Importar PDF), consulta y edita la base de datos local.
3. **Gestión de Concursos y Operaciones**: Crea, edita y exporta logs de concursos y operaciones.
4. **Temas e Idioma**: Cambia entre tema claro/oscuro y selecciona idioma desde el menú principal.
5. **Persistencia**: Todos los datos se guardan automáticamente en la base SQLite local.

---

## Licencia

MIT
