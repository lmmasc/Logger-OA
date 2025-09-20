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
- **Exportar** (submenú):
	- **Exportar como TXT**: Exporta el log actual en formato texto plano. Al finalizar, se abre la carpeta y se selecciona el archivo exportado.
	- **Exportar como CSV**: Exporta el log actual en formato CSV (hoja de cálculo). Al finalizar, se abre la carpeta y se selecciona el archivo exportado.
	- **Exportar como ADI**: Exporta el log actual en formato ADIF para otros programas de radioafición. Al finalizar, se abre la carpeta y se selecciona el archivo exportado.
	- **Exportar como PDF**: Exporta el log de concurso en formato planilla PDF (solo disponible para logs de concurso). Al finalizar, se abre la carpeta y se selecciona el archivo exportado.
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

1. Ve a **Archivo > Nuevo** y selecciona:
	- **Nuevo operativo**: Para registrar operaciones regulares.
	- **Nuevo concurso**: Para registrar participaciones en concursos.

2. **Opciones al crear un log operativo:**
	- Define el indicativo principal de operación.
	- Selecciona el tipo de operación (CPS, RENER, BOLETIN).
	- Elige la banda de frecuencia y el modo (HF, VHF, LSB, USB, FM, etc.).
	- Ingresa la frecuencia y, si corresponde, el repetidor.
	- La aplicación genera automáticamente el archivo de log y lo asocia a la sesión.

3. **Opciones al crear un log de concurso:**
	- Define el indicativo principal de operación.
	- Selecciona el concurso en el que participas (de una lista predefinida).
	- El log se asocia al nombre del concurso y se genera el archivo correspondiente.

4. Una vez creado el log, la ventana principal mostrará el encabezado con los datos seleccionados y podrás comenzar a registrar contactos.

### Registrar un contacto en el log
1. Escribe el indicativo en el campo "Ingrese indicativo". Si el indicativo existe en la base de datos, se autocompletan los datos asociados y se muestra un resumen en lugar de sugerencias.
2. Completa los campos requeridos del formulario (estación, energía, potencia, RS RX/TX, observaciones, etc. según el tipo de log).
3. Haz clic en **Agregar contacto**. El sistema valida los datos y verifica duplicados. Si el contacto ya existe en el bloque horario (en concursos), se solicita confirmación.
4. Si el indicativo no está en la base de datos, se ofrece agregarlo mediante un diálogo. Si se acepta, se registra el operador y luego el contacto.
5. El contacto se agrega al log y la tabla se actualiza automáticamente. El campo de indicativo se limpia para ingresar el siguiente.

### Eliminar un contacto del log
1. Selecciona el contacto que deseas eliminar en la tabla de contactos del log, seleccionando la fila correspondiente para que se habilite el boton de eliminar.
2. Haz clic en el botón **Eliminar contacto**.
3. El sistema solicitará confirmación antes de eliminar el contacto.
4. Una vez confirmado, el contacto será eliminado del log y la tabla se actualizará automáticamente.

### Funcionamiento de las sugerencias
- Al escribir en el campo de indicativo, a su lado aparecen sugerencias de operadores que coinciden con lo ingresado (mínimo 2 caracteres).
- Las sugerencias muestran el indicativo y el nombre del operador al poner el puntero sobre el.
- Puedes hacer clic en una sugerencia para autocompletar el campo de indicativo y cargar los datos asociados.

### Funcionamiento de la cola de espera
- Puedes agregar indicativos a la cola de espera usando el botón correspondiente o desde el campo de ingreso.
- La cola muestra los indicativos pendientes de registro.
- Al hacer clic en un indicativo de la cola, se autocompleta el campo de ingreso para facilitar el registro.
- Puedes eliminar indicativos de la cola usando el menú contextual (clic derecho sobre el indicativo y seleccionar "Eliminar").
- El sistema evita duplicados en la cola y muestra un mensaje si intentas agregar el mismo indicativo dos veces.

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

### Uso de la ventana de base de datos de operadores
1. Ve al menú **Base de datos > Mostrar base de datos** para abrir la ventana de gestión de operadores OA.
2. La ventana muestra una tabla con todos los operadores registrados y sus datos principales.
	- Puedes agregar un nuevo operador usando el botón **Agregar operador**.
	- Para editar un operador, haz doble clic sobre la fila correspondiente.
	- Para eliminar un operador, selecciona la fila y haz clic en **Eliminar operador** (se solicitará confirmación).
3. En la parte superior, puedes filtrar los operadores por cualquier columna seleccionando el campo en el menú desplegable y escribiendo el texto en el campo de filtro.
	- El filtro es dinámico y muestra el número de resultados encontrados.
	- El texto del filtro se normaliza automáticamente a mayúsculas para facilitar la búsqueda.
4. Debajo del filtro, encontrarás una serie de casillas de verificación (checkboxes) para cada columna de la tabla.
	- Puedes mostrar u ocultar columnas activando o desactivando las casillas correspondientes.
	- La configuración de columnas visibles se guarda automáticamente y se mantiene en futuras sesiones.
5. Puedes ajustar el ancho de las columnas arrastrando los bordes en el encabezado de la tabla.
	- Los anchos configurados se guardan automáticamente.

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
La única ayuda disponible es la que se brinda en este manual de usuario, accesible desde el menú Ayuda > Manual de uso dentro de la aplicación. No se ofrece soporte oficial ni atención personalizada. Pero siempre habrá algun colega OA que te pueda ayudar !

---

## Soporte y contacto

**Soporte:**
No se brinda soporte oficial ni atención personalizada. El uso del software es bajo tu propio riesgo y responsabilidad. Toda la ayuda disponible está contenida en este manual de usuario.


---

**Condiciones de uso:**
El uso de Logger OA implica la aceptación de la licencia MIT y del descargo de responsabilidad. Si distribuyes, modificas o creas versiones derivadas, debes mantener la mención a los autores originales. No se ofrece soporte oficial ni garantía sobre el funcionamiento, seguridad o resultados del software.

¡Gracias por usar Logger OA ,73!
