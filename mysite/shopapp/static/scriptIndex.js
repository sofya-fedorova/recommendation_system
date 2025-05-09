//document.addEventListener('DOMContentLoaded', function () {
const form = document.getElementById('myForm');
const emailInput = document.getElementById('email');
const placeOfWorkInput = document.getElementById('placeOfWork');
const postInput = document.getElementById('post');
let flag = 0;

// Функция для проверки валидности email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).trim().toLowerCase());
}

// Функция для проверки на пустоту
function checkEmpty(input) {
    if (input.value.trim() === '') {
        return false;
    } else {
        return true;
    }
}

// Слушатель события отправки формы
form.addEventListener('submit', function (event) {
    event.preventDefault();

    // Проверка email
    if (!validateEmail(emailInput.value) || !checkEmpty(emailInput)) {
        emailInput.style.borderColor = 'red';
        flag = 1 // Прекращаем выполнение функции, если email невалидный
    }
    else{
        emailInput.style.borderColor = '';
    }

    if (!checkEmpty(placeOfWorkInput)) {
        placeOfWorkInput.style.borderColor = 'red';
        flag = 2 // Прекращаем выполнение функции, если email невалидный
    }
    else{
        placeOfWorkInput.style.borderColor = '';
    }

    if (postInput.value === '') {
        postInput.style.borderColor = 'red';
        flag = 3 // Прекращаем выполнение функции, если email невалидный
    }
    else{
        postInput.style.borderColor = '';
    }

    if(flag !== 0){
        alert("Проверьте заполнение формы!");
        flag = 0;
        return;
    }

    // Если проверка прошла успешно, позволяем форме отправляться
    form.submit(); // Убрали условие внутри else, чтобы избежать рекурсии
});
