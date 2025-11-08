"""
Entidades del dominio
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """
    Entidad Usuario del dominio
    Representa un usuario en el sistema
    """
    username: str
    email: str
    password: str  # Será hasheado antes de guardar
    id: Optional[int] = None
    date_joined: Optional[datetime] = None
    is_active: bool = True
    
    def __post_init__(self):
        """Validaciones de dominio - Estas validaciones son redundantes si el servicio ya validó"""
        # Las validaciones principales se hacen en el servicio
        # Estas son solo para asegurar la integridad de la entidad
        # Validar username
        if not self.username or (isinstance(self.username, str) and len(self.username.strip()) == 0):
            raise ValueError("El nombre de usuario no puede estar vacío")
        
        # Validar email
        if not self.email or (isinstance(self.email, str) and ('@' not in self.email or len(self.email.strip()) == 0)):
            raise ValueError("El email debe ser válido")
        
        # Validar password - solo si el usuario no tiene ID (usuario nuevo)
        # Si tiene ID, es un usuario ya creado y no necesitamos validar la contraseña
        if self.id is None:
            # Solo validar contraseña para usuarios nuevos
            if not self.password or (isinstance(self.password, str) and len(self.password.strip()) == 0):
                raise ValueError("La contraseña no puede estar vacía")


@dataclass
class Note:
    """
    Entidad Nota del dominio
    Representa una nota en el sistema
    """
    title: str
    content: str
    user_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_archived: bool = False
    
    def __post_init__(self):
        """Validaciones de dominio"""
        # Validar título
        if not self.title or (isinstance(self.title, str) and len(self.title.strip()) == 0):
            raise ValueError("El título de la nota no puede estar vacío")
        
        if len(self.title.strip()) > 200:
            raise ValueError("El título no puede tener más de 200 caracteres")
        
        # Validar contenido
        if self.content is None:
            self.content = ""
        
        # Validar user_id
        if not self.user_id or not isinstance(self.user_id, int):
            raise ValueError("El ID de usuario es requerido y debe ser un entero")
