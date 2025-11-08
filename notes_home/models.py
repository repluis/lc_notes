from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Note(models.Model):
    """
    Modelo de Nota
    Representa una nota creada por un usuario
    """
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', verbose_name='Usuario')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    is_archived = models.BooleanField(default=False, verbose_name='Archivada')
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['user', 'is_archived']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
