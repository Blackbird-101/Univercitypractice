document.addEventListener('DOMContentLoaded', function () {
    const items = document.querySelectorAll('.information__item');
    const details = document.querySelector('.czn-contacts');
    const info = document.querySelector('.czn-info');
    const news = document.querySelector('.czn-news');

    items.forEach(item => {
        item.addEventListener('click', function () {
            // Получаем текст из параграфа
            const text = this.querySelector('.text-content').innerText;

            // Обновляем текст в блоке с деталями
            details.querySelector('.information__details-text').innerText = text;

            // Показываем или скрываем блок с деталями c учётом значения text
            if (text == 'Центры службы занятости Москвы') {
                if (!news.classList.contains('czn-news')) {
                    news.classList.add('czn-news');
                }
                if (!info.classList.contains('czn-info')) {
                    info.classList.add('czn-info');
                }

                details.querySelector('.information__details-text').innerText = text;
                if (details.classList.contains('czn-contacts')) {
                    details.classList.remove('czn-contacts');
                } else {
                    details.classList.add('czn-contacts');
                }
            }

            if (text == 'Полезные материалы') {
                if (!news.classList.contains('czn-news')) {
                    news.classList.add('czn-news');
                }
                if (!details.classList.contains('czn-contacts')) {
                    details.classList.add('czn-contacts');
                }

                info.querySelector('.information__details-text').innerText = text;
                if (info.classList.contains('czn-info')) {
                    info.classList.remove('czn-info');
                } else {
                    info.classList.add('czn-info');
                }
            }

            if (text == 'Новости в сфере трудоустройства') {
                if (!details.classList.contains('czn-contacts')) {
                    details.classList.add('czn-contacts');
                }
                if (!info.classList.contains('czn-info')) {
                    info.classList.add('czn-info');
                }

                news.querySelector('.information__details-text').innerText = text;
                if (news.classList.contains('czn-news')) {
                    news.classList.remove('czn-news');
                } else {
                    news.classList.add('czn-news');
                }
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

    // form.addEventListener('submit', (e) => {
    //     e.preventDefault();
    //     sendMessages.classList.add('send-messages_hidden');
    // });
});
