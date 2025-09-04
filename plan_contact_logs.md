# Plan de Implementación: Contact Logs para Radioaficionados

## 1. Modelo de Dominio
- **ContactLog (base/abstracta):**
  - Campos: `id` (UUID), `operator`, `start_time`, `end_time`, `contacts`, `metadata`.
  - Métodos: agregar/eliminar contactos, validaciones generales.
- **OperationLog** y **ContestLog**:
  - Heredan de ContactLog, agregan campos y reglas específicas (ej: nombre de concurso, tipo de operativo).
- **Contact:**
  - Entidad individual (OperationContact, ContestContact) con campos como indicativo, hora, banda, modo, reportes, etc.
  - Relación uno-a-muchos con cada log.

## 2. Persistencia y Paths
- Cada log se guarda en un archivo SQLite independiente, ubicado en `/operativos/` o `/concursos/` según el tipo.
- El nombre del archivo sigue el patrón: `<indicativo>_<tipo>_<timestamp>.sqlite`.
- El módulo `src/config/paths.py` centraliza la lógica de generación de paths y nombres de archivo, y asegura la existencia de carpetas.
- Estructura de tablas:
  - Tabla `logs`: id, tipo, operador, start_time, end_time, metadata.
  - Tabla `contacts`: id, log_id (FK), data (JSON serializado).

## 3. Repositorios
- `ContactLogRepository` implementa métodos CRUD para logs y contactos en SQLite.
- Métodos: crear, guardar, eliminar logs y contactos, obtener contactos de un log.

## 4. Casos de Uso Implementados
- **Crear log:**
  - Crea un log operativo o de concurso, genera el archivo y guarda el log inicial.
- **Abrir log:**
  - Lista archivos de logs disponibles y permite cargar un log y sus contactos desde SQLite.
- **Gestión de contactos:**
  - Agregar, editar y eliminar contactos en un log abierto.
- **Exportar log:**
  - Exporta los contactos de un log a CSV en la carpeta de exportación.

## 5. Flujo actual de la aplicación
1. Crear log (operativo/concurso) → genera archivo y registro inicial.
2. Abrir log existente → carga datos y contactos.
3. Agregar, editar o eliminar contactos.
4. Exportar log a CSV.

## 6. Validaciones y reglas de negocio (pendiente de profundizar)
### Estado actual:
- Validaciones genéricas y específicas refactorizadas en módulos independientes (`validators.py`, `contest_rules.py`, `operation_rules.py`).
- Integración de validaciones en los casos de uso de gestión de contactos.
- Estructura lista para agregar nuevas reglas y reglamentos.

## 7. Exportación (pendiente de ampliar)
- Exportación a ADIF, PDF y otros formatos estándar de radioaficionados.
- Servicios/utilidades para transformar los datos desde SQLite a los formatos requeridos.

## 8. UI/Interface Adapters (pendiente)
### Estado actual:
- Ventana principal con `QStackedWidget` y vistas separadas para bienvenida, operativos y concursos.
- Menú de log unificado con selector de tipo (operativo/concurso).
- Sistema global de tema e idioma integrado en toda la UI.
- Componentes compartidos implementados:
  - `LogFormWidget`: formulario base reutilizable para datos de contacto/log.
  - `ContactTableWidget`: tabla adaptable para mostrar contactos agregados.
  - `CallsignSuggestionWidget`: campo de entrada con autocompletado de indicativos.
  - `ContactQueueWidget`: visualización de la cola de contactos en espera.
- Integración de estos componentes en las views de operativos y concursos.
- Estructura lista para conectar lógica de datos y eventos.

## 9. Extensibilidad
- Arquitectura preparada para agregar nuevos tipos de logs, reglas o formatos de exportación sin modificar la lógica central.
- Repositorios y servicios desacoplados y fácilmente extensibles.

---

## Avances realizados (al 2025-09-04)
- Refactorización de entidades y modelos de dominio.
- Implementación de paths y generación de archivos por log.
- Repositorio base para persistencia en SQLite.
- Casos de uso para crear, abrir, editar y exportar logs y contactos.
- Exportación a CSV funcional.
- Validaciones y reglas de negocio refactorizadas y extensibles.
- Menú de log unificado y selector de tipo de log en la UI.
- Integración completa de temas e idioma en la interfaz.
- Componentes compartidos de UI implementados e integrados en las vistas principales.

## Próximos pasos sugeridos
- Finalizar la conexión de los componentes UI con la lógica de datos y eventos.
- Implementar validaciones de dominio y reglas específicas para concursos y operativos.
- Ampliar exportación a ADIF, PDF y otros formatos.
- Mejorar la gestión de metadatos y cierre de logs.
- Pruebas automatizadas y documentación de los módulos clave.

---

Este documento refleja el estado actual del desarrollo y sirve como referencia para retomar el trabajo en cualquier momento.
