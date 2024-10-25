'use strict';



// element toggle function
const elementToggleFunc = function (elem) { elem.classList.toggle("active"); }



// sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// sidebar toggle functionality for mobile
sidebarBtn.addEventListener("click", function () { elementToggleFunc(sidebar); });



// testimonials variables
const testimonialsItem = document.querySelectorAll("[data-testimonials-item]");
const modalContainer = document.querySelector("[data-modal-container]");
const modalCloseBtn = document.querySelector("[data-modal-close-btn]");
const overlay = document.querySelector("[data-overlay]");

// modal variable
const modalImg = document.querySelector("[data-modal-img]");
const modalTitle = document.querySelector("[data-modal-title]");
const modalText = document.querySelector("[data-modal-text]");

// modal toggle function
const testimonialsModalFunc = function () {
  modalContainer.classList.toggle("active");
  overlay.classList.toggle("active");
}

// add click event to all modal items
for (let i = 0; i < testimonialsItem.length; i++) {

  testimonialsItem[i].addEventListener("click", function () {

    modalImg.src = this.querySelector("[data-testimonials-avatar]").src;
    modalImg.alt = this.querySelector("[data-testimonials-avatar]").alt;
    modalTitle.innerHTML = this.querySelector("[data-testimonials-title]").innerHTML;
    modalText.innerHTML = this.querySelector("[data-testimonials-text]").innerHTML;

    testimonialsModalFunc();

  });

}

// add click event to modal close button
modalCloseBtn.addEventListener("click", testimonialsModalFunc);
overlay.addEventListener("click", testimonialsModalFunc);



// custom select variables
const select = document.querySelector("[data-select]");
const selectItems = document.querySelectorAll("[data-select-item]");
const selectValue = document.querySelector("[data-selecct-value]");
const filterBtn = document.querySelectorAll("[data-filter-btn]");

select.addEventListener("click", function () { elementToggleFunc(this); });

// add event in all select items
for (let i = 0; i < selectItems.length; i++) {
  selectItems[i].addEventListener("click", function () {

    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    elementToggleFunc(select);
    filterFunc(selectedValue);

  });
}

// filter variables
const filterItems = document.querySelectorAll("[data-filter-item]");

const filterFunc = function (selectedValue) {

  for (let i = 0; i < filterItems.length; i++) {

    if (selectedValue === "all") {
      filterItems[i].classList.add("active");
    } else if (selectedValue === filterItems[i].dataset.category) {
      filterItems[i].classList.add("active");
    } else {
      filterItems[i].classList.remove("active");
    }

  }

}

// add event in all filter button items for large screen
let lastClickedBtn = filterBtn[0];

for (let i = 0; i < filterBtn.length; i++) {

  filterBtn[i].addEventListener("click", function () {

    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    filterFunc(selectedValue);

    lastClickedBtn.classList.remove("active");
    this.classList.add("active");
    lastClickedBtn = this;

  });

}



// contact form variables
const form = document.querySelector("[data-form]");
const formInputs = document.querySelectorAll("[data-form-input]");
const formBtn = document.querySelector("[data-form-btn]");

// add event to all form input field
for (let i = 0; i < formInputs.length; i++) {
  formInputs[i].addEventListener("input", function () {

    // check form validation
    if (form.checkValidity()) {
      formBtn.removeAttribute("disabled");
    } else {
      formBtn.setAttribute("disabled", "");
    }

  });
}



// page navigation variables
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

// add event to all nav link
for (let i = 0; i < navigationLinks.length; i++) {
  navigationLinks[i].addEventListener("click", function () {

    for (let i = 0; i < pages.length; i++) {
      if (this.innerHTML.toLowerCase() === pages[i].dataset.page) {
        pages[i].classList.add("active");
        navigationLinks[i].classList.add("active");
        window.scrollTo(0, 0);
      } else {
        pages[i].classList.remove("active");
        navigationLinks[i].classList.remove("active");
      }
    }

  });
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('form[data-form]');
  const cityInput = document.getElementById('city');
  const weatherInfo = document.querySelector('.weather-data');

  // 處理回車鍵按下事件
  cityInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault();  // 阻止表單的默認提交行為
      const city = cityInput.value.trim(); // 確保城市名稱沒有多餘空格

      if (city) {
        // 發送 AJAX 請求到 /get_weather 而不是 /contact
        fetchWeather(city);  // 使用下面定義的 fetchWeather 函數
      } else {
        weatherInfo.innerHTML = `<p>Please enter a city name.</p>`;
      }
    }
  });

  // Function to fetch weather information for a given city
  function fetchWeather(city) {
    fetch('/get_weather', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ city: city }),  // 將用戶輸入的城市發送給後端
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);  // 檢查返回的數據
      if (data.weather) {
        // 更新天氣資訊到頁面
        weatherInfo.innerHTML = `
          <div class="weather-info-row">
                    <div class="city-info">
                        <img src="/assets/images/landmark.ico" alt="landmark" class="icon">
                        <span>${data.weather.city}</span>
                    </div>
                </div>
                <div class="weather-info-row">
                    <div class="temperature-info">
                        <img src="/assets/images/celsius.ico" alt="celsius" class="icon">
                        <span>${data.weather.temperature}°C</span>
                    </div>
                </div>
                <div class="weather-info-row">
                    <div class="description-info">
                        <img src="/assets/images/condition.ico" alt="condition" class="icon">
                        <span>${data.weather.description}</span>
                    </div>
                </div>
            `;
      } else if (data.error) {
        weatherInfo.innerHTML = `<p>${data.error}</p>`;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      weatherInfo.innerHTML = `<p>Error fetching weather data.</p>`;
    });
  }
});



