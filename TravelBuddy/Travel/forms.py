from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Route, Favorite

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['login', 'user_name', 'email', 'password1', 'password2']
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name', 'attractions', 'date', 'cost', 'category_id', 'favorite']
        widgets = {
            'route_name': forms.TextInput(attrs={'class': 'form-control'}),
            'attractions': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['route_id']
        widgets = {
            'route_id': forms.Select(attrs={'class': 'form-control'}),
        } 