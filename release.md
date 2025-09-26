# Logger OA — v1.0.0 (binarios)

Aplicación de escritorio multiplataforma para gestionar concursos y operaciones de radioaficionados OA, con base de datos local e importación/exportación de datos.

## Descarga
Descargá la aplicación desde GitHub Releases:
- Página de releases: https://github.com/lmmasc/Logger-OA/releases
- En la sección “Assets” de la release v1.0.0 vas a encontrar los binarios para tu sistema:
	- Windows: LoggerOA-v1.0.0-windows-x64.exe
	- macOS: LoggerOA-v1.0.0-macos-universal.dmg
	- Linux: LoggerOA-v1.0.0-linux-x86_64.tar.gz
	- (Opcional) Checksums: SHA256SUMS.txt

Los nombres pueden variar levemente según la build; elegí el que corresponda a tu sistema operativo.

## Instalación y ejecución

### Windows
1. Descargá el .exe y ejecutalo.
2. Si aparece SmartScreen, clic en “Más información” → “Ejecutar de todas formas”.
3. Abrí “Logger OA” desde el menú Inicio.

### macOS
1. Descargá el .dmg y arrastrá “Logger OA” a Aplicaciones.
2. Si Gatekeeper bloquea la app: clic derecho sobre la app → “Abrir” y confirmá.
	 - Alternativa: Sistema → Privacidad y seguridad → “Permitir de todos modos”.

### Linux
1. Descargá el .tar.gz y descomprimí.
2. Desde la carpeta extraída:
	 - `chmod +x LoggerOA`
	 - `./LoggerOA`
3. Si necesitás, ejecutá desde una terminal dentro de la carpeta extraída.

Nota: Los binarios incluyen los runtimes necesarios (Qt/PySide). No es necesario instalar Python ni dependencias.

## Primeros pasos
- Importar operadores:
	- PDF: Base de datos → Importar → Desde PDF (listados oficiales).
	- CSV: Base de datos → Importar → Desde CSV (formato exportado por la app).
- Exportar logs: Archivo → Exportar → TXT/CSV/ADI/PDF.
- Manual de usuario: Ayuda → Manual de uso.
- Backup/Restore: Base de datos → Backup/Restore.

## Requisitos del sistema
- Windows 10/11, macOS 12+ o Linux x86_64.
- No requiere conexión a Internet ni servicios externos (base de datos local).

## Verificación (opcional)
Para verificar integridad, descargá `SHA256SUMS.txt` y compará el checksum de tu binario.

## Resumen de funcionalidades
- Gestión de logs de operación y concursos.
- Base de datos local SQLite.
- Importación desde PDF/CSV y exportación a TXT/CSV/ADI/PDF.
- Interfaz con temas claro/oscuro e idiomas ES/EN.
- Arquitectura desacoplada (Clean Architecture).

## Licencia y créditos
- Licencia: MIT.
- Créditos: Miguel OA4BAU, Raquel OA4EHN.
- Software distribuido “tal cual”; usalo bajo tu propio riesgo (ver README).
