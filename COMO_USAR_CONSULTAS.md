# Cómo Hacer Consultas a la Base de Datos desde la Consola

Hay dos formas principales de hacer consultas desde la consola:

## Opción 1: Management Command (Recomendado - Más Fácil)

Usa el comando `consultar_usuarios` que acabamos de crear:

### Listar todos los usuarios
```bash
python manage.py consultar_usuarios --listar
```

### Listar solo usuarios activos
```bash
python manage.py consultar_usuarios --activos
```

### Listar solo usuarios inactivos
```bash
python manage.py consultar_usuarios --inactivos
```

### Buscar usuario por username
```bash
python manage.py consultar_usuarios --buscar-username juan
```

### Buscar usuario por ID
```bash
python manage.py consultar_usuarios --buscar-id 1
```

### Buscar usuarios por email (puede ser parcial)
```bash
python manage.py consultar_usuarios --buscar-email gmail
```

### Verificar si existe un username
```bash
python manage.py consultar_usuarios --existe-username juan
```

### Verificar si existe un email
```bash
python manage.py consultar_usuarios --existe-email juan@example.com
```

### Ver estadísticas
```bash
python manage.py consultar_usuarios --estadisticas
```

### Crear un nuevo usuario
```bash
python manage.py consultar_usuarios --crear --username nuevo_usuario --email nuevo@example.com --password contraseña_segura
```

### Ver todas las opciones disponibles
```bash
python manage.py consultar_usuarios --help
```

---

## Opción 2: Shell Interactivo de Django

Para hacer consultas más complejas o interactivas:

### 1. Iniciar el shell
```bash
python manage.py shell
```

### 2. Importar lo necesario
```python
from django.contrib.auth.models import User as DjangoUser
from notes_home.repositories.user_repository import UserRepository

user_repo = UserRepository()
```

### 3. Hacer consultas

#### Listar todos los usuarios
```python
DjangoUser.objects.all()
```

#### Contar usuarios
```python
DjangoUser.objects.count()
```

#### Obtener un usuario específico
```python
user = DjangoUser.objects.get(username="nombre_usuario")
print(user.email)
```

#### Buscar con repositorio
```python
user = user_repo.get_by_username("nombre_usuario")
if user:
    print(f"Email: {user.email}")
```

#### Filtrar usuarios activos
```python
DjangoUser.objects.filter(is_active=True)
```

#### Verificar existencia
```python
user_repo.exists_by_username("nombre_usuario")
```

#### Buscar por email
```python
DjangoUser.objects.filter(email__icontains="gmail")
```

### 4. Usar el script de ayuda

En el shell, puedes copiar y pegar el contenido de `shell_consultas.py`:

```python
# Copia todo el contenido de shell_consultas.py
# Esto cargará funciones útiles como:
listar_usuarios()
buscar_username("nombre")
estadisticas()
```

---

## Ejemplos Rápidos

### Ejemplo 1: Ver todos los usuarios con sus emails
```bash
python manage.py consultar_usuarios --listar
```

### Ejemplo 2: Verificar si puedo usar un username
```bash
python manage.py consultar_usuarios --existe-username mi_usuario
```

### Ejemplo 3: Ver estadísticas rápidas
```bash
python manage.py consultar_usuarios --estadisticas
```

### Ejemplo 4: Encontrar un usuario específico
```bash
python manage.py consultar_usuarios --buscar-username juan
```

---

## Solución de Problemas

### Error: "Unknown command"
Si ves el error "Unknown command: consultar_usuarios", asegúrate de que:
1. Los archivos estén en `notes_home/management/commands/consultar_usuarios.py`
2. Los archivos `__init__.py` existan en `notes_home/management/` y `notes_home/management/commands/`

### Error: "No module named django"
Asegúrate de estar en el entorno virtual correcto y que Django esté instalado.

### Error: "database is locked"
Cierra cualquier otra conexión a la base de datos (servidor Django en ejecución, etc.)

---

## Próximos Pasos

- Modifica `consultar_usuarios.py` para agregar más funcionalidades
- Crea más management commands para otras entidades
- Usa el shell para experimentar con consultas complejas

