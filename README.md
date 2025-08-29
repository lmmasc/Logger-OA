# Logger OA v2

## Descripción
Proyecto base en Python usando PySide6 para una aplicación de escritorio con una ventana principal. Estructura limpia y lista para escalar.

---

## Estructura de Carpetas y Archivos


```
Logger OA v2/
├── .gitignore
├── Logger OA v2.code-workspace
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── assets/
│   ├── app_icon.ico
│   ├── app_icon.png
│   ├── app_icon.icns
│   └── rcp_logo.png
├── scripts/
│   ├── build-linux.sh
│   ├── build-mac.sh
│   └── build-windows.bat
├── src/
│   ├── main.py
│   └── app/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings_manager.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   └── queries.py
│       └── ui/
│           ├── main_window.py
│           ├── menu_bar.py
│           └── themes/
│               ├── base.qss
│               ├── light.qss
│               ├── dark.qss
│               └── theme_manager.py
└── .venv-linux/ (o .venv-windows)
```

- **.gitignore**: Exclusiones para Git (entornos, cachés, etc).
- **Logger OA v2.code-workspace**: Configuración de espacio de trabajo para VS Code.
- **README.md**: Documentación del proyecto.
- **requirements.txt**: Dependencias del proyecto.
- **requirements-dev.txt**: Dependencias de desarrollo (ej: PyInstaller).
- **assets/**: Carpeta para recursos como iconos e imágenes de la app.
  - `app_icon.ico`: Icono para ejecutable en Windows.
  - `app_icon.png`: Icono para ejecutable en Linux.
  - `app_icon.icns`: Icono para ejecutable en Mac.
  - `rcp_logo.png`: Logo usado dentro de la aplicación.
- **scripts/**: Scripts para automatizar la generación de ejecutables.
  - `build-linux.sh`: Genera el ejecutable en Linux.
  - `build-mac.sh`: Genera el ejecutable en Mac.
  - `build-windows.bat`: Genera el ejecutable en Windows.
- **src/main.py**: Punto de entrada de la aplicación. Crea y muestra la ventana principal.
- **src/app/__init__.py**: Marca la carpeta `app` como un paquete Python.
- **src/app/config/settings_manager.py**: Abstracción de QSettings para configuración persistente.
- **src/app/db/connection.py**: Funciones para abrir/cerrar cualquier base SQLite.
- **src/app/db/queries.py**: Funciones CRUD y consultas reutilizables.
- **src/app/ui/main_window.py**: Define la clase `MainWindow` (ventana principal).
- **src/app/ui/menu_bar.py**: Barra de menús modular.
- **src/app/ui/themes/**: Temas y estilos centralizados (QSS y lógica de temas).
  - `base.qss`: Estilos base comunes.
  - `light.qss`: Tema claro.
  - `dark.qss`: Tema oscuro.
  - `theme_manager.py`: Lógica para aplicar y recordar el tema.
- **.venv-linux/**, **.venv-windows/**: Entornos virtuales (no se suben a Git).

---

## Módulos y Funcionalidades

### src/main.py
- Importa y ejecuta la clase `MainWindow`.
- Inicializa la aplicación Qt.
- Documentado y estructurado para fácil mantenimiento.

### src/app/ui/main_window.py
- Contiene la clase `MainWindow`.
- Hereda de `QMainWindow`.
- Configura el título, tamaño y centra la ventana al iniciar.

### assets/
- Guarda aquí los recursos gráficos de la aplicación.
- Iconos para ejecutables:
  - Windows: `app_icon.ico`
  - Linux: `app_icon.png`
  - Mac: `app_icon.icns`
- Logo de la app: `rcp_logo.png` (para usar dentro de la interfaz).

### scripts/
- Scripts para automatizar la generación de ejecutables multiplataforma.
- Uso:
  - **Linux:**
    ```bash
    chmod +x scripts/build-linux.sh
    ./scripts/build-linux.sh
    ```
  - **Mac:**
    ```bash
    chmod +x scripts/build-mac.sh
    ./scripts/build-mac.sh
    ```
  - **Windows:**
    ```cmd
    scripts\build-windows.bat
    ```
- Cada script debe ejecutarse en su sistema operativo correspondiente y generará el ejecutable en la carpeta `dist/`.

---

## Crear ejecutable multiplataforma

Para generar un ejecutable autocontenible en cada sistema operativo, se recomienda usar [PyInstaller](https://pyinstaller.org/):

### 1. Instalar PyInstaller

```bash
.venv-linux/bin/pip install pyinstaller  # Linux
.venv-windows\Scripts\pip install pyinstaller  # Windows
```

### 2. Generar el ejecutable

- **En Linux:**
  ```bash
  ./scripts/build-linux.sh
  ```
- **En Windows:**
  ```cmd
  scripts\build-windows.bat
  ```
- **En Mac:**
  ```bash
  ./scripts/build-mac.sh
  ```

Esto generará un ejecutable único en la carpeta `dist/` para cada plataforma.

> **Nota:** Debes ejecutar PyInstaller en cada sistema operativo objetivo para obtener el ejecutable nativo correspondiente.
> El icono debe estar en la carpeta `assets/` y en el formato adecuado para cada sistema.

---

## Ejecución

Desde la raíz del proyecto:

```bash
.venv-linux/bin/python src/main.py  # Linux
.venv-windows\Scripts\python src\main.py  # Windows
```

---

## Dependencias
- **requirements.txt**: Solo dependencias necesarias para ejecutar la aplicación.
- **requirements-dev.txt**: Dependencias para desarrollo y empaquetado (ej: PyInstaller).

Instala dependencias de ejecución con:
```bash
.venv-linux/bin/pip install -r requirements.txt
```

Instala dependencias de desarrollo con:
```bash
.venv-linux/bin/pip install -r requirements-dev.txt
```

---

## Configuración automática de entornos virtuales en VS Code

El archivo `Logger OA v2.code-workspace` está configurado para que la terminal integrada de VS Code active automáticamente el entorno virtual correcto según el sistema operativo:

- En Linux: activa `.venv-linux`
- En Windows: activa `.venv-windows`

Esto se logra con la sección `settings`:

```jsonc
"settings": {
  "terminal.integrated.env.linux": {
    "VIRTUAL_ENV": "${workspaceFolder}/.venv-linux",
    "PATH": "${workspaceFolder}/.venv-linux/bin:${env:PATH}"
  },
  "terminal.integrated.env.windows": {
    "VIRTUAL_ENV": "${workspaceFolder}\\.venv-windows",
    "PATH": "${workspaceFolder}\\.venv-windows\\Scripts;${env:PATH}"
  }
}
```

Así, al abrir una terminal en VS Code, se usará automáticamente el entorno adecuado para cada plataforma.

---

## Selección automática del intérprete de Python en VS Code

El archivo `.vscode/settings.json` está configurado para que VS Code seleccione automáticamente el intérprete de Python adecuado según el sistema operativo:

- En Linux: usa `.venv-linux/bin/python`
- En Windows: usa `.venv-windows/Scripts/python.exe`
- En Mac: usa `.venv-mac/bin/python3`

Configuración utilizada:

```jsonc
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv-linux/bin/python",
  "python.defaultInterpreterPath.linux": "${workspaceFolder}/.venv-linux/bin/python",
  "python.defaultInterpreterPath.windows": "${workspaceFolder}\\.venv-windows\\Scripts\\python.exe",
  "python.defaultInterpreterPath.osx": "${workspaceFolder}/.venv-mac/bin/python3"
}
```

Esto permite que VS Code detecte y use automáticamente el entorno virtual correcto al abrir el proyecto, sin necesidad de configuraciones manuales.

---

## Configuración y persistencia de estado

La aplicación utiliza una clase `SettingsManager` basada en QSettings para guardar y recuperar configuraciones de usuario (preferencias, estado de la ventana, etc.) de forma multiplataforma.

### Estructura

```
src/app/config/
    __init__.py
    settings_manager.py
```

- **settings_manager.py**: Contiene la clase `SettingsManager`, que abstrae el uso de QSettings y provee métodos para guardar, obtener y eliminar valores de configuración.

### Ejemplo de uso

```python
from app.config.settings_manager import SettingsManager

settings = SettingsManager()
settings.set_value('ventana/posicion', (100, 100))
pos = settings.get_value('ventana/posicion', (0, 0))
```

Esto permite que la app recuerde configuraciones entre sesiones de forma sencilla y multiplataforma.

---

## Gestión de base de datos (SQLite)

La aplicación utiliza SQLite como motor de base de datos, aprovechando el módulo `sqlite3` incluido en la biblioteca estándar de Python (no requiere instalación adicional).

### Estructura

```
src/app/db/
    __init__.py
    connection.py   # Funciones para abrir/cerrar cualquier base SQLite
    queries.py      # Funciones CRUD y consultas reutilizables para base principal y auxiliares
```

- **connection.py**: Proporciona la función `get_connection(db_path)` para abrir conexiones a cualquier base de datos SQLite (principal o auxiliar).
- **queries.py**: Incluye funciones para ejecutar consultas SELECT, INSERT, UPDATE y DELETE sobre cualquier base, recibiendo la ruta de la base como argumento.

### Ejemplo de uso

```python
from app.db.queries import fetch_all, execute_query

# Consultar todos los registros de una tabla en la base principal
registros = fetch_all('ruta/base_principal.db', 'SELECT * FROM tabla')

# Insertar un registro en una base auxiliar
ok = execute_query('ruta/auxiliar.db', 'INSERT INTO tabla (col1, col2) VALUES (?, ?)', (valor1, valor2))
```

Esto permite trabajar con una base principal y varias bases auxiliares de forma modular y sencilla.

---

## Temas y estilos (claro/oscuro)

La aplicación permite cambiar entre tema claro y oscuro, centralizando los estilos en archivos QSS. La preferencia del usuario se guarda usando SettingsManager.

### Estructura

```
src/app/ui/themes/
    base.qss         # Estilos comunes
    light.qss        # Tema claro
    dark.qss         # Tema oscuro
    theme_manager.py # Lógica para aplicar y recordar el tema
```

- **base.qss**: Estilos base aplicados a todos los temas.
- **light.qss**: Estilos para el tema claro.
- **dark.qss**: Estilos para el tema oscuro.
- **theme_manager.py**: Clase `ThemeManager` para cargar, aplicar y recordar el tema seleccionado por el usuario. Utiliza `SettingsManager` para guardar la preferencia.

### Ejemplo de uso

```python
from app.ui.themes.theme_manager import ThemeManager

themes = ThemeManager()
themes.apply_theme("dark")  # Cambia a tema oscuro
themes.load_last_theme()     # Aplica el último tema usado
```

Esto permite una gestión centralizada y escalable de los estilos visuales de la app.

---

## Menú principal modular

La barra de menús de la aplicación está definida en un archivo independiente para mantener la modularidad y la separación de responsabilidades.

### Estructura

```
src/app/ui/menu_bar.py
```

- **menu_bar.py**: Contiene la clase `MainMenuBar`, que hereda de `QMenuBar` y define los menús y acciones principales de la aplicación.

### Ejemplo de uso

```python
from app.ui.menu_bar import MainMenuBar

menu_bar = MainMenuBar(parent=self)
self.setMenuBar(menu_bar)
```

Esto permite mantener la lógica del menú separada de la ventana principal y facilita su mantenimiento y expansión.

---
