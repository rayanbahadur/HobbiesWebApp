from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
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

class UserChangeForm(BaseUserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('name', 'email', 'date_of_birth', 'hobbies')

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
            if 'hobbies' in self.cleaned_data:
                user.hobbies.set(self.cleaned_data['hobbies'])
        return user

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")

        return cleaned_data

    def save(self, user):
        user.set_password(self.cleaned_data["new_password1"])
        user.save()
        return user

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ['name']