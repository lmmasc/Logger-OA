Ya manito, aquí el feedback de lo que he podido usar de tu logger el día de hoy, luego lo manoseo más:

General:
  - UX: Detectar esquema de colores cuando el SO lo soporta, de igual manera el idioma del sistema
  - UX: Los menús Archivo y Log pueden ser uno (la opción de abrir carpeta debería ser algo como "ver archivos locales")
  - UX: Los menús Aspecto e Idioma pueden ser uno (algo como "Interfaz")
  - UX: Crear un nuevo log no debería mostrar un diálogo para seleccionar el tipo, debería ser un submenú dentro de Log > Nuevo. (Los diálogos solo deben usarse para confirmar o alertar al usuario de una acción que no espera en el flujo de uso normal de la aplicación)
  - UX: Abrir un nuevo log no debería requerir especificar su tipo, el archivo de log debe contener esta información (tipo + versión) y cargar en concordancia.
  - UX: "Borrar base de datos" no necesita confirmar la cancelación de la operación con un diálogo, el usuario ya decidió que no debe hacerse nada.


Operativo:
  - UX: El usuario podría introducir su indicativo en la primera ejecución del logger y hacerlo persistir, para que al crear un nuevo operativo se escoja si hacerlo directamente con el operador al que pertenece el logger u otro.
  - UX: Los registros deben guardarse de forma descendente (el último debe mostrarse en la primera fila) para ver el número de estaciones registradas a simple vista.
  - UX: ENTER debería guardar directamente el indicativo ingresado (la acción por defecto soportando al flujo de trabajo básico)
  - BUG: Cola de espera permite valores duplicados
  - UX: Debería poderse entrar/salir de la cola de espera con un atajo
  - UX: Cola de espera debería poder registrar/borrar directamente con un atajo
  - UX: No es obvio el proceso de eliminar un contacto registrado 
  - UI: Fechas/Horas deberían estar alineadas verticalmente, es confuso leerlas en una sola línea a primera vista. Pueden estar en alguna esquina, con el valor que siempre cambia al extremo.
  - UI: Input de indicativo y resumen tienen distintas dimensiones
  - UX: Los indicativos en toda la app se beneficiarían en su lectura teniendo una fuente monoespaciada (Courier/Consolas)
  - UI: Las cabeceras de la tabla pueden ser más pequeñas, la información relevante son los registros en sí.
  - UX: La columna país y sus valores pueden tener el código ISO 3166 para ahorrar espacio.
  - UX: Los valores "Sin datos" pueden usar una abreviatura o simplemente nada para evitar el ruido visual.
  - UX: Las columnas de fecha/hora podrían estar antes ya que son más importantes que los demás, y podría obviarse el año para mejor visibilidad.