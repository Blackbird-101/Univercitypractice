// Функция для проверки URL и обработки клика
function handleClickOutside() {
    // Проверяем текущий URL
    const currentUrl = window.location.pathname;
    const allowedUrls = ['/auth', '/register/employer', '/register/user'];
    
    // Если URL не соответствует нужному, выходим из функции
    if (!allowedUrls.includes(currentUrl)) {
        return;
    }

    // Проверяем наличие блока b-auth-modal на странице
    const formBlock = document.querySelector('.b-auth-modal');
    
    // Если блока нет на странице, выходим
    if (!formBlock) {
        return;
    }

    // Добавляем обработчик клика на документ
    document.addEventListener('click', function(event) {
        // Проверяем, был ли клик внутри b-auth-modal
        if (formBlock.contains(event.target)) {
            return; // Если клик был внутри формы, ничего не делаем
        }

        // Здесь ваш код, который должен выполниться при клике вне формы
        console.log('Клик вне формы!');
        window.location.href = '/';
    });
}

// Запускаем функцию при загрузке страницы
document.addEventListener('DOMContentLoaded', handleClickOutside);