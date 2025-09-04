# Plan de Implementación: Contact Logs para Radioaficionados

## 1. Modelo de Dominio
- **ContactLog (base/abstracta):**
  - Campos comunes: `id` (UUID/autoincremental), `start_time`, `end_time`, `operator`, lista de contactos, metadatos.
  - Clase base para todos los logs, facilita extensibilidad y validaciones generales.
- **OperationLog** y **ContestLog**:
  - Heredan de ContactLog, agregan campos y reglas específicas (ej: nombre de concurso, tipo de operativo, validaciones propias).
- **Contact:**
  - Entidad individual (indicativo, hora, banda, modo, reportes, etc.), relacionada uno-a-muchos con cada log.
- Subtipos mediante subclases según la complejidad futura.

## 2. Casos de Uso (Application/Domain)
- Crear, abrir, editar, cerrar y exportar logs.
- Agregar, editar, eliminar contactos en un log.
- Validar reglas específicas (concursos, duplicados, formatos, etc.).
- Sugerir indicativos (autocomplete) y gestionar la cola de espera.

### Flujo principal
- Al crear un log (operativo o concurso), se genera un archivo SQLite en la carpeta correspondiente (`/operativos/` o `/concursos/`).
- El nombre del archivo incluye el indicativo del operador, el tipo de log y un timestamp para unicidad y trazabilidad.
- Los logs pueden abrirse, editarse, cerrarse y exportarse desde el menú principal.
- Exportación soportada a CSV, PDF, ADIF y otros formatos.

## 3. Persistencia
- Cada log se guarda en un archivo SQLite independiente, ubicado en `/operativos/` o `/concursos/` según el tipo.
- El nombre del archivo sigue el patrón: `<indicativo>_<tipo>_<timestamp>.sqlite`.
- Repositorios abstraen el acceso a los archivos/logs y permiten operaciones CRUD sobre logs y contactos.
- Estructura de tablas:
  - Tabla `logs`: id, tipo, operador, start_time, end_time, metadatos.
  - Tabla `contacts`: id, log_id (FK), campos de contacto (indicativo, hora, banda, modo, etc.).

## 4. UI/Interface Adapters
- Ventanas separadas para Operativos y Concursos, ambas basadas en una ventana base reutilizable.
- Componentes comunes: formulario de datos del log, tabla de contactos, campo de entrada con sugerencias, cola de espera.
- Diferencias puntuales: campos adicionales, validaciones, reglas de negocio, formatos de exportación.

### Paths y organización de archivos
- El módulo de paths centraliza la lógica para crear y ubicar los archivos de logs.
- Al crear un log, se utiliza el módulo para generar el path y nombre de archivo adecuado.

## 5. Sugerencias y Autocompletado
- Servicio desacoplado que consulta la base de operadores o historial de contactos.

## 6. Exportación
- Casos de uso para exportar en diferentes formatos (ADIF, Cabrillo, CSV, etc.), como servicios o utilidades.

### Detalles
- La exportación toma los datos desde el archivo SQLite y los transforma al formato deseado.
- Se pueden agregar nuevos formatos de exportación fácilmente mediante servicios o utilidades.

## 7. Validaciones
- Validaciones en la capa de dominio o aplicación, no en la UI.
- Para concursos, reglas específicas (no duplicados, formatos de campo, etc.).

### Ejemplos de validaciones
- No permitir contactos duplicados en concursos.
- Validar formato de campos (indicativo, hora, etc.) al agregar contactos.
- Validaciones extensibles por tipo de log.

## 8. Extensibilidad
- Permitir agregar nuevos subtipos de logs o reglas sin modificar la lógica central.
- Usar interfaces/abstracciones para los repositorios y servicios.

### Consideraciones
- La arquitectura y los modelos permiten agregar nuevos tipos de logs o reglas de negocio sin afectar el núcleo del sistema.
- Los repositorios y servicios están desacoplados y pueden extenderse fácilmente.

---

## Resumen visual de arquitectura
```
UI (Ventanas de Log) 
   |
Interface Adapters (Controladores, Adaptadores de Repositorio)
   |
Application/Domain (Casos de uso, Entidades: ContactLog, Contact, etc.)
   |
Infrastructure (Repositorios de archivos, servicios de exportación)
```

## Siguientes pasos sugeridos
- Refactorizar modelos de dominio para incluir clase base `ContactLog`, campos `id`, `start_time`, `end_time` y metadatos.
- Implementar lógica de generación de paths y nombres de archivo en el módulo de paths.
- Crear repositorios para manejo de archivos SQLite por log.
- Implementar casos de uso principales: crear, abrir, editar, cerrar y exportar logs.
- Iterar agregando reglas, validaciones y exportaciones según necesidades.
