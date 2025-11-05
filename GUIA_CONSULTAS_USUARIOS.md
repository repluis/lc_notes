# Guía de Consultas a la Base de Datos de Usuarios

Este documento explica cómo hacer consultas a la base de datos de usuarios en este proyecto.

## Arquitectura

El proyecto usa una arquitectura en capas:
- **Capa de Dominio**: Entidades puras (`notes_home/domain/entities.py`)
- **Capa de Repositorio**: Abstrae el acceso a la base de datos (`notes_home/repositories/user_repository.py`)
- **Capa de Servicio**: Lógica de negocio (`notes_home/services/auth_service.py`)
- **Capa de Presentación**: Vistas y formularios (`notes_home/views.py`, `notes_home/forms.py`)

## Opción 1: Usar el Repositorio (Recomendado)

El repositorio abstrae el acceso a la base de datos y es la forma más limpia de hacer consultas.

### Importar el repositorio

```python
from notes_home.repositories.user_repository import UserRepository
```

### Métodos disponibles

#### 1. Obtener usuario por username
```python
from notes_home.repositories.user_repository import UserRepository

user_repo = UserRepository()
user = user_repo.get_by_username("nombre_usuario")

if user:
    print(f"Usuario encontrado: {user.username}, Email: {user.email}")
else:
    print("Usuario no encontrado")
```

#### 2. Obtener usuario por ID
```python
user = user_repo.get_by_id(1)

if user:
    print(f"Usuario ID {user.id}: {user.username}")
```

#### 3. Verificar si existe un usuario por username
```python
if user_repo.exists_by_username("nombre_usuario"):
    print("El usuario existe")
else:
    print("El usuario no existe")
```

#### 4. Verificar si existe un usuario por email
```python
if user_repo.exists_by_email("usuario@example.com"):
    print("El email ya está registrado")
```

#### 5. Autenticar usuario
```python
user = user_repo.authenticate("nombre_usuario", "contraseña")

if user:
    print(f"Usuario autenticado: {user.username}")
else:
    print("Credenciales incorrectas")
```

#### 6. Crear un nuevo usuario
```python
from notes_home.domain.entities import User

new_user = User(
    username="nuevo_usuario",
    email="nuevo@example.com",
    password="contraseña_segura"
)

try:
    created_user = user_repo.create(new_user)
    print(f"Usuario creado con ID: {created_user.id}")
except ValueError as e:
    print(f"Error: {e}")
```

---

## Opción 2: Usar Django ORM directamente

Si necesitas consultas más complejas, puedes usar el ORM de Django directamente.

### Importar el modelo

```python
from django.contrib.auth.models import User as DjangoUser
```

### Consultas básicas

#### Obtener un usuario
```python
# Por ID
user = DjangoUser.objects.get(id=1)

# Por username
user = DjangoUser.objects.get(username="nombre_usuario")

# Por email
user = DjangoUser.objects.get(email="usuario@example.com")
```

#### Obtener múltiples usuarios (QuerySet)
```python
# Todos los usuarios activos
active_users = DjangoUser.objects.filter(is_active=True)

# Usuarios con email específico
users_with_email = DjangoUser.objects.filter(email__contains="@gmail.com")

# Usuarios ordenados por fecha de registro
recent_users = DjangoUser.objects.all().order_by('-date_joined')

# Limitar resultados
first_10_users = DjangoUser.objects.all()[:10]
```

#### Verificar existencia
```python
# Verificar si existe
exists = DjangoUser.objects.filter(username="nombre_usuario").exists()

# Contar usuarios
count = DjangoUser.objects.filter(is_active=True).count()
```

