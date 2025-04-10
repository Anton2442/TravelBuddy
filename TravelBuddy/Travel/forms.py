from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Route, Favorite
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Неверный логин или пароль')
        return cleaned_data

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['login', 'user_name', 'email', 'password1', 'password2']
        labels = {
            'login': 'Логин',
            'user_name': 'Имя пользователя',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name', 'attractions', 'date', 'cost', 'category_id', 'favorite']
        widgets = {
            'route_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название маршрута'}),
            'attractions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Достопримечательности'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Дата'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Стоимость'}),
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