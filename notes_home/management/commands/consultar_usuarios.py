"""
Management command para consultar usuarios desde la consola
Uso: python manage.py consultar_usuarios [opciones]
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User as DjangoUser
from notes_home.repositories.user_repository import UserRepository
from notes_home.services.auth_service import AuthService


class Command(BaseCommand):
    help = 'Consulta usuarios en la base de datos. Usa --help para ver todas las opciones.'

    def add_arguments(self, parser):
        # Opciones para listar usuarios
        parser.add_argument(
            '--listar',
            action='store_true',
            help='Lista todos los usuarios',
        )
        parser.add_argument(
            '--activos',
            action='store_true',
            help='Lista solo usuarios activos',
        )
        parser.add_argument(
            '--inactivos',
            action='store_true',
            help='Lista solo usuarios inactivos',
        )
        
        # Opciones para buscar usuarios
        parser.add_argument(
            '--buscar-username',
            type=str,
            help='Busca un usuario por username',
        )
        parser.add_argument(
            '--buscar-id',
            type=int,
            help='Busca un usuario por ID',
        )
        parser.add_argument(
            '--buscar-email',
            type=str,
            help='Busca usuarios por email (puede ser parcial)',
        )
        
        # Opciones para verificar existencia
        parser.add_argument(
            '--existe-username',
            type=str,
            help='Verifica si existe un usuario con ese username',
        )
        parser.add_argument(
            '--existe-email',
            type=str,
            help='Verifica si existe un usuario con ese email',
        )
        
        # Opciones para estadísticas
        parser.add_argument(
            '--estadisticas',
            action='store_true',
            help='Muestra estadísticas de usuarios',
        )
        
        # Opciones para crear usuario
        parser.add_argument(
            '--crear',
            action='store_true',
            help='Crea un nuevo usuario (requiere --username, --email, --password)',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username para crear usuario',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email para crear usuario',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password para crear usuario',
        )

    def handle(self, *args, **options):
        user_repo = UserRepository()
        
        # Listar usuarios
        if options['listar']:
            self.listar_usuarios()
        elif options['activos']:
            self.listar_usuarios_activos()
        elif options['inactivos']:
            self.listar_usuarios_inactivos()
        
        # Buscar usuarios
        elif options['buscar_username']:
            self.buscar_por_username(user_repo, options['buscar_username'])
        elif options['buscar_id']:
            self.buscar_por_id(user_repo, options['buscar_id'])
        elif options['buscar_email']:
            self.buscar_por_email(options['buscar_email'])
        
        # Verificar existencia
        elif options['existe_username']:
            self.verificar_username(user_repo, options['existe_username'])
        elif options['existe_email']:
            self.verificar_email(user_repo, options['existe_email'])
        
        # Estadísticas
        elif options['estadisticas']:
            self.mostrar_estadisticas()
        
        # Crear usuario
        elif options['crear']:
            if not all([options['username'], options['email'], options['password']]):
                raise CommandError('Para crear un usuario necesitas --username, --email y --password')
            self.crear_usuario(user_repo, options['username'], options['email'], options['password'])
        
        # Si no se especifica ninguna opción, mostrar ayuda
        else:
            self.stdout.write(self.style.WARNING('No se especificó ninguna acción. Usa --help para ver las opciones disponibles.'))
            self.stdout.write('')
            self.stdout.write('Ejemplos de uso:')
            self.stdout.write('  python manage.py consultar_usuarios --listar')
            self.stdout.write('  python manage.py consultar_usuarios --buscar-username juan')
            self.stdout.write('  python manage.py consultar_usuarios --estadisticas')
            self.stdout.write('  python manage.py consultar_usuarios --existe-email juan@example.com')

    def listar_usuarios(self):
        """Lista todos los usuarios"""
        users = DjangoUser.objects.all().order_by('username')
        self.stdout.write(self.style.SUCCESS(f'\nTotal de usuarios: {users.count()}\n'))
        
        for user in users:
            estado = 'ACTIVO' if user.is_active else 'INACTIVO'
            self.stdout.write(f'  [{user.id}] {user.username} - {user.email} ({estado}) ')
            self.stdout.write(f'      Registrado: {user.date_joined}')

    def listar_usuarios_activos(self):
        """Lista solo usuarios activos"""
        users = DjangoUser.objects.filter(is_active=True).order_by('username')
        self.stdout.write(self.style.SUCCESS(f'\nUsuarios activos: {users.count()}\n'))
        
        for user in users:
            self.stdout.write(f'  [{user.id}] {user.username} - {user.email}')
            self.stdout.write(f'      Registrado: {user.date_joined}')

    def listar_usuarios_inactivos(self):
        """Lista solo usuarios inactivos"""
        users = DjangoUser.objects.filter(is_active=False).order_by('username')
        self.stdout.write(self.style.SUCCESS(f'\nUsuarios inactivos: {users.count()}\n'))
        
        for user in users:
            self.stdout.write(f'  [{user.id}] {user.username} - {user.email}')
            self.stdout.write(f'      Registrado: {user.date_joined}')

    def buscar_por_username(self, user_repo, username):
        """Busca un usuario por username"""
        user = user_repo.get_by_username(username)
        
        if user:
            self.stdout.write(self.style.SUCCESS(f'\nUsuario encontrado:\n'))
            self.stdout.write(f'  ID: {user.id}')
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'  Email: {user.email}')
            self.stdout.write(f'  Activo: {user.is_active}')
            self.stdout.write(f'  Fecha registro: {user.date_joined}')
        else:
            self.stdout.write(self.style.ERROR(f'\nUsuario "{username}" no encontrado'))

    def buscar_por_id(self, user_repo, user_id):
        """Busca un usuario por ID"""
        user = user_repo.get_by_id(user_id)
        
        if user:
            self.stdout.write(self.style.SUCCESS(f'\nUsuario encontrado:\n'))
            self.stdout.write(f'  ID: {user.id}')
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'  Email: {user.email}')
            self.stdout.write(f'  Activo: {user.is_active}')
            self.stdout.write(f'  Fecha registro: {user.date_joined}')
        else:
            self.stdout.write(self.style.ERROR(f'\nUsuario con ID {user_id} no encontrado'))

    def buscar_por_email(self, email):
        """Busca usuarios por email (puede ser parcial)"""
        users = DjangoUser.objects.filter(email__icontains=email)
        
        if users.exists():
            self.stdout.write(self.style.SUCCESS(f'\nUsuarios encontrados ({users.count()}):\n'))
            for user in users:
                self.stdout.write(f'  [{user.id}] {user.username} - {user.email}')
        else:
            self.stdout.write(self.style.ERROR(f'\nNo se encontraron usuarios con email que contenga "{email}"'))

    def verificar_username(self, user_repo, username):
        """Verifica si existe un username"""
        existe = user_repo.exists_by_username(username)
        
        if existe:
            self.stdout.write(self.style.SUCCESS(f'\n✓ El username "{username}" ya está en uso'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✓ El username "{username}" está disponible'))

    def verificar_email(self, user_repo, email):
        """Verifica si existe un email"""
        existe = user_repo.exists_by_email(email)
        
        if existe:
            self.stdout.write(self.style.SUCCESS(f'\n✓ El email "{email}" ya está registrado'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✓ El email "{email}" está disponible'))

    def mostrar_estadisticas(self):
        """Muestra estadísticas de usuarios"""
        total = DjangoUser.objects.count()
        activos = DjangoUser.objects.filter(is_active=True).count()
        inactivos = DjangoUser.objects.filter(is_active=False).count()
        
        self.stdout.write(self.style.SUCCESS('\n=== ESTADÍSTICAS DE USUARIOS ===\n'))
        self.stdout.write(f'  Total de usuarios: {total}')
        self.stdout.write(f'  Usuarios activos: {activos}')
        self.stdout.write(f'  Usuarios inactivos: {inactivos}')
        
        if total > 0:
            porcentaje_activos = (activos / total) * 100
            self.stdout.write(f'  Porcentaje activos: {porcentaje_activos:.1f}%')

    def crear_usuario(self, user_repo, username, email, password):
        """Crea un nuevo usuario"""
        from notes_home.domain.entities import User as DomainUser
        
        self.stdout.write(f'\nCreando usuario: {username}...')
        
        # Verificar si ya existe
        if user_repo.exists_by_username(username):
            self.stdout.write(self.style.ERROR(f'Error: El username "{username}" ya está en uso'))
            return
        
        if user_repo.exists_by_email(email):
            self.stdout.write(self.style.ERROR(f'Error: El email "{email}" ya está registrado'))
            return
        
        # Crear usuario
        try:
            new_user = DomainUser(
                username=username,
                email=email,
                password=password
            )
            created_user = user_repo.create(new_user)
            self.stdout.write(self.style.SUCCESS(f'\n✓ Usuario creado exitosamente:'))
            self.stdout.write(f'  ID: {created_user.id}')
            self.stdout.write(f'  Username: {created_user.username}')
            self.stdout.write(f'  Email: {created_user.email}')
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'\nError al crear usuario: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nError inesperado: {e}'))

