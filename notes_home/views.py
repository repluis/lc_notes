from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib import messages
from notes_home.forms import RegisterForm
from notes_home.services.auth_service import AuthService


@login_required
def home(request):
    return render(request, 'notes_home/home.html')


def logout_view(request):
    """
    Vista personalizada de logout que funciona con GET y POST
    """
    if request.user.is_authenticated:
        django_logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


def register(request):
    """
    Vista de registro de usuarios usando el servicio de autenticación
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            auth_service = AuthService()
            # Acceder directamente a cleaned_data sin .get() para asegurar que los datos estén presentes
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            
            # Log temporal para depuración
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"LOG VISTA - username: {username}, email: {email}, password type: {type(password)}, password length: {len(password) if password else 0}, password value: {'***' if password else 'EMPTY'}, password_confirm length: {len(password_confirm) if password_confirm else 0}")
            
            user, errors = auth_service.register_user(
                username=username,
                email=email,
                password=password,
                password_confirm=password_confirm
            )
            
            if user and not errors:
                # Autenticar al usuario después del registro
                from django.contrib.auth import authenticate
                django_user = authenticate(username=username, password=password)
                if django_user:
                    django_login(request, django_user)
                    messages.success(request, f'¡Bienvenido {username}! Tu cuenta ha sido creada exitosamente.')
                    return redirect('home')
                else:
                    messages.success(request, 'Tu cuenta ha sido creada. Por favor inicia sesión.')
                    return redirect('login')
            else:
                # Mostrar errores del servicio
                for error in errors:
                    messages.error(request, error)
        else:
            # Mostrar errores del formulario
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'notes_home/register.html', {'form': form})