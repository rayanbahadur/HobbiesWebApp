"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import views

from .views import main_spa, search_users

## TODO, any access to pages after login should be protected by login_required
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('similar/', views.similar_view, name='similar'),
    path('profile/', views.profile_view, name='profile'),
    path('hobbies/', views.hobbies_view, name='hobbies'),
    path('', login_required(main_spa), name='main_spa'),
    # Friend Request URLs
    path('friend-requests/', views.list_friend_requests, name='list_friend_requests'),
    path('friend-requests/send/', views.send_friend_request, name='send_friend_request'),
    path('friend-requests/accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-requests/reject/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),

    # Friends and Search URLs
    path('friends/', views.list_friends, name='list_friends'),
    path('search/', search_users, name='search_users'),

]
