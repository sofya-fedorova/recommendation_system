document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('myForm');
    const login = document.getElementById('login');
    const password = document.getElementById('password');
    const btn_enter = document.getElementById('btn_enter');
    const validForm = document.getElementById('validForm');

    if(validForm.innerHTML == 'Неверный логин.'){
        login.style.borderColor = 'red';
        btn_enter.style.marginTop = '10px';
    }
    else{
        login.style.borderColor = '';
    }
    if(validForm.innerHTML == 'Неверный пароль.'){
        password.style.borderColor = 'red';
        btn_enter.style.marginTop = '10px';
        validForm.style.display = '';
    }
    else{
        password.style.borderColor = '';
    }
});