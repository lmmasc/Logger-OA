# Logger OA v2

## Descripción

**Logger OA v2** es una aplicación de escritorio multiplataforma para el registro y gestión de concursos y operaciones de radioaficionados OA (Perú). Permite llevar un control detallado de contactos, concursos y actividades, con soporte para temas claro/oscuro, persistencia de datos en SQLite y una interfaz moderna basada en PySide6 (Qt).

---

## Requisitos del sistema

- **Sistema operativo:** Linux, Windows o macOS
- **Python:** 3.8 o superior (recomendado 3.12+)
- **Dependencias principales:**
	- PySide6
	- PySide6_Addons
	- PySide6_Essentials
	- shiboken6

---

## Instalación

1. **Clona el repositorio y accede a la carpeta del proyecto:**
	 ```bash
	 git clone <URL_DEL_REPOSITORIO>
	 cd "Logger OA v2"
	 ```

2. **Crea y activa un entorno virtual:**
	 ```bash
	 python3 -m venv .venv
	 source .venv/bin/activate
	 ```

3. **Instala las dependencias:**
	 ```bash
	 pip install -r requirements.txt
	 ```

---

## Ejemplo de ejecución

Para ejecutar la aplicación en modo desarrollo:

```bash
python src/main.py
```

Para generar un ejecutable (ejemplo en Linux):

```bash
bash scripts/build-linux.sh
```
El ejecutable se generará en la carpeta `dist/`.

---

## Estructura de carpetas

```
assets/           # Iconos e imágenes de la aplicación
build/            # Archivos generados por PyInstaller
dist/             # Ejecutables generados
scripts/          # Scripts de build para cada SO
src/
	app/
		config/       # Gestión de configuración (QSettings)
		db/           # Conexión y consultas a SQLite
		ui/           # Interfaz gráfica (ventanas, menús, temas, traducciones)
			themes/     # Archivos QSS para temas claro/oscuro
		utils/        # Utilidades generales (gestión de archivos, rutas)
	main.py         # Punto de entrada de la aplicación
requirements.txt  # Dependencias principales
requirements-dev.txt # Dependencias de desarrollo (ej: pyinstaller)
LoggerOA.spec     # Configuración de PyInstaller
```

---

## Notas sobre la base de datos SQLite

- La aplicación utiliza una base de datos SQLite local para almacenar los registros.
- Por defecto, la base de datos se crea en la ruta: `~/LoggerOA/loggeroa.db` (puede cambiarse en la configuración).
- El acceso y las operaciones CRUD se gestionan desde `src/app/db/connection.py` y `src/app/db/queries.py`.
- No requiere instalación ni configuración adicional de servidores de base de datos.

---

## Manejo de temas claros/oscuros con QSS

- Los temas visuales se gestionan mediante archivos QSS ubicados en `src/app/ui/themes/`.
- El usuario puede alternar entre tema claro (`light.qss`) y oscuro (`dark.qss`) desde el menú de la aplicación.
- La preferencia de tema se guarda automáticamente y se restaura al iniciar la aplicación.
- El archivo `theme_manager.py` se encarga de aplicar el tema seleccionado usando PySide6.

---
