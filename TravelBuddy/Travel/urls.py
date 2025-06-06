from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('routes/', views.routes, name='routes'),
    path('routes/edit/<int:route_id>/', views.edit_route, name='edit_route'),
    path('routes/delete/<int:route_id>/', views.delete_route, name='delete_route'),
    path('routes/change_favourite/<int:route_id>/', views.change_favourite, name='change_favourite'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings, name='settings'),
    path('settings/delete_user/', views.delete_user, name='delete_user'),
    path('download-excel/', views.download_excel, name='download_excel'),
] 