"""
Repositorio de usuarios - Abstrae el acceso a la base de datos
Permite cambiar de base de datos sin modificar la lógica de negocio
"""
from typing import Optional
from django.contrib.auth.models import User as DjangoUser
from django.db import transaction
from notes_home.domain.entities import User as DomainUser
import logging

# Logger específico para operaciones de base de datos
db_operations_logger = logging.getLogger('database_operations')
repository_logger = logging.getLogger('notes_home.repositories')


class UserRepository:
    """
    Repositorio para gestionar usuarios
    Abstrae el acceso a la base de datos independientemente del motor (SQLite, MySQL, PostgreSQL)
    """
    
    @staticmethod
    def create(user: DomainUser) -> DomainUser:
        """
        Crea un nuevo usuario en la base de datos
        """
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.contrib.auth.password_validation import validate_password
        
        # Log de operación INSERT
        db_operations_logger.info(f"INSERT - Creando nuevo usuario: username='{user.username}', email='{user.email}'")
        
        # Validar la contraseña usando los validadores de Django
        # Esto asegura que la contraseña cumpla con todos los requisitos
        try:
            validate_password(user.password, user=DjangoUser(username=user.username, email=user.email))
        except DjangoValidationError as e:
            error_messages = []
            for error in e.messages:
                error_messages.append(str(error))
            error_text = "; ".join(error_messages) if error_messages else "La contraseña no cumple con los requisitos de seguridad"
            db_operations_logger.error(f"INSERT FALLIDO - Error de validación de contraseña para usuario '{user.username}': {error_text}")
            raise ValueError(error_text)
        
        try:
            with transaction.atomic():
                try:
                    django_user = DjangoUser.objects.create_user(
                        username=user.username,
                        email=user.email,
                        password=user.password,
                        is_active=user.is_active
                    )
                    # Log de éxito
                    db_operations_logger.info(f"INSERT EXITOSO - Usuario creado con ID={django_user.id}, username='{user.username}', email='{user.email}'")
                except Exception as inner_e:
                    db_operations_logger.error(f"INSERT FALLIDO - Error al crear usuario '{user.username}': {type(inner_e).__name__}: {str(inner_e)}")
                    raise
                
                # Crear DomainUser de retorno - usar password vacío ya que no retornamos contraseñas
                return DomainUser(
                    id=django_user.id,
                    username=django_user.username,
                    email=django_user.email,
                    password="",  # No retornamos la contraseña
                    date_joined=django_user.date_joined,
                    is_active=django_user.is_active
                )
        except DjangoValidationError as e:
            error_messages = []
            if hasattr(e, 'error_dict'):
                for field, errors in e.error_dict.items():
                    for error in errors:
                        if hasattr(error, 'message'):
                            error_messages.append(f"{field}: {error.message}")
                        else:
                            error_messages.append(f"{field}: {str(error)}")
            elif hasattr(e, 'messages'):
                error_messages.extend([str(msg) for msg in e.messages])
            else:
                error_messages.append(str(e))
            db_operations_logger.error(f"INSERT FALLIDO - Error de validación Django para usuario '{user.username}': {'; '.join(error_messages) if error_messages else str(e)}")
            raise ValueError("; ".join(error_messages) if error_messages else str(e))
        except ValueError as e:
            raise
        except Exception as e:
            error_msg = str(e)
            db_operations_logger.error(f"INSERT FALLIDO - Error inesperado al crear usuario '{user.username}': {type(e).__name__}: {error_msg}")
            raise ValueError(f"Error al crear el usuario: {error_msg}")
    
    @staticmethod
    def get_by_username(username: str) -> Optional[DomainUser]:
        """
        Obtiene un usuario por su nombre de usuario
        """
        db_operations_logger.info(f"SELECT - Consultando usuario por username='{username}'")
        try:
            django_user = DjangoUser.objects.get(username=username)
            db_operations_logger.info(f"SELECT EXITOSO - Usuario encontrado: ID={django_user.id}, username='{username}', email='{django_user.email}'")
            return DomainUser(
                id=django_user.id,
                username=django_user.username,
                email=django_user.email,
                password="",  # No retornamos la contraseña
                date_joined=django_user.date_joined,
                is_active=django_user.is_active
            )
        except DjangoUser.DoesNotExist:
            db_operations_logger.warning(f"SELECT - Usuario no encontrado: username='{username}'")
            return None
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[DomainUser]:
        """
        Obtiene un usuario por su ID
        """
        db_operations_logger.info(f"SELECT - Consultando usuario por ID={user_id}")
        try:
            django_user = DjangoUser.objects.get(id=user_id)
            db_operations_logger.info(f"SELECT EXITOSO - Usuario encontrado: ID={user_id}, username='{django_user.username}', email='{django_user.email}'")
            return DomainUser(
                id=django_user.id,
                username=django_user.username,
                email=django_user.email,
                password="",
                date_joined=django_user.date_joined,
                is_active=django_user.is_active
            )
        except DjangoUser.DoesNotExist:
            db_operations_logger.warning(f"SELECT - Usuario no encontrado: ID={user_id}")
            return None
    
    @staticmethod
    def exists_by_username(username: str) -> bool:
        """
        Verifica si un usuario existe por nombre de usuario
        """
        db_operations_logger.info(f"SELECT - Verificando existencia de usuario por username='{username}'")
        exists = DjangoUser.objects.filter(username=username).exists()
        db_operations_logger.info(f"SELECT RESULTADO - Usuario '{username}' {'existe' if exists else 'no existe'}")
        return exists
    
    @staticmethod
    def exists_by_email(email: str) -> bool:
        """
        Verifica si un usuario existe por email
        """
        db_operations_logger.info(f"SELECT - Verificando existencia de usuario por email='{email}'")
        exists = DjangoUser.objects.filter(email=email).exists()
        db_operations_logger.info(f"SELECT RESULTADO - Usuario con email '{email}' {'existe' if exists else 'no existe'}")
        return exists
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[DomainUser]:
        """
        Autentica un usuario con username y password
        """
        from django.contrib.auth import authenticate as django_authenticate
        
        db_operations_logger.info(f"SELECT - Autenticando usuario: username='{username}'")
        django_user = django_authenticate(username=username, password=password)
        if django_user:
            db_operations_logger.info(f"SELECT EXITOSO - Autenticación exitosa para usuario: ID={django_user.id}, username='{username}'")
            return DomainUser(
                id=django_user.id,
                username=django_user.username,
                email=django_user.email,
                password="",
                date_joined=django_user.date_joined,
                is_active=django_user.is_active
            )
        db_operations_logger.warning(f"SELECT - Autenticación fallida para usuario: username='{username}'")
        return None

