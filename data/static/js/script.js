document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.information__item');
    const details = document.querySelector('.information__details');
    
    items.forEach(item => {
        item.addEventListener('click', function() {
            // Получаем текст из параграфа
            const text = this.querySelector('.text-content').innerText;
            
            // Обновляем текст в блоке с деталями
            details.querySelector('.information__details-text').innerText = text;
            
            // Показываем или скрываем блок с деталями
            if (details.classList.contains('hidden')) {
                details.classList.remove('hidden');
            } else {
                details.classList.add('hidden');
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const sendMessages = document.querySelector('.send-messages');
    const button = document.querySelector('.contacts__button');
    const form = document.querySelector('.send-messages__form');

    button.addEventListener('click', () => {
        if (sendMessages.classList.contains('send-messages_hidden')) {
            sendMessages.classList.remove('send-messages_hidden');
        } else {
            sendMessages.classList.add('send-messages_hidden');
        }
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessages.classList.add('send-messages_hidden');
    });
});
