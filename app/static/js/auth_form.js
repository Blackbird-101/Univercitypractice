// Проверяем текущий URL
const currentUrl = window.location.pathname;

if (currentUrl === '/auth/' || currentUrl === '/auth') {
    document.addEventListener('DOMContentLoaded', function() {
        // Получаем элементы
        const authForm = document.querySelector('.b-auth-modal__form');
        
        if (!authForm) {
            console.error('Форма авторизации не найдена');
            return;
        }

        // Обработчик формы
        authForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Валидация полей формы
            const isValid = validateForm(this);
            
            if (isValid) {
                // Если форма валидна - отправляем данные
                handleSubmit(this);
            }
        });

        function validateForm(form) {
            // Получаем значения полей
            const usernameInput = form.querySelector('input[name="nickname"]');
            const passwordInput = form.querySelector('input[name="password"]');
            
            if (!usernameInput || !passwordInput) {
                showError('Не найдены поля формы');
                return false;
            }
            
            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();
            
            if (!username || !password) {
                showError('Все поля обязательны для заполнения');
                return false;
            }
            
            return true;
        }

        function handleSubmit(form) {
            // Собираем данные формы
            const formData = new FormData(form);
            
            // Отправляем POST-запрос
            fetch('/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams(formData)
            })
            .then(response => {
                if (response.ok) {
                    console.log(response)
                    window.location.href = '/index';
                } else {
                    return response.text();
                }
            })
            .then(data => {
                if (!data) return;
                showError(data || 'Ошибка авторизации');
            })
            .catch(error => {
                console.error('Ошибка при отправке формы:', error);
                showError('Произошла ошибка при обработке запроса');
            });
        }

        function showError(message) {
            const errorElement = document.createElement('div');
            errorElement.classList.add('b-auth-modal__error');
            errorElement.textContent = message;
            authForm.insertAdjacentElement('beforeend', errorElement);
        }
    });
}