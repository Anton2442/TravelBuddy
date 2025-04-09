from django.contrib import admin
from .models import User, Category, Route, Favorite

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'user_name', 'email', 'is_staff')
    search_fields = ('login', 'user_name', 'email')
    list_filter = ('is_staff', 'is_superuser')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'descripton')
    search_fields = ('category_name',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'user_id', 'category_id', 'date', 'cost', 'favorite')
    list_filter = ('category_id', 'favorite', 'date')
    search_fields = ('route_name', 'attractions')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'route_id')
    list_filter = ('user_id', 'route_id')
