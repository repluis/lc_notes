from django.apps import AppConfig


class NotesHomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes_home'
    
    def ready(self):
        """Registra las señales cuando la aplicación está lista"""
        import notes_home.middleware  # Importa las señales para que se registren