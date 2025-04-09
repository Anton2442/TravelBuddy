from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise TypeError('Users must have a login.')
        
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'user_name']

    objects = CustomUserManager()
    
    def __str__(self):
        return self.user_name + f' ({self.login})'

    def has_module_perms(self, _):
        return self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'Users'

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    descripton = models.TextField()

    REQUIRED_FIELDS = ['category_name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'Categories'

class Route(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=30)
    attractions = models.TextField()
    date = models.DateField()
    cost = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['user_id', 'route_name', 'date']

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'
        db_table = 'Routes'

class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_id')

    REQUIRED_FIELDS = ['user_id', 'route_id']

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        db_table = 'Favorites'