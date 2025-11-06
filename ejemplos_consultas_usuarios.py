"""
Ejemplos prácticos de consultas a la base de datos de usuarios
Este archivo contiene ejemplos que puedes usar directamente en tu código
"""

# ============================================================================
# OPCIÓN 1: USAR EL REPOSITORIO (Recomendado para operaciones estándar)
# ============================================================================

from notes_home.repositories.user_repository import UserRepository
from notes_home.domain.entities import User

# Crear instancia del repositorio
user_repo = UserRepository()

# Ejemplo 1: Obtener usuario por username
def ejemplo_obtener_por_username():
    """Obtiene un usuario por su nombre de usuario"""
    user = user_repo.get_by_username("nombre_usuario")
    if user:
        print(f"Usuario encontrado:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Activo: {user.is_active}")
        print(f"  Fecha registro: {user.date_joined}")
    else:
        print("Usuario no encontrado")


# Ejemplo 2: Obtener usuario por ID
def ejemplo_obtener_por_id(user_id):
    """Obtiene un usuario por su ID"""
    user = user_repo.get_by_id(user_id)
    if user:
        print(f"Usuario ID {user.id}: {user.username} ({user.email})")
    else:
        print(f"Usuario con ID {user_id} no encontrado")


# Ejemplo 3: Verificar si un usuario existe
def ejemplo_verificar_existencia():
    """Verifica si un usuario existe por username o email"""
    username = "nombre_usuario"
    email = "usuario@example.com"
    
    if user_repo.exists_by_username(username):
        print(f"El username '{username}' ya está en uso")
    else:
        print(f"El username '{username}' está disponible")
    
    if user_repo.exists_by_email(email):
        print(f"El email '{email}' ya está registrado")
    else:
        print(f"El email '{email}' está disponible")


# Ejemplo 4: Autenticar usuario
def ejemplo_autenticar():
    """Autentica un usuario con username y password"""
    user = user_repo.authenticate("nombre_usuario", "contraseña")
    if user:
        print(f"Usuario autenticado: {user.username}")
    else:
        print("Credenciales incorrectas")


# Ejemplo 5: Crear nuevo usuario
def ejemplo_crear_usuario():
    """Crea un nuevo usuario"""
    new_user = User(
        username="nuevo_usuario",
        email="nuevo@example.com",
        password="contraseña_segura_123"
    )
    
    try:
        created_user = user_repo.create(new_user)
        print(f"Usuario creado exitosamente:")
        print(f"  ID: {created_user.id}")
        print(f"  Username: {created_user.username}")
        print(f"  Email: {created_user.email}")
    except ValueError as e:
        print(f"Error al crear usuario: {e}")


# ============================================================================
# OPCIÓN 2: USAR DJANGO ORM DIRECTAMENTE (Para consultas complejas)
# ============================================================================

from django.contrib.auth.models import User as DjangoUser
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

# Ejemplo 6: Obtener todos los usuarios activos
def ejemplo_todos_activos():
    """Obtiene todos los usuarios activos"""
    active_users = DjangoUser.objects.filter(is_active=True)
    print(f"Total de usuarios activos: {active_users.count()}")
    for user in active_users:
        print(f"  - {user.username} ({user.email})")


# Ejemplo 7: Buscar usuarios por email
def ejemplo_buscar_por_email():
    """Busca usuarios cuyo email contenga un texto"""
    search_term = "gmail"
    users = DjangoUser.objects.filter(email__icontains=search_term)
    print(f"Usuarios con '{search_term}' en el email:")
    for user in users:
        print(f"  - {user.username}: {user.email}")


