# Plan de Reestructuración a Clean Architecture

Este documento describe los pasos detallados para reestructurar el proyecto Python en `src/` siguiendo los principios de Clean Architecture.

## 1. Objetivo

Alinear la estructura, nombres y ubicación de archivos y carpetas del proyecto para cumplir con Clean Architecture, separando claramente dominio, casos de uso, infraestructura y adaptadores de interfaz.

---

## 2. Pasos Detallados

### Paso 1: Reorganizar Repositorios
- Mover las interfaces abstractas de repositorios a `src/domain/repositories/`.
- Mover las implementaciones concretas de repositorios a `src/infrastructure/repositories/`.

### Paso 2: Unificar Casos de Uso
- Consolidar todos los casos de uso en `src/application/use_cases/`.
- Eliminar o fusionar `src/application/services/` si su contenido corresponde a casos de uso.

### Paso 3: Reubicar Interfaces
- Mover interfaces de `src/application/interfaces/` a `src/domain/` o `src/application/` según su función.

### Paso 4: Limpiar Infraestructura
- Agrupar archivos de infraestructura por tipo en `src/infrastructure/`:
  - `db/` para base de datos
  - `pdf/` para manejo de PDFs
  - `files/` para archivos generales
- Eliminar subcarpetas demasiado específicas como `operators_update/` y distribuir sus archivos en las carpetas correspondientes.

### Paso 5: Adaptadores de Interfaz
- Mantener controladores y UI en `src/interface_adapters/`:
  - `controllers/` para controladores
  - `ui/` para la interfaz gráfica y vistas
- Mover o eliminar `core/` si su contenido corresponde a utilidades generales (`utils/`) o configuración.

### Paso 6: Entidades y Dominio
- Mantener entidades de negocio en `src/domain/entities/`.
- Mantener abstracciones de dominio (interfaces, repositorios) en `src/domain/`.

### Paso 7: Utilidades
- Mantener utilidades generales en `src/utils/`.

### Paso 8: Punto de Entrada
- Mantener `src/main.py` como único punto de entrada, sin lógica de negocio.

---

## 3. Resumen de la Estructura Final

```
src/
  main.py
  domain/
    entities/
    repositories/
  application/
    use_cases/
  infrastructure/
    db/
    pdf/
    files/
    repositories/
  interface_adapters/
    controllers/
    ui/
  utils/
```

---

## 4. Ejecución

1. Realizar un backup del proyecto.
2. Seguir los pasos 1 a 8 en orden, validando el funcionamiento tras cada cambio.
3. Actualizar los imports en todos los archivos afectados.
4. Ejecutar pruebas tras cada paso para asegurar la integridad del sistema.

---

**Este plan debe ser seguido paso a paso para garantizar una migración segura y ordenada.**
