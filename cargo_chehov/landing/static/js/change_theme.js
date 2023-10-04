document.addEventListener('DOMContentLoaded', function() {
    $(document).ready(function() {
        // Функция для переключения темы и сохранения её в localStorage
        function toggleTheme() {
            if ($('body').hasClass('dark-mode')) {
                // Темная тема
                $('body').removeClass('dark-mode');
                localStorage.setItem('theme', 'light');
            } else {
                // Светлая тема
                $('body').addClass('dark-mode');
                localStorage.setItem('theme', 'dark');
            }
        }

        // Попытка получить сохраненную тему из localStorage
        var savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            $('body').addClass('dark-mode');
            // Добавляем атрибут к элементу body при темной теме
            $('body').attr('data-layout-mode', 'dark');
        } else {
            $('body').removeClass('dark-mode');
            // Удаляем атрибут при светлой теме
            $('body').removeAttr('data-layout-mode');
        }

        // Добавляем обработчик клика на кнопку переключения темы
        $('#mode').on('click', function() {
            toggleTheme();
        });
    });
});
