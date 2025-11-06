"""
Middleware para registrar operaciones de base de datos (UPDATE y DELETE)
"""
import logging
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

# Logger para operaciones de base de datos
db_operations_logger = logging.getLogger('database_operations')


@receiver(pre_save, sender=User)
def log_user_pre_save(sender, instance, **kwargs):
    """Registra cuando se va a guardar un usuario (UPDATE)"""
    if instance.pk:  # Si tiene pk, es una actualización
        try:
            old_instance = User.objects.get(pk=instance.pk)
            # Verificar si hay cambios
            changes = []
            if old_instance.username != instance.username:
                changes.append(f"username: '{old_instance.username}' -> '{instance.username}'")
            if old_instance.email != instance.email:
                changes.append(f"email: '{old_instance.email}' -> '{instance.email}'")
            if old_instance.is_active != instance.is_active:
                changes.append(f"is_active: {old_instance.is_active} -> {instance.is_active}")
            
            if changes:
                db_operations_logger.info(f"UPDATE - Actualizando usuario ID={instance.pk}: {', '.join(changes)}")
        except User.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def log_user_post_save(sender, instance, created, **kwargs):
    """Registra cuando se guarda un usuario"""
    if created:
        # Esto ya se registra en el repositorio, pero lo registramos aquí también por si se crea directamente
        db_operations_logger.info(f"INSERT - Usuario creado directamente con ORM: ID={instance.pk}, username='{instance.username}'")
    else:
        db_operations_logger.info(f"UPDATE EXITOSO - Usuario actualizado: ID={instance.pk}, username='{instance.username}'")


@receiver(pre_delete, sender=User)
def log_user_pre_delete(sender, instance, **kwargs):
    """Registra cuando se va a eliminar un usuario"""
    db_operations_logger.warning(f"DELETE - Eliminando usuario: ID={instance.pk}, username='{instance.username}', email='{instance.email}'")


@receiver(post_delete, sender=User)
def log_user_post_delete(sender, instance, **kwargs):
    """Registra cuando se eliminó un usuario"""
    db_operations_logger.warning(f"DELETE EXITOSO - Usuario eliminado: ID={instance.pk}, username='{instance.username}'")

