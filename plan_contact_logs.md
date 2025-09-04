# Plan de Implementación: Contact Logs para Radioaficionados

## 1. Modelo de Dominio
- **ContactLog (base/abstracta):**
  - Campos comunes: fecha, operador, lista de contactos, etc.
- **OperationLog** y **ContestLog**:
  - Heredan de ContactLog, agregan campos y reglas específicas.
- **Contact:**
  - Representa un contacto individual (indicativo, hora, banda, modo, etc.).
- Subtipos mediante atributos o subclases según la complejidad.

## 2. Casos de Uso (Application/Domain)
- Crear, abrir, editar, cerrar y exportar logs.
- Agregar, editar, eliminar contactos en un log.
- Validar reglas específicas (concursos, duplicados, formatos, etc.).
- Sugerir indicativos (autocomplete) y gestionar la cola de espera.

## 3. Persistencia
- Cada log se guarda en un archivo (SQLite, JSON, CSV, etc.).
- Repositorios para abstraer el acceso a los archivos/logs.

## 4. UI/Interface Adapters
- Ventanas separadas para Operativos y Concursos, ambas basadas en una ventana base reutilizable.
- Componentes comunes: formulario de datos del log, tabla de contactos, campo de entrada con sugerencias, cola de espera.
- Diferencias puntuales: campos adicionales, validaciones, reglas de negocio, formatos de exportación.

## 5. Sugerencias y Autocompletado
- Servicio desacoplado que consulta la base de operadores o historial de contactos.

## 6. Exportación
- Casos de uso para exportar en diferentes formatos (ADIF, Cabrillo, CSV, etc.), como servicios o utilidades.

## 7. Validaciones
- Validaciones en la capa de dominio o aplicación, no en la UI.
- Para concursos, reglas específicas (no duplicados, formatos de campo, etc.).

## 8. Extensibilidad
- Permitir agregar nuevos subtipos de logs o reglas sin modificar la lógica central.
- Usar interfaces/abstracciones para los repositorios y servicios.

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

## Siguiente paso sugerido
- Definir modelos de dominio y estructura de carpetas.
- Implementar la UI base y los flujos principales.
- Iterar agregando reglas, validaciones y exportaciones según necesidades.
