"""
Servicio de notas - Lógica de negocio para notas
"""
from typing import Optional, Tuple, List
from notes_home.domain.entities import Note
from notes_home.repositories.note_repository import NoteRepository


class NoteService:
    """
    Servicio que maneja la lógica de negocio para notas
    """
    
    def __init__(self, note_repository: NoteRepository = None):
        self.note_repository = note_repository or NoteRepository()
    
    def create_note(self, title: str, content: str, user_id: int) -> Tuple[Optional[Note], list]:
        """
        Crea una nueva nota
        
        Returns:
            Tuple[Optional[Note], list]: (Nota creada o None, lista de errores)
        """
        errors = []
        
        # Limpiar y validar datos
        title = title.strip() if title else ""
        content = content.strip() if content else ""
        
        if not title:
            errors.append("El título de la nota no puede estar vacío")
            return None, errors
        
        if len(title) > 200:
            errors.append("El título no puede tener más de 200 caracteres")
            return None, errors
        
        if not user_id:
            errors.append("El ID de usuario es requerido")
            return None, errors
        
        # Crear entidad de dominio
        try:
            domain_note = Note(
                title=title,
                content=content,
                user_id=user_id
            )
        except ValueError as e:
            errors.append(str(e))
            return None, errors
        
        # Guardar en el repositorio
        try:
            created_note = self.note_repository.create(domain_note)
            return created_note, []
        except ValueError as e:
            errors.append(str(e))
            return None, errors
        except Exception as e:
            errors.append(f"Error al crear la nota: {str(e)}")
            return None, errors
    
    def get_note(self, note_id: int, user_id: int) -> Tuple[Optional[Note], list]:
        """
        Obtiene una nota por su ID
        
        Returns:
            Tuple[Optional[Note], list]: (Nota encontrada o None, lista de errores)
        """
        errors = []
        
        if not note_id:
            errors.append("El ID de la nota es requerido")
            return None, errors
        
        if not user_id:
            errors.append("El ID de usuario es requerido")
            return None, errors
        
        try:
            note = self.note_repository.get_by_id(note_id, user_id)
            if not note:
                errors.append("La nota no existe o no tienes permiso para acceder a ella")
            return note, errors
        except Exception as e:
            errors.append(f"Error al obtener la nota: {str(e)}")
            return None, errors
    
    def get_all_notes(self, user_id: int, include_archived: bool = False) -> Tuple[List[Note], list]:
        """
        Obtiene todas las notas de un usuario
        
        Returns:
            Tuple[List[Note], list]: (Lista de notas, lista de errores)
        """
        errors = []
        
        if not user_id:
            errors.append("El ID de usuario es requerido")
            return [], errors
        
        try:
            notes = self.note_repository.get_all_by_user(user_id, include_archived)
            return notes, []
        except Exception as e:
            errors.append(f"Error al obtener las notas: {str(e)}")
            return [], errors
    
    def update_note(self, note_id: int, title: str, content: str, user_id: int, is_archived: bool = False) -> Tuple[Optional[Note], list]:
        """
        Actualiza una nota existente
        
        Returns:
            Tuple[Optional[Note], list]: (Nota actualizada o None, lista de errores)
        """
        errors = []
        
        # Limpiar y validar datos
        title = title.strip() if title else ""
        content = content.strip() if content else ""
        
        if not note_id:
            errors.append("El ID de la nota es requerido")
            return None, errors
        
        if not title:
            errors.append("El título de la nota no puede estar vacío")
            return None, errors
        
        if len(title) > 200:
            errors.append("El título no puede tener más de 200 caracteres")
            return None, errors
        
        if not user_id:
            errors.append("El ID de usuario es requerido")
            return None, errors
        
        # Obtener la nota existente para preservar campos que no se actualizan
        existing_note, get_errors = self.get_note(note_id, user_id)
        if get_errors:
            errors.extend(get_errors)
            return None, errors
        
        if not existing_note:
            errors.append("La nota no existe o no tienes permiso para editarla")
            return None, errors
        
        # Crear entidad de dominio actualizada
        try:
            updated_note = Note(
                id=existing_note.id,
                title=title,
                content=content,
                user_id=user_id,
                created_at=existing_note.created_at,
                is_archived=is_archived
            )
        except ValueError as e:
            errors.append(str(e))
            return None, errors
        
        # Actualizar en el repositorio
        try:
            saved_note = self.note_repository.update(updated_note)
            return saved_note, []
        except ValueError as e:
            errors.append(str(e))
            return None, errors
        except Exception as e:
            errors.append(f"Error al actualizar la nota: {str(e)}")
            return None, errors
    
    def delete_note(self, note_id: int, user_id: int) -> Tuple[bool, list]:
        """
        Elimina una nota
        
        Returns:
            Tuple[bool, list]: (True si se eliminó, lista de errores)
        """
        errors = []
        
        if not note_id:
            errors.append("El ID de la nota es requerido")
            return False, errors
        
        if not user_id:
            errors.append("El ID de usuario es requerido")
            return False, errors
        
        try:
            deleted = self.note_repository.delete(note_id, user_id)
            if not deleted:
                errors.append("La nota no existe o no tienes permiso para eliminarla")
            return deleted, errors
        except ValueError as e:
            errors.append(str(e))
            return False, errors
        except Exception as e:
            errors.append(f"Error al eliminar la nota: {str(e)}")
            return False, errors

