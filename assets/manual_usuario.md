# Licencia y condiciones de uso

Este software se distribuye bajo la licencia MIT. Puedes copiarlo, modificarlo y crear tus propias versiones, siempre y cuando **menciones a los desarrolladores originales** en los créditos:

- Miguel OA4BAU
- Raquel OA4EHN

No se aceptan sugerencias ni mejoras en este repositorio oficial. Eres libre de crear y distribuir tus propias versiones, respetando la mención a los autores.

**Disclaimer:** Este software se proporciona "tal cual", sin garantías de ningún tipo, expresas o implícitas. Los autores no se hacen responsables por daños, pérdidas o cualquier consecuencia derivada del uso del software. Úsalo bajo tu propio riesgo.

# Manual de Usuario — Logger OA

Bienvenido a Logger OA, la aplicación multiplataforma para radioaficionados OA de Perú. Este manual te guía por todas las funciones y menús reales de la app, pensada para usuarios finales que ejecutan el programa desde el archivo ejecutable distribuido (LoggerOA.exe, LoggerOA, etc.).

---

## Instalación y Primer Inicio

1. Descarga el instalador o ejecutable de Logger OA para tu sistema operativo (Windows, Linux o macOS) desde la página oficial o el repositorio.
2. Ejecuta el instalador y sigue las instrucciones en pantalla, o simplemente abre el archivo ejecutable proporcionado.
3. Al finalizar, encontrarás el acceso directo en tu menú de aplicaciones o escritorio.
4. Haz doble clic en el icono de Logger OA para iniciar la aplicación.

---

## Ventana Principal y Menús

Al abrir Logger OA, verás la ventana principal con los siguientes menús:


### Menú Archivo
- **Nuevo** (submenú):
	- **Nuevo operativo**: Crea un nuevo log de operación.
	- **Nuevo concurso**: Crea un nuevo log de concurso.
- **Abrir** (submenú):
	- **Abrir operativo**: Abre un log de operación existente.
	- **Abrir concurso**: Abre un log de concurso existente.
- **Exportar log**: Exporta el log actual en formato compatible.
- **Cerrar log**: Cierra el log actual y vuelve a la pantalla de bienvenida.
- **Abrir carpeta**: Accede rápidamente a la carpeta de trabajo.
- **Salir**: Cierra la aplicación.

### Menú Base de datos
- **Mostrar base de datos**: Abre la ventana de gestión de operadores OA.
- **Importar desde PDF**: Importa operadores OA desde un archivo PDF oficial. Selecciona el PDF y la app procesará los datos, mostrando un resumen (nuevos, actualizados, deshabilitados, rehabilitados).
- **Importar desde base de datos**: Importa operadores desde otro archivo de base de datos.
- **Crear respaldo**: Genera una copia de seguridad de la base de datos local.
- **Restaurar respaldo**: Restaura la base de datos desde un respaldo previo.
- **Exportar a CSV**: Exporta la base de datos de operadores a un archivo CSV.
- **Eliminar base de datos**: Borra la base de datos local (requiere confirmación).

### Menú Preferencias
- **Indicativo** (submenú):
	- **Establecer indicativo**: Permite definir el indicativo principal de operación.
	- **Modo guardar indicativo**: El indicativo se guarda y se reutiliza automáticamente.
	- **Modo preguntar siempre**: La aplicación solicita el indicativo cada vez que se crea o abre un log.
	- **Mostrar indicativo actual**: Visualiza el indicativo actualmente configurado.
- **Aspecto** (submenú):
	- **Tema claro**: Cambia la interfaz al modo claro.
	- **Tema oscuro**: Cambia la interfaz al modo oscuro.
	- **Tema automático**: Adapta el tema según la configuración del sistema operativo.
- **Idioma** (submenú):
	- **Español**: Cambia la interfaz al idioma español.
	- **Inglés**: Cambia la interfaz al idioma inglés.
	- **Automático**: Selecciona el idioma según la configuración del sistema operativo.

### Menú Ayuda
- **Manual de uso**: Muestra este manual en pantalla.
- **Acerca de**: Muestra información sobre la aplicación y el equipo desarrollador.

---

## Flujos principales


### Crear un nuevo log
1. Ve a **Archivo > Nuevo** y selecciona **Nuevo operativo** o **Nuevo concurso**.
2. Si corresponde, define el indicativo en el submenú **Preferencias > Indicativo**.
3. Completa los datos requeridos y comienza a registrar tus contactos.

### Abrir un log existente
1. Ve a **Archivo > Abrir** y selecciona **Abrir operativo** o **Abrir concurso**.
2. Elige el archivo de log que deseas abrir.

### Exportar logs y base de datos
- Para exportar un log: **Archivo > Exportar log**.
- Para exportar la base de datos: **Base de datos > Exportar a CSV**.

### Importar operadores OA desde PDF
1. Ve a **Base de datos > Importar desde PDF**.
2. Selecciona el archivo PDF oficial.
3. Espera el procesamiento y revisa el resumen de la importación.

### Cambiar tema o idioma
- Ve a **Preferencias > Aspecto** para alternar entre modo claro, oscuro o automático.
- Ve a **Preferencias > Idioma** para cambiar entre español, inglés o automático.

### Gestionar indicativo
- Ve a **Preferencias > Indicativo** para definir, visualizar o cambiar el modo de uso del indicativo.

### Crear y restaurar respaldos
- **Base de datos > Crear respaldo** para guardar una copia de seguridad.
- **Base de datos > Restaurar respaldo** para recuperar datos desde un backup.

---

## Preguntas frecuentes

**¿Dónde se guardan mis datos?**  
Tus registros y operadores se almacenan localmente en una base de datos segura (SQLite). No necesitas conexión a internet para usar la app.

**¿Puedo usar Logger OA en cualquier sistema operativo?**  
Sí, descarga el ejecutable adecuado para Windows, Linux o macOS.

**¿Cómo actualizo la lista de operadores OA?**  
Importa el PDF oficial más reciente desde el menú correspondiente.

**¿Cómo obtengo ayuda?**  
La única ayuda disponible es la que se brinda en este manual de usuario, accesible desde el menú Ayuda > Manual de uso dentro de la aplicación. No se ofrece soporte oficial ni atención personalizada.

---

## Soporte y contacto

**Soporte:**
No se brinda soporte oficial ni atención personalizada. El uso del software es bajo tu propio riesgo y responsabilidad. Toda la ayuda disponible está contenida en este manual de usuario.


---

**Condiciones de uso:**
El uso de Logger OA implica la aceptación de la licencia MIT y del descargo de responsabilidad. Si distribuyes, modificas o creas versiones derivadas, debes mantener la mención a los autores originales. No se ofrece soporte oficial ni garantía sobre el funcionamiento, seguridad o resultados del software.

¡Gracias por usar Logger OA v2!
