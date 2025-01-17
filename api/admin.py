from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Hobby, FriendRequest, Friendship
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'name', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('email', 'name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'date_of_birth', 'hobbies')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'date_of_birth', 'hobbies', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

class HobbyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# FriendRequest Admin
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    search_fields = ('from_user__email', 'to_user__email')
    list_filter = ('created_at',)

# Friendship Admin
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'created_at')
    search_fields = ('user__email', 'friend__email')
    list_filter = ('created_at',)

# Register models in the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Hobby, HobbyAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friendship, FriendshipAdmin)
