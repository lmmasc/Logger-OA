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
├── assets/
│   ├── app_icon.ico
│   ├── app_icon.png
│   ├── app_icon.icns
│   └── rcp_logo.png
├── src/
│   ├── main.py
│   └── app/
│       ├── __init__.py
│       └── ui/
│           └── main_window.py
└── .venv/
```

- **.gitignore**: Exclusiones para Git (entornos, cachés, etc).
- **Logger OA v2.code-workspace**: Configuración de espacio de trabajo para VS Code.
- **README.md**: Documentación del proyecto.
- **requirements.txt**: Dependencias del proyecto.
- **assets/**: Carpeta para recursos como iconos e imágenes de la app.
  - `app_icon.ico`: Icono para ejecutable en Windows.
  - `app_icon.png`: Icono para ejecutable en Linux.
  - `app_icon.icns`: Icono para ejecutable en Mac.
  - `rcp_logo.png`: Logo usado dentro de la aplicación.
- **src/main.py**: Punto de entrada de la aplicación. Crea y muestra la ventana principal.
- **src/app/__init__.py**: Marca la carpeta `app` como un paquete Python.
- **src/app/ui/main_window.py**: Define la clase `MainWindow` (ventana principal).
- **.venv/**: Entorno virtual de Python (no se sube a Git).

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

---

## Crear ejecutable multiplataforma

Para generar un ejecutable autocontenible en cada sistema operativo, se recomienda usar [PyInstaller](https://pyinstaller.org/):

### 1. Instalar PyInstaller

```bash
.venv/bin/pip install pyinstaller
```

### 2. Generar el ejecutable

- **En Linux:**
  ```bash
  .venv/bin/pyinstaller src/main.py --onefile --name LoggerOA --icon=assets/app_icon.png
  ```
- **En Windows:**
  Ejecuta el comando equivalente en una terminal de Windows:
  ```cmd
  .venv\Scripts\pyinstaller src\main.py --onefile --name LoggerOA --icon=assets/app_icon.ico
  ```
- **En Mac:**
  Ejecuta el comando equivalente en una terminal de Mac:
  ```bash
  .venv/bin/pyinstaller src/main.py --onefile --name LoggerOA --icon=assets/app_icon.icns
  ```

Esto generará un ejecutable único en la carpeta `dist/` para cada plataforma.

> **Nota:** Debes ejecutar PyInstaller en cada sistema operativo objetivo para obtener el ejecutable nativo correspondiente.
> El icono debe estar en la carpeta `assets/` y en el formato adecuado para cada sistema.

---

## Ejecución

Desde la raíz del proyecto:

```bash
.venv/bin/python src/main.py
```

---

## Dependencias
- **requirements.txt**: Solo dependencias necesarias para ejecutar la aplicación.
- **requirements-dev.txt**: Dependencias para desarrollo y empaquetado (ej: PyInstaller).

Instala dependencias de ejecución con:
```bash
.venv/bin/pip install -r requirements.txt
```

Instala dependencias de desarrollo con:
```bash
.venv/bin/pip install -r requirements-dev.txt
```

---

## Notas
- La estructura está lista para crecer: puedes agregar más módulos en `app/` y más componentes de UI en `app/ui/`.
- El archivo `.gitignore` evita que archivos temporales y entornos virtuales se suban al repositorio.
