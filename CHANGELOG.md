# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.


## [Unreleased]
### Added
- Base de compatibilidad para una rama legacy de Windows 7 x86: bootstrap Qt que permite mapear PySide2 como respaldo de PySide6 y recrea enums de Qt6 usados por la UI.
- Archivos separados de dependencias para variante moderna y legacy.
- Script y spec iniciales para build de la variante `win7-x86`.
- Scripts de setup para entornos virtuales modernos y legacy en Windows, con documentación del flujo dual.
- Validaciones explícitas de Python 3.8 x86 en los scripts de setup y build legacy.

### Changed
- Toolchain legacy fijado para compatibilidad real de empaquetado: `pyinstaller==4.10` con `pyinstaller-hooks-contrib==2022.0`.
- Dependencias legacy ajustadas para empaquetado estable con PyInstaller 4.10, fijando `charset-normalizer<3`.
- La variante legacy vuelve a `PySide2/shiboken2 5.14.2.3` y el spec vuelve a `onefile`, eliminando la dependencia temporal en `PyQt5` para evitar la dualidad GPL/comercial en distribuciones legacy.
- Bootstrap Qt legacy ampliado para mapear `exec_()` de Qt5 a `exec()` en `QApplication` y diálogos usados por la UI actual.
- Build legacy ajustado para excluir `multiprocessing` y `concurrent.futures.process`, evitando el runtime hook `pyi_rth_multiprocessing` que fallaba en Windows 7 antes de arrancar la app.
- Build legacy ajustado para excluir `pkg_resources` y `setuptools`, eliminando el runtime hook `pyi_rth_pkgres` que fallaba en Windows 7 al cargar `pyexpat`.
- Bootstrap Qt legacy endurecido para Windows 7: cuando `os.add_dll_directory()` falla con WinError 127, degrada a una ruta segura vía `PATH` en lugar de abortar la inicialización de PySide2.
- Bootstrap Qt legacy reforzado en Windows: adelanta al `PATH` las carpetas de `PySide2` y `shiboken2` antes del primer import, para mejorar la resolución de DLLs en builds `onefile` sobre Windows 7.
- Stack Qt legacy rebajado a `PySide2/shiboken2 5.14.2.3` para probar una línea de wheels potencialmente más compatible con Windows 7 x86.
- Win7 x86 legacy: `qt_compat_bootstrap` ahora agrega tambien la raiz del bundle (`sys._MEIPASS` / directorio del ejecutable) al `PATH` antes de importar PySide2, para que `shiboken2.abi3.dll`, `pyside2.abi3.dll` y los `Qt5*.dll` ubicados en la raiz del onedir sean resolubles durante el arranque.
- Win7 x86 legacy experimental fallback: la variante legacy pasa a priorizar `PyQt5==5.15.4` como backend Qt5 para evitar el bloqueo de carga nativa en `shiboken2` observado con PySide2 en Windows 7, manteniendo la misma superficie de imports `PySide6` mediante `qt_compat_bootstrap`.
- Win7 x86 legacy experimental PyQt5: `qt_compat_bootstrap` ahora prepara tambien rutas de `PyQt5`, registra alias `sip -> PyQt5.sip` y deja de silenciar errores del backend legacy; si PyQt5 o PySide2 fallan al importar en Win7, el mensaje resultante ahora expone la causa real en vez de terminar solo con `ModuleNotFoundError: No module named 'PySide6'`.
- Fixed legacy Win7 x86 PDF startup by pinning `cryptography==42.0.7` in the legacy requirements. `pdfminer.six` had been pulling `cryptography 46.x`, which fails on native Windows 7 during `_rust` import, while `42.0.7` is the last wheel line that explicitly restored Windows 7 compatibility.

### Docs
- Documentados los prerrequisitos de runtime para ejecutar la variante legacy en Windows 7 x86: SP1, KB2999226 y VC++ 2015 x86.


## [1.2.0] - 2026-03-02
### Added
- Exportación ADIF actualizada: se agrega el campo <OPERATOR> en cada registro y se actualiza la versión del estándar a 3.1.6, cumpliendo la especificación oficial.
- Mejora en la exportación de texto para WhatsApp: formato enriquecido con tipo de log, modo, repetidor/frecuencia y operador, usando claves de traducción dedicadas.
- En exportación ADIF de concursos, se agregan los campos <STX_STRING> y <SRX_STRING> con el intercambio completo (RS + correlativo, sin separador), cumpliendo el estándar.
- En exportación ADIF de concursos, se agrega el campo <FREQ> con valor fijo según banda: 7100 (40m), 146000 (VHF/2m), 435000 (UHF/70cm) para compatibilidad con el calificador.
- Los valores por defecto para los operativos ahora se asignan correctamente según la banda al abrir el log: HF (estación "base", energía "comercial", potencia 100), VHF/UHF (estación "portátil", energía "batería", potencia 5).

### Changed
- Exportador ADIF ahora incluye <OPERATOR> y usa la versión 3.1.6 en el encabezado.
- WhatsApp export: el texto ahora utiliza la clave de traducción 'operator_label' para el operador.

### Docs
- Documentación actualizada sobre exportación ADIF y formato de texto para WhatsApp.

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

[NOTA]: La versión 1.2.0 aún no ha sido publicada como release oficial; los cambios están disponibles únicamente en el código fuente.

[1.2.0]: https://github.com/lmmasc/Logger-OA/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/lmmasc/Logger-OA/releases/tag/v1.1.0
[1.0.0]: https://github.com/lmmasc/Logger-OA/releases/tag/v1.0.0
