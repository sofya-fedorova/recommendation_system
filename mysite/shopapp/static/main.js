function validateForm(lenListComp) {

    const radioButtons = document.querySelectorAll('input[type="radio"]');
    let atLeastOneSelected = false;

    let sum = 0

    radioButtons.forEach(radioButton => {
        if (radioButton.checked) {
            sum += 1
        }
    });

    if (sum === lenListComp) {
        downloadDev();
        return true;
    } else {
        alert("Выбраны не все компетенции!");
        return false;
    }
}

let screenHeight = window.innerHeight;
const pageHeight = Math.max(
    document.documentElement.scrollHeight,
    document.body.scrollHeight,
    window.innerHeight
);

function downloadDev(){
    // Делаем элементы видимыми
    document.getElementById('hiddenElements').style.display = 'flex';
    document.getElementById('hiddenElements').style.marginTop = String(pageHeight - screenHeight)+ 'px';
    // Блокируем прокрутку экрана
    document.body.classList.add('noScroll');
}


// Получаем элементы слайдера
const slider = document.querySelector('.slider');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
const slides = Array.from(slider.querySelectorAll('.blockVac'));
const slideCount = slides.length;
let slideIndex = 0;

// Устанавливаем обработчики событий для кнопок
prevButton.addEventListener('click', showPreviousSlide);
nextButton.addEventListener('click', showNextSlide);

// Функция для показа предыдущего слайда
function showPreviousSlide() {
  slideIndex = (slideIndex - 1 + slideCount) % slideCount;
  updateSlider();
}

// Функция для показа следующего слайда
function showNextSlide() {
  slideIndex = (slideIndex + 1) % slideCount;
  updateSlider();
}

// Функция для обновления отображения слайдера
function updateSlider() {
  slides.forEach((slide, index) => {
    if (index === slideIndex) {
      slide.style.display = 'block';
    } else {
      slide.style.display = 'none';
    }
  });
}

// Инициализация слайдера
updateSlider();

