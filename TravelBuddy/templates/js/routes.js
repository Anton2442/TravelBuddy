document.addEventListener('DOMContentLoaded', function() {
    const categoryFilter = document.getElementById('route-category');
    const favoriteFilter = document.getElementById('favorite-filter');
    const routesTable = document.getElementById('routes-tbody');
    const noRoutesMessage = document.getElementById('no-routes');
    
    
    function filterRoutes() {
        const selectedCategory = categoryFilter.value;
        const selectedFavorite = favoriteFilter.value;
        let visibleCount = 0;

        Array.from(routesTable.getElementsByTagName('tr')).forEach(row => {
            const category = row.getAttribute('data-category');
            const isFavorite = row.getAttribute('data-favorite') === 'True';
            
            const categoryMatch = selectedCategory === 'all' || category === selectedCategory;
            
            let favoriteMatch = true;
            if (selectedFavorite === 'favorite') {
                favoriteMatch = isFavorite;
            } else if (selectedFavorite === 'not-favorite') {
                favoriteMatch = !isFavorite;
            }

            if (categoryMatch && favoriteMatch) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        noRoutesMessage.style.display = visibleCount === 0 ? '' : 'none';
    }

    categoryFilter.addEventListener('change', filterRoutes);
    favoriteFilter.addEventListener('change', filterRoutes);

    document.querySelectorAll('.favorite-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const button = this.querySelector('button');
                    const img = button.querySelector('img');
                    const row = this.closest('tr');
                    
                    if (data.favorite) {
                        img.src = '/static/images/Icons/FavouriteFilled.svg';
                        row.setAttribute('data-favorite', 'True');
                    } else {
                        img.src = '/static/images/Icons/Favourite.svg';
                        row.setAttribute('data-favorite', 'False');
                    }
                    
                    filterRoutes();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    filterRoutes();
}); 

document.querySelectorAll('form[action*="change_favourite"]').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                const button = form.querySelector('button');
                const img = button.querySelector('img');
                if (!data.favorite) {
                    img.src = "/templates/images/Icons/Favourite.svg";
                } else {
                    img.src = "/templates/images/Icons/FavouriteFilled.svg";
                }
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Произошла ошибка при изменении статуса избранного');
        }
    });
});