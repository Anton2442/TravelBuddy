document.addEventListener('DOMContentLoaded', function() {
    const themeChanger = document.getElementById('ThemeChanger');
    const themeIcon = document.getElementById('ThemeIcon');
    const body = document.body;

    // Функция для установки темы
    function setTheme(isDark) {
        if (isDark) {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            themeIcon.src = "{% static 'images/Icons/LightTheme.svg' %}";
        } else {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
            themeIcon.src = "{% static 'images/Icons/DarkTheme.svg' %}";
        }
        // Сохраняем предпочтение в localStorage
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    // Проверяем сохранённую тему при загрузке страницы
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme === 'dark');
    } else {
        // Если тема не сохранена, используем системные настройки
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark);
    }

    // Обработчик клика по кнопке смены темы
    themeChanger.addEventListener('click', function() {
        const isDark = body.classList.contains('light-theme');
        setTheme(isDark);
    });

    // Слушаем изменения системной темы
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches);
        }
    });
});