# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [1.1.0] - 2025-09-29
### Added
- Edición de hora solamente en ContactEditDialog (QTimeEdit) para QTR OA/UTC, preservando la fecha al guardar.
- Deshabilitado automático de operadores vencidos generalizado; se ejecuta al inicio y después de importar (PDF/Excel/CSV).
- Resolver de operador que mantiene la lógica histórica (prefijo/base/sufijo) vía consultas SQLite; integrado en formularios de operación y concursos; nuevas pruebas unitarias.
- Validadores numéricos para RS, potencia e intercambios; marcado visual de campos inválidos y bloqueo de Aceptar si hay errores.
- Visualización de versión en el título de la ventana y en “Acerca de”; generación automática de `src/version.py` desde git en scripts de build (Linux/Windows/macOS).

### Changed
- Sugerencias de indicativos ahora permiten coincidencias por subcadena y el comodín histórico `*` como un carácter (vía SQLite LIKE con `ESCAPE`).
- Atajo de teclado para confirmar indicativo: ahora Ctrl+Enter (antes Alt+Enter).
- Botones de diálogos estandarizados a “Aceptar/Cancelar”.
- Estilo de cabeceras de tablas: ajuste de tamaño de letra y padding horizontal.
- Manejo del título de la ventana unificado mediante helper para preservar el sufijo de versión al cambiar de vista/idioma/tema.
 - Títulos de vistas de logs (operativos/concursos): ahora muestran hora antes que fecha (formato `HH:MM dd/mm/YYYY`).
 - Vistas de logs: el título ya no incluye el sufijo de versión de la app.

### Fixed
- Carga de fechas en diálogo de edición: normalización de timestamps en texto a int/None.
- Correcciones menores de indentación y estabilidad en formularios.
- Ajustes en pruebas y configuración para evitar conflictos de Pylance en imports.
 - Tabla operativos: marcar con `*` la hora UTC cuando su fecha difiere de la fecha OA.
 - Formulario concursos: corrección del ancho del campo RS (RX).

### Docs
- Actualización de documentación de importación (PDF PERÚ/URUGUAY, Excel ARG/CHL y CSV) y atajos de teclado.

### Build
- Scripts de build: generación de versión desde git, limpieza del spec en Linux y mejoras de empaquetado.
 - Refactor: eliminación de setlocale innecesario en tabla de contactos.

## [1.0.0] - 2025-09-26
### Added
- Primera versión pública de Logger OA.
- Gestión de logs de operación y concursos.
- Base de datos local SQLite (sin dependencias externas).
- Importación de operadores desde PDF oficiales del MTC/OA.
- Importación desde CSV (formato exportado por la app).
- Exportación de logs en TXT, CSV, ADI y PDF.
- Interfaz gráfica con PySide6 (Qt), con temas claro/oscuro e idioma ES/EN.
- Arquitectura desacoplada (Clean Architecture).
- Scripts de build para Linux, Windows y macOS.
- Sistema de traducciones modular.
- Pruebas con pytest.

[1.1.0]: https://github.com/lmmasc/Logger-OA/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/lmmasc/Logger-OA/releases/tag/v1.0.0
