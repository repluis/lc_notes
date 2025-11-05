# Sistema de Logging de Operaciones de Base de Datos

Este documento explica cómo funciona el sistema de logging automático para operaciones de base de datos.

## Archivos de Log Generados

El sistema genera **3 archivos de log** en el directorio raíz del proyecto:

1. **`database_operations.log`** - Logs de operaciones CRUD (INSERT, UPDATE, DELETE, SELECT)
2. **`database_queries.log`** - Logs de todas las consultas SQL ejecutadas
3. **`debug.log`** - Logs generales del sistema

## Operaciones Registradas

### INSERT (Crear)
Se registra cuando se crea un nuevo usuario:
```
INFO 2025-11-05 18:30:00,123 [DB OPERATION] INSERT - Creando nuevo usuario: username='juan', email='juan@example.com'
INFO 2025-11-05 18:30:00,456 [DB OPERATION] INSERT EXITOSO - Usuario creado con ID=4, username='juan', email='juan@example.com'
```

Si falla:
```
ERROR 2025-11-05 18:30:00,789 [DB OPERATION] INSERT FALLIDO - Error de validación de contraseña para usuario 'juan': La contraseña es muy corta
```

### SELECT (Consultar)
Se registra cuando se consulta un usuario:
```
INFO 2025-11-05 18:30:10,123 [DB OPERATION] SELECT - Consultando usuario por username='juan'
INFO 2025-11-05 18:30:10,456 [DB OPERATION] SELECT EXITOSO - Usuario encontrado: ID=4, username='juan', email='juan@example.com'
```

Si no se encuentra:
```
WARNING 2025-11-05 18:30:15,123 [DB OPERATION] SELECT - Usuario no encontrado: username='pedro'
```

### UPDATE (Actualizar)
Se registra cuando se actualiza un usuario:
```
INFO 2025-11-05 18:30:20,123 [DB OPERATION] UPDATE - Actualizando usuario ID=4: email: 'juan@example.com' -> 'juan@nuevo.com'
INFO 2025-11-05 18:30:20,456 [DB OPERATION] UPDATE EXITOSO - Usuario actualizado: ID=4, username='juan'
```

### DELETE (Eliminar)
Se registra cuando se elimina un usuario:
```
WARNING 2025-11-05 18:30:25,123 [DB OPERATION] DELETE - Eliminando usuario: ID=4, username='juan', email='juan@example.com'
WARNING 2025-11-05 18:30:25,456 [DB OPERATION] DELETE EXITOSO - Usuario eliminado: ID=4, username='juan'
```

## Dónde se Registran las Operaciones

### Operaciones del Repositorio
Las operaciones realizadas a través del `UserRepository` se registran automáticamente en:
- `database_operations.log`
- `debug.log` (si el nivel es INFO o superior)

**Métodos que registran logs:**
- `create()` - Registra INSERT
- `get_by_username()` - Registra SELECT
- `get_by_id()` - Registra SELECT
- `exists_by_username()` - Registra SELECT
- `exists_by_email()` - Registra SELECT
- `authenticate()` - Registra SELECT

### Operaciones Directas del ORM
Las operaciones realizadas directamente con el ORM de Django (como `User.objects.create()`, `user.save()`, `user.delete()`) se registran automáticamente mediante señales de Django en:
- `database_operations.log`

**Operaciones capturadas:**
- Crear usuario con `User.objects.create()` o `User.objects.create_user()`
- Actualizar usuario con `user.save()`
- Eliminar usuario con `user.delete()`

## Consultas SQL Detalladas

Todas las consultas SQL ejecutadas se registran en `database_queries.log`:
```
DEBUG 2025-11-05 18:30:00,123 [SQL] SELECT "auth_user"."id", "auth_user"."username", "auth_user"."email" FROM "auth_user" WHERE "auth_user"."username" = 'juan' LIMIT 21
```

## Ver los Logs

### Opción 1: Ver directamente los archivos
```bash
# Ver operaciones de base de datos
type database_operations.log

# Ver consultas SQL
type database_queries.log

# Ver logs generales
type debug.log
```

### Opción 2: Usar el comando de gestión (si está disponible)
```bash
python manage.py ver_logs --archivo database
```

## Ejemplos de Logs

### Ejemplo 1: Registro de Usuario
```
INFO 2025-11-05 18:30:00,123 [DB OPERATION] INSERT - Creando nuevo usuario: username='juan', email='juan@example.com'
INFO 2025-11-05 18:30:00,456 [DB OPERATION] INSERT EXITOSO - Usuario creado con ID=4, username='juan', email='juan@example.com'
```

### Ejemplo 2: Consulta de Usuario
```
INFO 2025-11-05 18:30:10,123 [DB OPERATION] SELECT - Consultando usuario por username='juan'
INFO 2025-11-05 18:30:10,456 [DB OPERATION] SELECT EXITOSO - Usuario encontrado: ID=4, username='juan', email='juan@example.com'
```

### Ejemplo 3: Actualización de Usuario
```
INFO 2025-11-05 18:30:20,123 [DB OPERATION] UPDATE - Actualizando usuario ID=4: email: 'juan@example.com' -> 'juan@nuevo.com'
INFO 2025-11-05 18:30:20,456 [DB OPERATION] UPDATE EXITOSO - Usuario actualizado: ID=4, username='juan'
```

### Ejemplo 4: Eliminación de Usuario
```
WARNING 2025-11-05 18:30:25,123 [DB OPERATION] DELETE - Eliminando usuario: ID=4, username='juan', email='juan@example.com'
WARNING 2025-11-05 18:30:25,456 [DB OPERATION] DELETE EXITOSO - Usuario eliminado: ID=4, username='juan'
```

## Configuración

La configuración está en `lc_proyect/settings.py`:

```python
'loggers': {
    'django.db.backends': {
        'handlers': ['sql_file'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
    'database_operations': {
        'handlers': ['console', 'database_operations_file'],
        'level': 'INFO',
    },
    'notes_home.repositories': {
        'handlers': ['console', 'file', 'database_operations_file'],
        'level': 'INFO',
    },
}
```

## Desactivar Logging de SQL

Si quieres desactivar el logging detallado de SQL (puede ser muy verboso), edita `settings.py`:

```python
'django.db.backends': {
    'handlers': ['sql_file'],
    'level': 'WARNING',  # Cambiar de DEBUG a WARNING
    'propagate': False,
},
```

## Ventajas del Sistema

1. **Trazabilidad completa**: Sabes exactamente qué operaciones se realizan en la base de datos
2. **Debugging**: Facilita identificar problemas y errores
3. **Auditoría**: Puedes rastrear quién hizo qué y cuándo
4. **Monitoreo**: Puedes detectar operaciones inusuales o problemas de rendimiento

## Notas Importantes

- Los logs pueden crecer rápidamente, especialmente `database_queries.log` en modo DEBUG
- Considera rotar los logs periódicamente en producción
- Los logs contienen información sensible (emails, usernames), asegúrate de protegerlos adecuadamente
- En producción, considera usar un servicio de logging centralizado

