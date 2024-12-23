from datetime import timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.timezone import now
from .forms import UserCreationForm, UserChangeForm, HobbyForm
from .models import User

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
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_spa')
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

@login_required
def similar_view(request):
    # Get query parameters
    age_min = request.GET.get('age_min', None)
    age_max = request.GET.get('age_max', None)
    page_number = request.GET.get('page', 1)

    # Start with all users annotated with common hobbies
    users = User.objects.annotate(
        common_hobbies=Count('hobbies')
    ).exclude(id=request.user.id)  # Exclude the currently logged-in user
    users = users.order_by('-common_hobbies')

    # Convert age range to date_of_birth range
    if age_min or age_max:
        today = now().date()

        if age_min:
            min_date_of_birth = today - timedelta(days=int(age_min) * 365.25)
        else:
            min_date_of_birth = None  # No lower limit

        if age_max:
            max_date_of_birth = today - timedelta(days=int(age_max) * 365.25)
        else:
            max_date_of_birth = None  # No upper limit

        # Apply the date_of_birth filter
        if min_date_of_birth and max_date_of_birth:
            users = users.filter(date_of_birth__range=[max_date_of_birth, min_date_of_birth])
        elif min_date_of_birth:
            users = users.filter(date_of_birth__lte=min_date_of_birth)
        elif max_date_of_birth:
            users = users.filter(date_of_birth__gte=max_date_of_birth)

    # Paginate the results
    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page_number)

    # Prepare the data for JSON response
    users_data = [
        {
            'name': user.name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'common_hobbies': user.common_hobbies,
        }
        for user in page_obj
    ]

    return JsonResponse({
        'users': users_data,
        'page': page_number,
        'num_pages': paginator.num_pages,
    })