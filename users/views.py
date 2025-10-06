from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUpdateForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # если уже вошёл — на главную

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # <-- тут редирект обязательно
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, 'users/login.html')

@login_required
def profile_view(request):
    user = request.user
    profile_form = ProfileUpdateForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'email' in request.POST or 'bio' in request.POST:
            # обновление профиля
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль успешно обновлён!")
                return redirect('profile')
        elif 'old_password' in request.POST:
            # смена пароля
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль успешно изменён!")
                return redirect('profile')

    return render(request, 'users/profile.html', {
        'user': user,
        'profile_form': profile_form,
        'password_form': password_form,
    })
def logout_view(request):
    logout(request)
    return redirect('login')
