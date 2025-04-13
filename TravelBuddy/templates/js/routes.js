document.addEventListener('DOMContentLoaded', function() {
    const categoryFilter = document.getElementById('route-category');
    const favoriteFilter = document.getElementById('favorite-filter');
    const sortSelect = document.getElementById('sort-select');
    const routesTable = document.getElementById('routes-tbody');
    const noRoutesMessage = document.getElementById('no-routes');
    
    function sortRoutes() {
        const rows = Array.from(routesTable.getElementsByTagName('tr'));
        const sortBy = sortSelect.value;
        
        const visibleRows = rows.filter(row => row.style.display !== 'none');
        
        visibleRows.sort((a, b) => {
            if (sortBy === 'date') {
                const dateA = new Date(a.getAttribute('data-date'));
                const dateB = new Date(b.getAttribute('data-date'));
                return dateB - dateA;
            } else if (sortBy === 'cost') {
                const costA = parseFloat(a.getAttribute('data-cost'));
                const costB = parseFloat(b.getAttribute('data-cost'));
                return costB - costA;
            }
            return 0;
        });

        const hiddenRows = rows.filter(row => row.style.display === 'none');
        
        while (routesTable.firstChild) {
            routesTable.removeChild(routesTable.firstChild);
        }
        
        visibleRows.forEach(row => routesTable.appendChild(row));
        
        hiddenRows.forEach(row => routesTable.appendChild(row));
    }

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

    categoryFilter.addEventListener('change', () => {
        filterRoutes();
        sortRoutes();
    });
    
    favoriteFilter.addEventListener('change', () => {
        filterRoutes();
        sortRoutes();
    });
    
    if (sortSelect) {
        sortSelect.addEventListener('change', sortRoutes);
    }

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
                        img.src = '/templates/images/Icons/FavouriteFilled.svg';
                        row.setAttribute('data-favorite', 'True');
                    } else {
                        img.src = '/templates/images/Icons/Favourite.svg';
                        row.setAttribute('data-favorite', 'False');
                    }
                    
                    filterRoutes();
                    sortRoutes();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    filterRoutes();
    sortRoutes();

    const downloadBtn = document.getElementById('download-excel');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            const table = document.getElementById('routes-table');
            if (!table) {
                console.error('Table not found');
                return;
            }

            const rows = Array.from(table.querySelectorAll('tbody tr:not([style*="display: none"])'));
            const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
            
            const data = rows.map(row => {
                const cells = Array.from(row.querySelectorAll('td'));
                return cells.map(cell => cell.textContent.trim());
            });

            fetch('/download-excel/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    headers: headers,
                    data: data
                })
            })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'routes.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            })
            .catch(error => console.error('Error:', error));
        });
    }
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