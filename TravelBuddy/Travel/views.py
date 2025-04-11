from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Route, Category, User
from .forms import RouteForm, LoginForm, UserForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('travel:index')
        elif form.data['username'] != '' and form.data['password'] != '':
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('travel:index')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('travel:login')

def index(request):
    return render(request, 'index.html')

@login_required
def routes(request):
    user_routes = Route.objects.filter(user_id=request.user)
    print(user_routes)
    return render(request, 'routes.html', {'routes': user_routes})

@login_required
def edit_route(request, route_id):
    if route_id != 0:
        route = get_object_or_404(Route, id=route_id, user_id=request.user)
        if request.method == 'POST':
            form = RouteForm(request.POST, instance=route)
            if form.is_valid():
                form.save()
                return redirect('travel:routes')
        else:
            form = RouteForm(instance=route)
        return render(request, 'edit-route.html', {'form': form})
    else:
        if request.method == 'POST':
            form = RouteForm(request.POST)
            if form.is_valid():
                route = form.save(commit=False)
                route.user_id = request.user
                route.save()
                return redirect('travel:routes')
        else:
            form = RouteForm()
        return render(request, 'edit-route.html', {'form': form})

@login_required
def delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id, user_id=request.user)
    if request.method == 'POST':
        route.delete()
        return redirect('travel:routes')
    return render(request, 'routes.html')

@login_required
def analytics(request):
    return render(request, 'analytics.html')

@login_required
def settings(request):
    return render(request, 'settings.html')
