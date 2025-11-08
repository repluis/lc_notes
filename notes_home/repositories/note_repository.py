"""
Repositorio de notas - Abstrae el acceso a la base de datos
Permite cambiar de base de datos sin modificar la lógica de negocio
"""
from typing import Optional, List
from django.db import transaction
from notes_home.models import Note as NoteModel
from notes_home.domain.entities import Note as DomainNote
import logging

# Logger específico para operaciones de base de datos
db_operations_logger = logging.getLogger('database_operations')
repository_logger = logging.getLogger('notes_home.repositories')


class NoteRepository:
    """
    Repositorio para gestionar notas
    Abstrae el acceso a la base de datos independientemente del motor (SQLite, MySQL, PostgreSQL)
    """
    
    @staticmethod
    def create(note: DomainNote) -> DomainNote:
        """
        Crea una nueva nota en la base de datos
        """
        db_operations_logger.info(f"INSERT - Creando nueva nota: title='{note.title}', user_id={note.user_id}")
        
        try:
            with transaction.atomic():
                note_model = NoteModel.objects.create(
                    title=note.title,
                    content=note.content,
                    user_id=note.user_id,
                    is_archived=note.is_archived
                )
                
                db_operations_logger.info(f"INSERT EXITOSO - Nota creada con ID={note_model.id}, title='{note.title}', user_id={note.user_id}")
                
                return DomainNote(
                    id=note_model.id,
                    title=note_model.title,
                    content=note_model.content,
                    user_id=note_model.user_id,
                    created_at=note_model.created_at,
                    updated_at=note_model.updated_at,
                    is_archived=note_model.is_archived
                )
        except Exception as e:
            error_msg = str(e)
            db_operations_logger.error(f"INSERT FALLIDO - Error al crear nota '{note.title}': {type(e).__name__}: {error_msg}")
            raise ValueError(f"Error al crear la nota: {error_msg}")
    
    @staticmethod
    def get_by_id(note_id: int, user_id: int) -> Optional[DomainNote]:
        """
        Obtiene una nota por su ID, verificando que pertenezca al usuario
        """
        db_operations_logger.info(f"SELECT - Consultando nota por ID={note_id}, user_id={user_id}")
        try:
            note_model = NoteModel.objects.get(id=note_id, user_id=user_id)
            db_operations_logger.info(f"SELECT EXITOSO - Nota encontrada: ID={note_id}, title='{note_model.title}'")
            
            return DomainNote(
                id=note_model.id,
                title=note_model.title,
                content=note_model.content,
                user_id=note_model.user_id,
                created_at=note_model.created_at,
                updated_at=note_model.updated_at,
                is_archived=note_model.is_archived
            )
        except NoteModel.DoesNotExist:
            db_operations_logger.warning(f"SELECT - Nota no encontrada: ID={note_id}, user_id={user_id}")
            return None
    
    @staticmethod
    def get_all_by_user(user_id: int, include_archived: bool = False) -> List[DomainNote]:
        """
        Obtiene todas las notas de un usuario
        """
        db_operations_logger.info(f"SELECT - Consultando todas las notas del usuario ID={user_id}, include_archived={include_archived}")
        
        queryset = NoteModel.objects.filter(user_id=user_id)
        if not include_archived:
            queryset = queryset.filter(is_archived=False)
        
        notes = queryset.all()
        db_operations_logger.info(f"SELECT EXITOSO - Se encontraron {len(notes)} notas para el usuario ID={user_id}")
        
        return [
            DomainNote(
                id=note.id,
                title=note.title,
                content=note.content,
                user_id=note.user_id,
                created_at=note.created_at,
                updated_at=note.updated_at,
                is_archived=note.is_archived
            )
            for note in notes
        ]
    
    @staticmethod
    def update(note: DomainNote) -> DomainNote:
        """
        Actualiza una nota existente
        """
        if not note.id:
            raise ValueError("El ID de la nota es requerido para actualizar")
        
        db_operations_logger.info(f"UPDATE - Actualizando nota ID={note.id}, title='{note.title}'")
        
        try:
            with transaction.atomic():
                note_model = NoteModel.objects.get(id=note.id, user_id=note.user_id)
                note_model.title = note.title
                note_model.content = note.content
                note_model.is_archived = note.is_archived
                note_model.save()
                
                db_operations_logger.info(f"UPDATE EXITOSO - Nota actualizada: ID={note.id}, title='{note.title}'")
                
                return DomainNote(
                    id=note_model.id,
                    title=note_model.title,
                    content=note_model.content,
                    user_id=note_model.user_id,
                    created_at=note_model.created_at,
                    updated_at=note_model.updated_at,
                    is_archived=note_model.is_archived
                )
        except NoteModel.DoesNotExist:
            db_operations_logger.error(f"UPDATE FALLIDO - Nota no encontrada: ID={note.id}, user_id={note.user_id}")
            raise ValueError("La nota no existe o no pertenece al usuario")
        except Exception as e:
            error_msg = str(e)
            db_operations_logger.error(f"UPDATE FALLIDO - Error al actualizar nota ID={note.id}: {type(e).__name__}: {error_msg}")
            raise ValueError(f"Error al actualizar la nota: {error_msg}")
    
    @staticmethod
    def delete(note_id: int, user_id: int) -> bool:
        """
        Elimina una nota, verificando que pertenezca al usuario
        """
        db_operations_logger.info(f"DELETE - Eliminando nota ID={note_id}, user_id={user_id}")
        
        try:
            with transaction.atomic():
                note_model = NoteModel.objects.get(id=note_id, user_id=user_id)
                note_model.delete()
                
                db_operations_logger.info(f"DELETE EXITOSO - Nota eliminada: ID={note_id}")
                return True
        except NoteModel.DoesNotExist:
            db_operations_logger.warning(f"DELETE - Nota no encontrada: ID={note_id}, user_id={user_id}")
            return False
        except Exception as e:
            error_msg = str(e)
            db_operations_logger.error(f"DELETE FALLIDO - Error al eliminar nota ID={note_id}: {type(e).__name__}: {error_msg}")
            raise ValueError(f"Error al eliminar la nota: {error_msg}")