# Ejemplo 8: Usuarios registrados recientemente
def ejemplo_usuarios_recientes():
    """Obtiene usuarios registrados en los últimos 30 días"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_users = DjangoUser.objects.filter(
        date_joined__gte=thirty_days_ago
    ).order_by('-date_joined')
    
    print(f"Usuarios registrados en los últimos 30 días: {recent_users.count()}")
    for user in recent_users:
        print(f"  - {user.username} (registrado: {user.date_joined})")


# Ejemplo 9: Buscar usuarios con múltiples condiciones
def ejemplo_busqueda_avanzada():
    """Busca usuarios con condiciones complejas"""
    # Usuarios activos cuyo username empiece con "admin" o email contenga "test"
    users = DjangoUser.objects.filter(
        Q(is_active=True) & (
            Q(username__startswith="admin") | Q(email__contains="test")
        )
    )
    
    print("Usuarios que cumplen las condiciones:")
    for user in users:
        print(f"  - {user.username} ({user.email})")


# Ejemplo 10: Actualizar usuario
def ejemplo_actualizar_usuario(user_id):
    """Actualiza un usuario"""
    try:
        user = DjangoUser.objects.get(id=user_id)
        user.email = "nuevo_email@example.com"
        user.save()
        print(f"Usuario {user.username} actualizado correctamente")
    except DjangoUser.DoesNotExist:
        print(f"Usuario con ID {user_id} no encontrado")


# Ejemplo 11: Estadísticas de usuarios
def ejemplo_estadisticas():
    """Obtiene estadísticas de usuarios"""
    total_users = DjangoUser.objects.count()
    active_users = DjangoUser.objects.filter(is_active=True).count()
    inactive_users = DjangoUser.objects.filter(is_active=False).count()
    
    print("Estadísticas de usuarios:")
    print(f"  Total: {total_users}")
    print(f"  Activos: {active_users}")
    print(f"  Inactivos: {inactive_users}")


# Ejemplo 12: Obtener usuario con manejo de excepciones
def ejemplo_obtener_seguro():
    """Obtiene un usuario con manejo seguro de excepciones"""
    username = "nombre_usuario"
    
    try:
        user = DjangoUser.objects.get(username=username)
        print(f"Usuario encontrado: {user.username} ({user.email})")
    except DjangoUser.DoesNotExist:
        print(f"Usuario '{username}' no existe")
    except DjangoUser.MultipleObjectsReturned:
        print(f"Error: Múltiples usuarios con username '{username}'")
    except Exception as e:
        print(f"Error inesperado: {e}")


# ============================================================================
# OPCIÓN 3: USAR EL SERVICIO (Para registro y autenticación)
# ============================================================================

from notes_home.services.auth_service import AuthService

# Ejemplo 13: Registrar usuario usando el servicio
def ejemplo_registrar_con_servicio():
    """Registra un usuario usando el servicio de autenticación"""
    auth_service = AuthService()
    
    user, errors = auth_service.register_user(
        username="usuario_prueba",
        email="prueba@example.com",
        password="contraseña_segura_123",
        password_confirm="contraseña_segura_123"
    )
    
    if user:
        print(f"Usuario registrado exitosamente: {user.username}")
    else:
        print("Errores al registrar:")
        for error in errors:
            print(f"  - {error}")


# Ejemplo 14: Autenticar usuario usando el servicio
def ejemplo_autenticar_con_servicio():
    """Autentica un usuario usando el servicio"""
    auth_service = AuthService()
    
    user, errors = auth_service.authenticate_user(
        username="nombre_usuario",
        password="contraseña"
    )
    
    if user:
        print(f"Usuario autenticado: {user.username}")
    else:
        print("Errores de autenticación:")
        for error in errors:
            print(f"  - {error}")


# ============================================================================
# EJEMPLOS DE USO EN VISTAS (Para usar en views.py)
# ============================================================================

# Ejemplo 15: Vista para listar usuarios
def vista_listar_usuarios():
    """Ejemplo de cómo crear una vista para listar usuarios"""
    from django.shortcuts import render
    from django.contrib.auth.decorators import login_required
    
    @login_required
    def list_users_view(request):
        users = DjangoUser.objects.all().order_by('username')
        return {
            'users': users,
            'total': users.count()
        }
    
    return list_users_view


# Ejemplo 16: Vista para buscar usuarios
def vista_buscar_usuarios():
    """Ejemplo de cómo crear una vista para buscar usuarios"""
    def search_users_view(request):
        query = request.GET.get('q', '').strip()
        users = None
        
        if query:
            users = DjangoUser.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            ).order_by('username')
        
        return {
            'users': users or DjangoUser.objects.none(),
            'query': query
        }
    
    return search_users_view


# ============================================================================
# FUNCIONES AUXILIARES ÚTILES
# ============================================================================

def obtener_todos_los_usuarios():
    """Obtiene todos los usuarios usando el repositorio"""
    # Nota: El repositorio actual no tiene un método get_all()
    # Para obtener todos, usa Django ORM directamente:
    users = DjangoUser.objects.all()
    return users


def convertir_django_user_a_domain_user(django_user):
    """Convierte un DjangoUser a una entidad de dominio User"""
    from notes_home.domain.entities import User as DomainUser
    
    return DomainUser(
        id=django_user.id,
        username=django_user.username,
        email=django_user.email,
        password="",  # No retornamos contraseñas
        date_joined=django_user.date_joined,
        is_active=django_user.is_active
    )


# ============================================================================
# EJEMPLO DE USO COMPLETO
# ============================================================================

if __name__ == "__main__":
    # Descomenta las funciones que quieras probar
    
    # Ejemplos con repositorio
    # ejemplo_obtener_por_username()
    # ejemplo_obtener_por_id(1)
    # ejemplo_verificar_existencia()
    
    # Ejemplos con Django ORM
    # ejemplo_todos_activos()
    # ejemplo_buscar_por_email()
    # ejemplo_usuarios_recientes()
    # ejemplo_estadisticas()
    
    # Ejemplos con servicio
    # ejemplo_registrar_con_servicio()
    # ejemplo_autenticar_con_servicio()
    
    print("Descomenta las funciones que quieras probar")

