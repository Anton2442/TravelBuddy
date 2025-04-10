document.addEventListener('DOMContentLoaded', function() {
    const routesTable = document.getElementById('routes-tbody');
    const noRoutesMessage = document.getElementById('no-routes');
    const categoryFilter = document.getElementById('route-category');
    
    // Пример данных маршрутов (в реальном приложении будут загружаться с сервера)
    let routes = [
        {
            id: 1,
            name: 'Путешествие по Золотому кольцу',
            date: '2024-03-15',
            cost: '25000',
            attractions: 'Суздаль, Владимир, Ярославль',
            category: 'history',
            isFavorite: false
        }
        // Другие маршруты будут добавляться здесь
    ];

    function createFavoriteIcon(isFavorite) {
        return `
            <svg class="favorite-icon ${isFavorite ? 'active' : ''}" viewBox="0 0 24 24">
                <path fill="${isFavorite ? '#FFD700' : '#ccc'}" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
            </svg>
        `;
    }

    function renderRoutes(filteredRoutes = routes) {
        if (filteredRoutes.length === 0) {
            routesTable.innerHTML = '';
            noRoutesMessage.style.display = 'block';
            return;
        }

        noRoutesMessage.style.display = 'none';
        routesTable.innerHTML = filteredRoutes.map(route => `
            <tr data-id="${route.id}">
                <td>${route.name}</td>
                <td>${new Date(route.date).toLocaleDateString('ru-RU')}</td>
                <td>${parseInt(route.cost).toLocaleString('ru-RU')} ₽</td>
                <td>${route.attractions}</td>
                <td class="favorite-cell">${createFavoriteIcon(route.isFavorite)}</td>
            </tr>
        `).join('');

        // Добавляем обработчики для иконок избранного
        document.querySelectorAll('.favorite-icon').forEach(icon => {
            icon.addEventListener('click', function() {
                const row = this.closest('tr');
                const routeId = parseInt(row.dataset.id);
                const route = routes.find(r => r.id === routeId);
                route.isFavorite = !route.isFavorite;
                this.classList.toggle('active');
                this.querySelector('path').setAttribute('fill', route.isFavorite ? '#FFD700' : '#ccc');
            });
        });
    }

    // Обработчик изменения фильтра категории
    categoryFilter.addEventListener('change', function() {
        const selectedCategory = this.value;
        const filteredRoutes = selectedCategory === 'all' 
            ? routes 
            : routes.filter(route => route.category === selectedCategory);
        renderRoutes(filteredRoutes);
    });

    // Инициализация отображения маршрутов
    renderRoutes();
}); 