from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Route, Favorite, Category
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
        labels = {
            'route_name':'Название маршрута',
            'attractions':'Достопримечательности',
            'date':'Дата',
            'cost':'Стоимость',
            'category_id':'Категория',
            'favorite':'Избранный'
        }
        widgets = {
            'route_name': forms.TextInput(attrs={'class': 'form-control'}),
            'attractions': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].empty_label = "Выберите категорию"

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['route_id']
        widgets = {
            'route_id': forms.Select(attrs={'class': 'form-control'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email', 'dark_theme']
        labels = {
            'user_name': 'Имя пользователя',
            'email': 'Email',
            'dark_theme': 'Тёмная тема',
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'dark_theme': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пароль'}),
        required=True
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}),
        required=True
    )
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Новые пароли не совпадают')
        
        return cleaned_data 