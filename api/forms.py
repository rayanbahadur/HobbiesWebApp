from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import User, Hobby

class UserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )
    class Meta:
        model = User
        fields = ('name', 'email', 'date_of_birth', 'hobbies', 'password1', 'password2')

    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Hobbies"
        )
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.cleaned_data['hobbies'] and user.hobbies.set(self.cleaned_data['hobbies'])
        return user



class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')

class UserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('name', 'email', 'date_of_birth', 'hobbies')

    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label="Hobbies"
        )
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.cleaned_data['hobbies'] and user.hobbies.set(self.cleaned_data['hobbies'])
        return user

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ['name']