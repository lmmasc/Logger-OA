# Logger OA v2

## Descripción General
Logger OA v2 es una aplicación de escritorio multiplataforma para el registro y gestión de concursos y operaciones de radioaficionados OA (Perú). Permite llevar un control detallado de contactos, concursos y actividades, con soporte para temas claro/oscuro, persistencia de datos en SQLite y una interfaz moderna basada en PySide6 (Qt).

---

## Motivación de la Reestructuración
El proyecto está en proceso de migración hacia Clean Architecture para mejorar la mantenibilidad, escalabilidad y claridad de responsabilidades. Este README documenta tanto el estado actual como la estructura objetivo.

---

## Estado Actual del Proyecto
- Estructura modular, pero con duplicidad de responsabilidades en algunas carpetas.
- Separación parcial entre dominio, aplicación, infraestructura y presentación.
- Utilidades y pruebas presentes, pero no organizadas por capa.

### Estructura actual (resumida)
```
src/
  main.py
  application/
  domain/
  infrastructure/
  repositories/
  services/
  ui/
  utils/
  ...
```

---

## Objetivo: Clean Architecture
El objetivo es reorganizar el proyecto siguiendo Clean Architecture, asegurando que cada módulo y archivo esté en la capa correspondiente:

### Estructura objetivo
```
src/
  main.py
  domain/
    entities/
    value_objects/
    services/
  application/
    use_cases/
    interfaces/
  infrastructure/
    db/
    files/
    pdf/
  interface_adapters/
    ui/
    controllers/
  utils/
  tests/
    domain/
    application/
    infrastructure/
    interface_adapters/
```

#### Descripción de carpetas
- **domain/**: Entidades, modelos y lógica de negocio pura.
- **application/**: Casos de uso y definición de interfaces (repositorios, servicios, gateways).
- **infrastructure/**: Implementaciones técnicas (DB, archivos, PDF, etc.).
- **interface_adapters/**: Adaptadores de interfaz (UI, controladores, API, CLI).
- **utils/**: Utilidades puras, sin dependencias de otras capas.
- **tests/**: Pruebas organizadas por capa.

---

## Plan de Migración
1. Documentar la arquitectura objetivo y crear la estructura de carpetas.
2. Mover entidades y lógica de negocio a `domain/`.
3. Mover casos de uso e interfaces a `application/`.
4. Mover implementaciones concretas a `infrastructure/`.
5. Adaptar la UI y controladores a `interface_adapters/`.
6. Reorganizar utilidades y pruebas.
7. Eliminar duplicidades y actualizar imports.
8. Verificar funcionalidad y documentar la arquitectura final.

---

## Instalación y Ejecución

1. Clona el repositorio y accede a la carpeta del proyecto:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd "Logger OA v2"
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```

---

## Estado de la Migración
- Consulta el archivo `PLAN_MIGRACION_CLEAN_ARCHITECTURE.md` para ver el plan detallado y el progreso.

---

## Licencia
MIT
