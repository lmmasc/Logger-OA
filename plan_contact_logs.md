# Plan de Implementación: Contact Logs para Radioaficionados

## 1. Modelo de Dominio
- ContactLog (base/abstracta): id, operator, start_time, end_time, contacts, metadata.
- OperationLog y ContestLog: heredan de ContactLog, agregan campos/reglas específicas.
- Contact: entidad individual (OperationContact, ContestContact), relación uno-a-muchos con cada log.

## 2. Persistencia y Paths
- Cada log se guarda en SQLite independiente, en `/operativos/` o `/concursos/`.
- Nombre de archivo: `<indicativo>_<tipo>_<timestamp>.sqlite`.
- `src/config/paths.py` centraliza paths y asegura carpetas.
- Tablas: `logs` y `contacts` (con FK y JSON).

## 3. Repositorios
- `ContactLogRepository` implementa CRUD para logs/contactos en SQLite.

## 4. Casos de Uso Implementados
- Crear log (operativo/concurso), abrir log, gestión de contactos, exportar log a CSV.

## 5. Flujo actual de la aplicación
1. Crear log → genera archivo y registro inicial.
2. Abrir log existente → carga datos y contactos.
3. Agregar, editar o eliminar contactos.
4. Exportar log a CSV.

## 6. Validaciones y reglas de negocio
- Validaciones genéricas y específicas en módulos independientes.
- Integración en casos de uso de gestión de contactos.
- Estructura lista para nuevas reglas.

## 7. Exportación
- Exportación a ADIF, PDF y otros formatos (pendiente de ampliar).
- Servicios/utilidades para transformar datos desde SQLite.

## 8. UI/Interface Adapters
- Ventana principal con `QStackedWidget` y vistas separadas.
- Menú de log unificado con selector de tipo.
- Sistema global de tema e idioma.
- Componentes compartidos: LogFormWidget, ContactTableWidget, CallsignSuggestionWidget, ContactQueueWidget.
- Integración de componentes en views de operativos y concursos.

## 9. Extensibilidad
- Arquitectura preparada para nuevos tipos de logs, reglas o formatos.
- Repositorios y servicios desacoplados.

---

## Avances realizados (al 2025-09-05)
- Refactorización de entidades y modelos de dominio.
- Implementación de paths y generación de archivos por log.
- Repositorio base para persistencia en SQLite.
- Casos de uso para crear, abrir, editar y exportar logs y contactos.
- Exportación a CSV funcional.
- Validaciones y reglas de negocio refactorizadas y extensibles.
- Menú de log unificado y selector de tipo de log en la UI.
- Integración completa de temas e idioma en la interfaz.
- Componentes compartidos de UI implementados e integrados en las vistas principales.
- Corrección de imports para robustez multiplataforma.
- Rutas de archivos generados fuera del proyecto, en carpeta de usuario.
- Mejora de estilos visuales para menús deshabilitados.
- Corrección de errores de importación y de indentación en la UI.

---
### Avances recientes y mejoras clave (2025-09-05)
- Solución de error en el uso de context manager en ContactLogRepository.
- Implementación robusta de la actualización de la tabla de contactos tras agregar y abrir logs.
- Sincronización de la instancia visible de la vista con el ViewManager.
- Refresco visual de la tabla tras cada operación de contacto.
- Mejora en la gestión de referencias y visualización de datos en la UI.
- Validación de flujo completo: alta, apertura y exportación de logs y contactos.

## Próximos pasos sugeridos

- Finalizar la conexión de los componentes UI con la lógica de datos y eventos (revisar edge cases).
- Implementar validaciones de dominio y reglas específicas para concursos y operativos.
- Ampliar exportación a ADIF, PDF y otros formatos.
- Mejorar la gestión de metadatos y cierre de logs.
- Pruebas automatizadas y documentación de los módulos clave.
- Mejorar la gestión de errores y feedback al usuario en la UI.
- Documentar el flujo de instancias y ViewManager para facilitar onboarding.
- Revisar y optimizar el protocolo de context manager en ContactLogRepository si se requiere.

---

Este documento refleja el estado actual del desarrollo y sirve como referencia para retomar el trabajo en cualquier momento. Actualizado al 2025-09-05.
