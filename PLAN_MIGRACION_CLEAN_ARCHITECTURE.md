# Plan de Migración y Reestructuración a Clean Architecture

## Objetivo
Reestructurar el proyecto para cumplir estrictamente con Clean Architecture, asegurando que cada módulo, archivo y responsabilidad esté en la capa correspondiente, eliminando duplicidades y mejorando la mantenibilidad y escalabilidad del sistema.

---

## 1. Diagnóstico Actual

- **Dominio disperso:** Entidades y lógica de negocio están en `domain/`, pero parte de la lógica y modelos pueden estar en otros módulos.
- **Duplicidad de repositorios y servicios:** Existen en `application/`, `repositories/`, `services/` y `infrastructure/`.
- **Infraestructura mezclada:** Implementaciones técnicas (DB, archivos, PDF) están en `infrastructure/`, pero también hay carpetas como `db/` y `core/` fuera de lugar.
- **UI separada:** `ui/` contiene la interfaz, pero debe adaptarse como "interface adapter".
- **Utilidades:** `utils/` contiene utilidades, pero algunas pueden estar acopladas a capas superiores.
- **Tests:** Existen, pero deben organizarse por capa.
- **Carpetas ambiguas:** `core/`, `db/`, `app/` requieren revisión y posible eliminación o integración.

---

## 2. Estructura Objetivo (Clean Architecture)

```
src/
  main.py
  domain/
    entities/           # Entidades y modelos de negocio
    value_objects/      # Objetos de valor
    services/           # Lógica de dominio pura
  application/
    use_cases/          # Casos de uso (orquestadores)
    interfaces/         # Interfaces (repositorios, servicios, gateways)
  infrastructure/
    db/                 # Implementaciones de repositorios y acceso a datos
    files/              # Implementaciones de servicios de archivos
    pdf/                # Implementaciones de servicios PDF
    ...                 # Otros adaptadores técnicos
  interface_adapters/
    ui/                 # Adaptadores de interfaz (GUI, CLI, API)
    controllers/        # Controladores que conectan UI y casos de uso
  utils/                # Utilidades puras, sin dependencias de otras capas
  tests/
    domain/
    application/
    infrastructure/
    interface_adapters/
```

---

## 3. Plan de Migración Paso a Paso

### Paso 1: Preparación ✅
- Documentar la arquitectura objetivo en el README. (Hecho)
- Crear la estructura de carpetas objetivo. (Hecho)

### Paso 2: Dominio ✅
- Mover todas las entidades, modelos y lógica de negocio pura a `domain/`. (Hecho)
- Unificar y limpiar entidades duplicadas (`RadioOperator`). (Hecho)
- Eliminar cualquier dependencia de infraestructura en el dominio. (Hecho)


### Paso 3: Application ✅
- Mover los casos de uso (servicios/orquestadores) a `application/use_cases/`. (Hecho)
- Definir todas las interfaces de repositorios y servicios en `application/interfaces/`. (Hecho)
- Asegurarse de que los casos de uso dependan solo de interfaces y modelos de dominio. (Hecho)


### Paso 4: Infrastructure ✅
- Mover implementaciones concretas de repositorios, servicios de archivos, PDF, etc. a `infrastructure/`. (Hecho)
- Cada implementación debe depender solo de interfaces de `application/` y modelos de `domain/`. (Hecho)
- Eliminar cualquier lógica de negocio de esta capa. (Hecho)

### Paso 5: Interface Adapters
- Mover la lógica de presentación y controladores a `interface_adapters/ui/` y `interface_adapters/controllers/`. (Hecho)
- Los controladores deben interactuar solo con los casos de uso de `application/`. (Hecho)
- La UI nunca debe acceder directamente a infraestructura o dominio. (Hecho)

### Paso 6: Utils
- Mantener solo utilidades puras en `utils/`.
- Si alguna utilidad es específica de una capa, moverla a esa capa.

### Paso 7: Tests
- Reorganizar los tests en subcarpetas por capa.
- Asegurarse de que los tests de cada capa solo dependan de esa capa y sus dependencias directas.

### Paso 8: Limpieza y Eliminación
- Revisar y eliminar carpetas/archivos obsoletos o duplicados (`core/`, `db/`, `app/`, etc.).
- Actualizar todos los imports para reflejar la nueva estructura.

### Paso 9: Verificación
- Ejecutar todos los tests y la aplicación para asegurar que todo sigue funcionando.
- Documentar la arquitectura final y los cambios realizados.

---

## 4. Notas y Recomendaciones

- Mantener la independencia de cada capa: las dependencias siempre deben ir hacia adentro (de infraestructura a dominio, nunca al revés).
- Usar interfaces para desacoplar implementaciones concretas.
- Documentar claramente la responsabilidad de cada carpeta y archivo.
- Realizar la migración de forma incremental, validando funcionalidad en cada paso.

---

## 5. Referencias
- [Clean Architecture - Robert C. Martin](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture Example in Python](https://github.com/jeffknupp/clean-architecture)

---

Este plan permitirá migrar el proyecto a una estructura robusta, escalable y mantenible, alineada con Clean Architecture.
