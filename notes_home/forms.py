"""
Formularios de la aplicación
"""
from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    """
    Formulario de registro de usuarios
    """
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre de usuario'
        }),
        help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        }),
        help_text='La contraseña debe tener al menos 8 caracteres.'
    )
    
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repita su contraseña'
        }),
        help_text='Ingrese la misma contraseña para verificación.'
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Validar que solo contenga caracteres permitidos
            from django.contrib.auth.validators import UnicodeUsernameValidator
            validator = UnicodeUsernameValidator()
            try:
                validator(username)
            except ValidationError:
                raise forms.ValidationError(
                    'El nombre de usuario solo puede contener letras, números y @/./+/-/_'
                )
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('La contraseña es requerida.')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        # Retornar la contraseña sin modificar
        return password
    
    def clean_password_confirm(self):
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password_confirm:
            raise forms.ValidationError('La confirmación de contraseña es requerida.')
        return password_confirm
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Solo validar coincidencia si ambos están presentes
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError({
                    'password_confirm': 'Las contraseñas no coinciden.'
                })
        elif password and not password_confirm:
            raise forms.ValidationError({
                'password_confirm': 'Por favor confirme su contraseña.'
            })
        elif not password and password_confirm:
            raise forms.ValidationError({
                'password': 'Por favor ingrese su contraseña.'
            })
        
        return cleaned_data

