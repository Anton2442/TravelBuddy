from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Route, Category, User
from .forms import RouteForm, LoginForm, UserForm, ProfileEditForm, PasswordChangeForm

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
    return render(request, 'routes.html', {'routes': user_routes, 'categories': Category.objects.all()})

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
    

@login_required
def change_favourite(request, route_id):
    try:
        route = get_object_or_404(Route, id=route_id, user_id=request.user)
        route.favorite = not route.favorite
        route.save()
        return JsonResponse({
            'status': 'success',
            'favorite': route.favorite
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def analytics(request):
    user_routes = Route.objects.filter(user_id=request.user)
    
    # Если нет маршрутов, возвращаем пустые значения
    if not user_routes.exists():
        return render(request, 'analytics.html', {
            'max_cost': 0,
            'min_cost': 0,
            'average_cost': 0,
            'favorite_category': None,
            'favorite_category_count': 0,
            'routes_count': 0,
            'last_route': None,
            'routes_last_month': 0
        })
    
    max_cost = max(route.cost for route in user_routes)
    min_cost = min(route.cost for route in user_routes)
    average_cost = sum(route.cost for route in user_routes) / len(user_routes)
    
    # Получаем количество маршрутов для каждой категории
    category_counts = {}
    for route in user_routes:
        category_counts[route.category_id] = category_counts.get(route.category_id, 0) + 1
    
    # Находим категорию с максимальным количеством маршрутов
    favorite_category = max(category_counts.items(), key=lambda x: x[1])[0]
    favorite_category_count = category_counts[favorite_category]
    
    # Подсчет маршрутов за последний месяц
    month_ago = timezone.now() - timedelta(days=30)
    routes_last_month = user_routes.filter(date__gte=month_ago).count()
    
    routes_count = len(user_routes)
    last_route = user_routes.order_by('-date').first()
    
    return render(request, 'analytics.html', {
        'max_cost': max_cost,
        'min_cost': min_cost,
        'average_cost': average_cost,
        'favorite_category': favorite_category,
        'favorite_category_count': favorite_category_count,
        'routes_count': routes_count,
        'last_route': last_route,
        'routes_last_month': routes_last_month
    })

@login_required
def settings(request):
    profile_form = ProfileEditForm(instance=request.user)
    password_form = PasswordChangeForm()

    if request.method == 'POST':
        if 'user_name' in request.POST:
            # Форма личных данных
            profile_form = ProfileEditForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Личные данные успешно обновлены')
                return redirect('travel:settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
        else:
            # Форма смены пароля
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                current_password = password_form.cleaned_data['current_password']
                new_password1 = password_form.cleaned_data['new_password1']
                
                if authenticate(login=request.user.login, password=current_password):
                    request.user.set_password(new_password1)
                    request.user.save()
                    
                    # Обновляем сессию пользователя
                    user = authenticate(login=request.user.login, password=new_password1)
                    login(request, user)
                    
                    messages.success(request, 'Пароль успешно изменен')
                    return redirect('travel:settings')
                else:
                    messages.error(request, 'Неверный текущий пароль')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
    
    return render(request, 'settings.html', {
        'form': profile_form,
        'password_form': password_form
    })

@login_required
def delete_user(request):
    request.user.delete()
    logout(request)
    return redirect('travel:login')
