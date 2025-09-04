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
- Validaciones básicas en la capa de dominio (duplicados, formato de campos, etc.).
- Validaciones específicas para concursos (no duplicados, reglas de intercambio, etc.).

## 7. Exportación (pendiente de ampliar)
- Exportación a ADIF, PDF y otros formatos estándar de radioaficionados.
- Servicios/utilidades para transformar los datos desde SQLite a los formatos requeridos.

## 8. UI/Interface Adapters (pendiente)
- Ventanas separadas para Operativos y Concursos, basadas en una ventana base reutilizable.
- Componentes: formulario de datos del log, tabla de contactos, campo de entrada con sugerencias, cola de espera.

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
- Commits realizados en cada etapa para trazabilidad.

## Próximos pasos sugeridos
- Implementar validaciones de dominio y reglas específicas para concursos.
- Ampliar exportación a ADIF, PDF y otros formatos.
- Desarrollar la UI base y los flujos principales de interacción.
- Integrar sugerencias/autocompletado de indicativos.
- Mejorar la gestión de metadatos y cierre de logs.
- Pruebas automatizadas y documentación de los módulos clave.

---

Este documento refleja el estado actual del desarrollo y sirve como referencia para retomar el trabajo en cualquier momento.
