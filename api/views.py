from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, HobbyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Hobby

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            new_hobbies = request.POST.get('new_hobby')
            if new_hobbies:
                hobby_names = [hobby.strip() for hobby in new_hobbies.split(',')]
                for hobby_name in hobby_names:
                    hobby, created = Hobby.objects.get_or_create(name=hobby_name)
                    user.save()
                    user.hobbies.add(hobby)
            else:
                user.save()
            form.save_m2m()
            login(request, user)
            return redirect('main_spa')
    else:
        form = UserCreationForm()
    return render(request, 'api/spa/signup.html', {'form': form})

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_spa')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        hobby_form = HobbyForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
        
        if hobby_form.is_valid():
            hobby = hobby_form.save()
            request.user.hobbies.add(hobby)
            return redirect('profile')
    else:
        user_form = UserChangeForm(instance=request.user)
        hobby_form = HobbyForm()
    return render(
        request,
        'profile.html',
        {'user_form': user_form, 'hobby_form': hobby_form})

@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})
