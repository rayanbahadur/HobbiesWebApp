from datetime import timedelta, datetime
import json
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, HobbyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.timezone import now
from .forms import UserCreationForm, UserChangeForm, CustomPasswordChangeForm
from .models import User, Hobby, Friendship, FriendRequest

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            existing_hobbies = form.cleaned_data.get('hobbies', [])
            user.hobbies.add(*existing_hobbies)  # Combine both new and selected hobbies
            
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
def profile_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == "POST":
        data = request.POST.copy()
        for field in ['name', 'email', 'date_of_birth']:
            if field not in data:
                data[field] = getattr(user, field)
        hobbies = request.POST.getlist('hobbies')
        if hobbies:
            data.setlist('hobbies', hobbies)
        else:
            data.setlist('hobbies', list(user.hobbies.values_list('id', flat=True)))

        new_hobby = request.POST.get('new_hobby')
        if new_hobby:
            hobby_names = [hobby.strip().capitalize() for hobby in new_hobby.split(',')]
            for hobby_name in hobby_names:
                hobby, created = Hobby.objects.get_or_create(name=hobby_name)
                user.hobbies.add(hobby)
                data.appendlist('hobbies', hobby.id)

        form = UserChangeForm(data, instance=user)
        password_form = CustomPasswordChangeForm(data)
        
        if form.is_valid() and (not data.get('new_password1') or password_form.is_valid()):
            form.save()
            if data.get('new_password1'):
                password_form.save(user)
                update_session_auth_hash(request, user)  # Re-authenticate the user

            existing_hobbies = form.cleaned_data.get('hobbies', [])
            user.hobbies.add(*existing_hobbies)  # Combine both new and selected hobbies

            return JsonResponse({"status": "success"})
        else:
            errors = form.errors.copy()
            errors.update(password_form.errors)
            return JsonResponse({"status": "error", "errors": errors}, status=400)
    else:
        user_data = {
            'name': user.name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'hobbies': list(user.hobbies.values('id', 'name')),
        }
        return JsonResponse(user_data)

def hobbies_view(request):
    hobbies = Hobby.objects.all().values('id', 'name')
    return JsonResponse(list(hobbies), safe=False)

@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

@login_required
def similar_view(request):
    # Get query parameters
    age_min = request.GET.get('age_min', None)
    age_max = request.GET.get('age_max', None)
    page_number = request.GET.get('page', 1)

    # Helper function to calculate age from date of birth
    def calculate_age(date_of_birth):
        if not date_of_birth:
            return None
        today = datetime.today().date()
        delta = today - date_of_birth
        return int(delta.days / 365.25)

    # Start with all users annotated with common hobbies
    users = User.objects.annotate(
        common_hobbies=Count('hobbies', filter=Q(hobbies__in=request.user.hobbies.all()))
    ).exclude(id=request.user.id)  # Exclude the currently logged-in user

    # Exclude users with 0 common hobbies
    users = users.filter(common_hobbies__gt=0).order_by('-common_hobbies')

    # Convert age range to filtering logic
    if age_min or age_max:
        filtered_users = []
        for user in users:
            user_age = calculate_age(user.date_of_birth)
            if user_age is None:
                continue
            if age_min and user_age < int(age_min):
                continue
            if age_max and user_age > int(age_max):
                continue
            filtered_users.append(user)
        users = filtered_users  # Replace users with filtered list

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

@login_required
@require_http_methods(["POST"])
def send_friend_request(request):
    try:
        # Parse JSON body
        data = json.loads(request.body)
        to_user_id = data.get('to_user_id')

        if not to_user_id:
            return JsonResponse({"error": "to_user_id is required"}, status=400)

        if request.user.id == int(to_user_id):
            return JsonResponse({"error": "You cannot send a friend request to yourself"}, status=400)

        to_user = User.objects.get(id=to_user_id)

        # Check if the friend request already exists
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return JsonResponse({"error": "Friend request already sent"}, status=400)

        # Check if already friends
        if Friendship.objects.filter(user=request.user, friend=to_user).exists():
            return JsonResponse({"error": "You are already friends"}, status=400)

        # Create the friend request
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return JsonResponse({"message": "Friend request sent"}, status=201)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


@login_required
@require_http_methods(["POST"])
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        # Create friendships for both users
        Friendship.objects.create(user=friend_request.from_user, friend=friend_request.to_user)
        Friendship.objects.create(user=friend_request.to_user, friend=friend_request.from_user)
        friend_request.delete()
        return JsonResponse({"message": "Friend request accepted"}, status=200)
    except FriendRequest.DoesNotExist:
        return JsonResponse({"message": "Friend request not found"}, status=404)


@login_required
@require_http_methods(["POST"])
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        friend_request.delete()
        return JsonResponse({"message": "Friend request rejected"}, status=200)
    except FriendRequest.DoesNotExist:
        return JsonResponse({"message": "Friend request not found"}, status=404)

@login_required
@require_http_methods(["GET"])
def list_friends(request):
    friendships = Friendship.objects.filter(user=request.user)
    friends_data = [
        {"id": friendship.friend.id, "name": friendship.friend.name, "email": friendship.friend.email}
        for friendship in friendships
    ]
    return JsonResponse(friends_data, safe=False, status=200)

@login_required
@require_http_methods(["GET"])
def list_friend_requests(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user).select_related('from_user')
    data = [
        {
            'id': fr.id,
            'from_user': {
                'id': fr.from_user.id,
                'name': fr.from_user.name,
                'email': fr.from_user.email,
            },
            'created_at': fr.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for fr in friend_requests
    ]
    return JsonResponse(data, safe=False)

@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()  # Get the query parameter
    if not query:
        return JsonResponse({"message": "No search query provided"}, status=400)

    # Search for users by name or email
    users = User.objects.filter(
        name__icontains=query  # You can also add `| email__icontains=query` for email search
    ).exclude(id=request.user.id)  # Exclude the logged-in user

    # Prepare response data
    user_data = [
        {"id": user.id, "username": user.name, "email": user.email}
        for user in users
    ]

    return JsonResponse(user_data, safe=False)