function hideBlockOnClick() {
    // Получаем кнопку по классу
    const button = document.querySelector('.not-found_button');
    
    // Получаем блок, который нужно скрывать
    const blockToHide = document.querySelector('.not-found');
    
    // Проверяем, существуют ли элементы
    if (button && blockToHide) {
        // Добавляем обработчик клика
        button.addEventListener('click', () => {
            // Скрываем блок
            blockToHide.style.display = 'none';
        });
    } else {
        console.error('Элементы не найдены');
    }
}

// Вызываем функцию при загрузке документа
document.addEventListener('DOMContentLoaded', hideBlockOnClick);