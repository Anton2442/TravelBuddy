from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise TypeError('Users must have a login.')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
    login = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'login'

    objects = CustomUserManager()
    
    def __str__(self):
        return self.user_name + f' ({self.login})'

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    descripton = models.TextField()

class Route(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=30)
    attractions = models.TextField()
    date = models.DateField()
    cost = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    favorite = models.BooleanField()


class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_id')