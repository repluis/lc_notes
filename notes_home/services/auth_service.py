"""
Servicio de autenticación - Lógica de negocio para usuarios
"""
from typing import Optional, Tuple
from notes_home.domain.entities import User
from notes_home.repositories.user_repository import UserRepository


class AuthService:
    """
    Servicio que maneja la lógica de negocio para autenticación y registro
    """
    
    def __init__(self, user_repository: UserRepository = None):
        self.user_repository = user_repository or UserRepository()
    
    def register_user(self, username: str, email: str, password: str, password_confirm: str) -> Tuple[Optional[User], list]:
        """
        Registra un nuevo usuario
        
        Returns:
            Tuple[Optional[User], list]: (Usuario creado o None, lista de errores)
        """
        errors = []
        
        # Log temporal para depuración
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"LOG SERVICIO INICIO - password type: {type(password)}, password length: {len(password) if password else 0}, password value: {'***' if password else 'EMPTY'}, password is None: {password is None}, password == '': {password == ''}")
        
        # Verificar que la contraseña esté presente antes de procesar
        if not password:
            logger.error("LOG SERVICIO ERROR - Password está vacío antes de strip")
            errors.append("La contraseña no puede estar vacía")
            return None, errors
        
        # Limpiar espacios en blanco primero (antes de cualquier validación)
        password_before_strip = password
        password = password.strip() if password else ""
        password_confirm = password_confirm.strip() if password_confirm else ""
        username = username.strip() if username else ""
        email = email.strip() if email else ""
        
        logger.error(f"LOG SERVICIO DESPUÉS STRIP - password length: {len(password)}, password_before_strip length: {len(password_before_strip) if password_before_strip else 0}")
        
        # Validaciones básicas - verificar que los datos no estén vacíos después de limpiar
        if not password:
            logger.error("LOG SERVICIO ERROR - Password está vacío después de strip")
            errors.append("La contraseña no puede estar vacía")
            return None, errors
        
        if not username:
            errors.append("El nombre de usuario no puede estar vacío")
            return None, errors
        
        if not email or '@' not in email:
            errors.append("El email debe ser válido")
            return None, errors
        
        # Validaciones de negocio - verificar que las contraseñas coincidan
        if password != password_confirm:
            errors.append("Las contraseñas no coinciden")
            return None, errors
        
        if self.user_repository.exists_by_username(username):
            errors.append("El nombre de usuario ya está en uso")
            return None, errors
        
        if self.user_repository.exists_by_email(email):
            errors.append("El email ya está registrado")
            return None, errors
        
        # Crear entidad de dominio
        logger.error(f"LOG SERVICIO ANTES ENTIDAD - password length: {len(password)}, password type: {type(password)}")
        try:
            domain_user = User(
                username=username,
                email=email,
                password=password  # El repositorio se encargará de hashearlo
            )
            logger.error(f"LOG SERVICIO ENTIDAD CREADA - domain_user.password length: {len(domain_user.password) if domain_user.password else 0}")
        except ValueError as e:
            logger.error(f"LOG SERVICIO ERROR ENTIDAD - {str(e)}")
            errors.append(str(e))
            return None, errors
        
        # Guardar en el repositorio
        logger.error(f"LOG SERVICIO ANTES REPOSITORIO - domain_user.password length: {len(domain_user.password) if domain_user.password else 0}")
        try:
            created_user = self.user_repository.create(domain_user)
            logger.error(f"LOG SERVICIO USUARIO CREADO - ID: {created_user.id if created_user else None}")
            return created_user, []
        except ValueError as e:
            # Errores de validación del repositorio
            logger.error(f"LOG SERVICIO ERROR REPOSITORIO - {str(e)}")
            errors.append(str(e))
            return None, errors
        except Exception as e:
            # Otros errores inesperados
            logger.error(f"LOG SERVICIO ERROR EXCEPTION - {str(e)}")
            errors.append(f"Error al crear el usuario: {str(e)}")
            return None, errors
    
    def authenticate_user(self, username: str, password: str) -> Tuple[Optional[User], list]:
        """
        Autentica un usuario
        
        Returns:
            Tuple[Optional[User], list]: (Usuario autenticado o None, lista de errores)
        """
        errors = []
        
        if not username or not password:
            errors.append("Usuario y contraseña son requeridos")
            return None, errors
        
        user = self.user_repository.authenticate(username, password)
        
        if not user:
            errors.append("Usuario o contraseña incorrectos")
            return None, errors
        
        if not user.is_active:
            errors.append("El usuario está inactivo")
            return None, errors
        
        return user, []

