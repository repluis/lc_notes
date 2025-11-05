"""
Script para usar en el shell de Django
Copia y pega estas funciones en el shell interactivo de Django

Para iniciar el shell:
    python manage.py shell

Luego copia y pega las funciones que necesites o ejecuta las consultas directamente.
"""

# ============================================================================
# IMPORTS (copia esto primero en el shell)
# ============================================================================

from django.contrib.auth.models import User as DjangoUser
from notes_home.repositories.user_repository import UserRepository
from notes_home.services.auth_service import AuthService
from notes_home.domain.entities import User as DomainUser
from django.db.models import Q

# Crear instancia del repositorio
user_repo = UserRepository()

# ============================================================================
# CONSULTAS RÁPIDAS (copia y pega estas líneas directamente)
# ============================================================================

# Listar todos los usuarios
def listar_usuarios():
    """Lista todos los usuarios"""
    users = DjangoUser.objects.all().order_by('username')
    print(f"\nTotal: {users.count()} usuarios\n")
    for user in users:
        estado = "ACTIVO" if user.is_active else "INACTIVO"
        print(f"[{user.id}] {user.username} - {user.email} ({estado})")

# Buscar usuario por username
def buscar_username(nombre):
    """Busca un usuario por username"""
    user = user_repo.get_by_username(nombre)
    if user:
        print(f"\nUsuario encontrado:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Activo: {user.is_active}")
        print(f"  Fecha: {user.date_joined}")
    else:
        print(f"Usuario '{nombre}' no encontrado")

# Buscar usuario por ID
def buscar_id(id_usuario):
    """Busca un usuario por ID"""
    user = user_repo.get_by_id(id_usuario)
    if user:
        print(f"\nUsuario ID {user.id}:")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Activo: {user.is_active}")
    else:
        print(f"Usuario con ID {id_usuario} no encontrado")

# Verificar si existe un username
def existe_username(nombre):
    """Verifica si existe un username"""
    existe = user_repo.exists_by_username(nombre)
    print(f"El username '{nombre}' {'existe' if existe else 'no existe'}")

# Verificar si existe un email
def existe_email(email):
    """Verifica si existe un email"""
    existe = user_repo.exists_by_email(email)
    print(f"El email '{email}' {'existe' if existe else 'no existe'}")

# Estadísticas
def estadisticas():
    """Muestra estadísticas de usuarios"""
    total = DjangoUser.objects.count()
    activos = DjangoUser.objects.filter(is_active=True).count()
    inactivos = DjangoUser.objects.filter(is_active=False).count()
    print(f"\n=== ESTADÍSTICAS ===")
    print(f"Total: {total}")
    print(f"Activos: {activos}")
    print(f"Inactivos: {inactivos}")

# Buscar por email
def buscar_email(email):
    """Busca usuarios cuyo email contenga el texto"""
    users = DjangoUser.objects.filter(email__icontains=email)
    print(f"\nEncontrados {users.count()} usuarios:")
    for user in users:
        print(f"  [{user.id}] {user.username} - {user.email}")

# ============================================================================
# EJEMPLOS DE USO DIRECTO (copia y pega estas líneas)
# ============================================================================

# Ejemplo 1: Ver todos los usuarios
# DjangoUser.objects.all()

# Ejemplo 2: Contar usuarios
# DjangoUser.objects.count()

# Ejemplo 3: Obtener un usuario específico
# user = DjangoUser.objects.get(username="nombre_usuario")
# print(user.email)

# Ejemplo 4: Filtrar usuarios activos
# DjangoUser.objects.filter(is_active=True)

# Ejemplo 5: Buscar usuarios con repositorio
# user = user_repo.get_by_username("nombre_usuario")

# Ejemplo 6: Verificar existencia
# user_repo.exists_by_username("nombre_usuario")

# Ejemplo 7: Crear usuario
# new_user = DomainUser(username="test", email="test@test.com", password="password123")
# created = user_repo.create(new_user)

print("\n✓ Funciones cargadas. Usa:")
print("  listar_usuarios()")
print("  buscar_username('nombre')")
print("  buscar_id(1)")
print("  existe_username('nombre')")
print("  existe_email('email@example.com')")
print("  estadisticas()")
print("  buscar_email('gmail')")