#### Consultas más complejas
```python
# Usuarios registrados en los últimos 30 días
from datetime import datetime, timedelta
from django.utils import timezone

thirty_days_ago = timezone.now() - timedelta(days=30)
recent_users = DjangoUser.objects.filter(date_joined__gte=thirty_days_ago)

# Usuarios con username que empiece con "admin"
admin_users = DjangoUser.objects.filter(username__startswith="admin")

# Usuarios inactivos ordenados por email
inactive_users = DjangoUser.objects.filter(
    is_active=False
).order_by('email')

# Combinar condiciones
from django.db.models import Q

users = DjangoUser.objects.filter(
    Q(is_active=True) | Q(username__startswith="admin")
)
```

#### Actualizar usuarios
```python
# Actualizar un usuario
user = DjangoUser.objects.get(id=1)
user.email = "nuevo_email@example.com"
user.save()

# Actualizar múltiples usuarios
DjangoUser.objects.filter(is_active=False).update(is_active=True)
```

#### Eliminar usuarios
```python
# Eliminar un usuario
user = DjangoUser.objects.get(id=1)
user.delete()

# Eliminar múltiples usuarios
DjangoUser.objects.filter(is_active=False).delete()
```

---

## Opción 3: Usar el Servicio de Autenticación

Para operaciones relacionadas con autenticación y registro, usa el servicio.

### Importar el servicio

```python
from notes_home.services.auth_service import AuthService
```

### Métodos disponibles

#### Registrar un usuario
```python
auth_service = AuthService()
user, errors = auth_service.register_user(
    username="nuevo_usuario",
    email="nuevo@example.com",
    password="contraseña_segura",
    password_confirm="contraseña_segura"
)

if user:
    print(f"Usuario registrado: {user.username}")
else:
    for error in errors:
        print(f"Error: {error}")
```

#### Autenticar un usuario
```python
user, errors = auth_service.authenticate_user(
    username="nombre_usuario",
    password="contraseña"
)

if user:
    print(f"Usuario autenticado: {user.username}")
else:
    for error in errors:
        print(f"Error: {error}")
```

---

## Ejemplos de Uso en Vistas

### Ejemplo 1: Listar todos los usuarios
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser

@login_required
def list_users(request):
    users = DjangoUser.objects.all().order_by('username')
    return render(request, 'list_users.html', {'users': users})
```

### Ejemplo 2: Buscar usuario
```python
from django.shortcuts import render
from django.contrib.auth.models import User as DjangoUser

def search_user(request):
    query = request.GET.get('q', '')
    if query:
        users = DjangoUser.objects.filter(
            username__icontains=query
        ) | DjangoUser.objects.filter(
            email__icontains=query
        )
    else:
        users = DjangoUser.objects.none()
    
    return render(request, 'search_user.html', {'users': users, 'query': query})
```

### Ejemplo 3: Obtener perfil de usuario
```python
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User as DjangoUser
from notes_home.repositories.user_repository import UserRepository

def user_profile(request, user_id):
    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)
    
    if not user:
        # Manejar error
        return render(request, 'error.html', {'message': 'Usuario no encontrado'})
    
    return render(request, 'user_profile.html', {'user': user})
```

---

## Resumen de Recomendaciones

1. **Usa el Repositorio** cuando:
   - Necesites operaciones estándar (crear, leer, verificar existencia)
   - Quieras mantener la abstracción de la base de datos
   - Quieras trabajar con entidades de dominio

2. **Usa Django ORM directamente** cuando:
   - Necesites consultas complejas (filtros avanzados, agregaciones)
   - Necesites actualizar o eliminar múltiples registros
   - Quieras hacer consultas específicas que no están en el repositorio

3. **Usa el Servicio** cuando:
   - Necesites registrar o autenticar usuarios
   - Quieras aplicar lógica de negocio (validaciones, reglas de negocio)

---

## Notas Importantes

- El repositorio retorna entidades de dominio (`User` de `notes_home.domain.entities`)
- Django ORM retorna objetos `DjangoUser` (modelo de Django)
- Las contraseñas nunca se retornan por seguridad (se retornan como cadena vacía)
- Todas las operaciones que modifican datos deben usar transacciones cuando sea necesario

