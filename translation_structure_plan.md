# Plan de Nueva Estructura de Traducciones

Este documento describe la propuesta para reorganizar el sistema de traducciones del proyecto Logger OA, abarcando todos los contextos donde se usan textos traducibles.

---

## Objetivos
- Facilitar el mantenimiento y escalabilidad de las traducciones.
- Agrupar las claves por componente real y contexto de uso.
- Evitar duplicados y colisiones de claves.
- Permitir automatización y validación de cobertura.

---

## Estructura Recomendada

```
src/translation/
  en/
    ui/
      main_window.py
      menu_bar.py
      db_table_window.py
      contact_table_widget.py
      contact_queue_widget.py
      log_form_widget.py
      log_contest_view.py
      log_ops_view.py
      dialogs/
        export_format_dialog.py
        enter_callsign_dialog.py
        select_contest_dialog.py
        select_log_type_dialog.py
        wait_dialog.py
        contact_edit_dialog.py
        operator_edit_dialog.py
        operativo_config_dialog.py
    export/
      log_txt.py
      log_csv.py
      log_adi.py
    config/
      paths.py
    messages/
      errors.py
      warnings.py
      confirmations.py
      info.py
    shared.py  # Botones, headers, textos comunes
  es/
    ... (igual que en inglés)
```

---

## Detalles por Contexto

- **ui/**: Traducciones específicas de cada componente visual.
- **dialogs/**: Diálogos y popups, cada uno con su propio archivo.
- **export/**: Cabeceras y textos usados en exportación de datos.
- **config/**: Textos usados en utilidades y generación de nombres dinámicos.
- **messages/**: Mensajes de error, advertencia, confirmación e información.
- **shared.py**: Claves comunes (botones, headers, textos genéricos).

---

## Loader Central
- El loader debe combinar todos los diccionarios por contexto y componente.
- Permitir fallback y validación de claves faltantes.

---

## Siguientes pasos
1. Crear carpetas y archivos según la estructura propuesta.
2. Migrar las claves existentes a los nuevos archivos.
3. Actualizar el loader central.
4. Validar cobertura y eliminar duplicados.
5. Documentar el proceso para agregar nuevas claves y módulos.

---

**Este plan puede ser ajustado según necesidades futuras o feedback del equipo.**
