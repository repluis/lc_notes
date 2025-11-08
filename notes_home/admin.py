from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from notes_home.models import Note


# Desregistrar el UserAdmin por defecto si ya está registrado
if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuración personalizada del admin para usuarios
    Muestra solo nombre de usuario y correo electrónico
    """
    # Campos a mostrar en la lista - solo username y email
    list_display = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    # Configuración de campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Configuración para agregar nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Configuración del admin para notas
    """
    list_display = ('title', 'user', 'created_at', 'updated_at', 'is_archived')
    list_filter = ('is_archived', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    
    fieldsets = (
        (None, {'fields': ('title', 'content', 'user')}),
        ('Estado', {'fields': ('is_archived',)}),
        ('Fechas', {'fields': ('created_at', 'updated_at')}),
    )
