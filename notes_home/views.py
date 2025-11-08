from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib import messages
from notes_home.forms import RegisterForm, NoteForm
from notes_home.services.auth_service import AuthService
from notes_home.services.note_service import NoteService


@login_required
def home(request):
    """Vista principal que muestra la lista de notas del usuario"""
    note_service = NoteService()
    notes, errors = note_service.get_all_notes(request.user.id, include_archived=False)
    
    if errors:
        for error in errors:
            messages.error(request, error)
    
    return render(request, 'notes_home/home.html', {'notes': notes})


@login_required
def note_create(request):
    """Vista para crear una nueva nota"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note_service = NoteService()
            note, errors = note_service.create_note(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                user_id=request.user.id
            )
            
            if note and not errors:
                messages.success(request, 'Nota creada exitosamente.')
                return redirect('note_detail', note_id=note.id)
            else:
                for error in errors:
                    messages.error(request, error)
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')
    else:
        form = NoteForm()
    
    return render(request, 'notes_home/note_form.html', {'form': form, 'action': 'Crear'})


@login_required
def note_detail(request, note_id):
    """Vista para ver el detalle de una nota"""
    note_service = NoteService()
    note, errors = note_service.get_note(note_id, request.user.id)
    
    if errors or not note:
        for error in errors:
            messages.error(request, error)
        return redirect('home')
    
    return render(request, 'notes_home/note_detail.html', {'note': note})


@login_required
def note_edit(request, note_id):
    """Vista para editar una nota existente"""
    note_service = NoteService()
    note, errors = note_service.get_note(note_id, request.user.id)
    
    if errors or not note:
        for error in errors:
            messages.error(request, error)
        return redirect('home')
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            updated_note, update_errors = note_service.update_note(
                note_id=note_id,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                user_id=request.user.id,
                is_archived=form.cleaned_data.get('is_archived', False)
            )
            
            if updated_note and not update_errors:
                messages.success(request, 'Nota actualizada exitosamente.')
                return redirect('note_detail', note_id=note_id)
            else:
                for error in update_errors:
                    messages.error(request, error)
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')
    else:
        form = NoteForm(initial={
            'title': note.title,
            'content': note.content,
            'is_archived': note.is_archived
        })
    
    return render(request, 'notes_home/note_form.html', {'form': form, 'note': note, 'action': 'Editar'})


@login_required
def note_delete(request, note_id):
    """Vista para eliminar una nota"""
    if request.method == 'POST':
        note_service = NoteService()
        deleted, errors = note_service.delete_note(note_id, request.user.id)
        
        if deleted and not errors:
            messages.success(request, 'Nota eliminada exitosamente.')
        else:
            for error in errors:
                messages.error(request, error)
    
    return redirect('home')


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