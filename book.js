const cardsContainer = document.querySelector('.card-container');
const showMoreBtn = document.getElementById('show-more');
const cardsPerPage = 20;

// скрыть все карточки, кроме первых 20
cardsContainer.querySelectorAll('.card').forEach((card, index) => {
  if (index >= cardsPerPage) {
    card.style.display = 'none';
  }
});

let currentIndex = cardsPerPage;

function showCards() {
  const cardsToShow = cardsContainer.querySelectorAll('.card');

  // скрыть предыдущие 20 карточек
  for (let i = currentIndex - cardsPerPage; i < currentIndex; i++) {
    if (cardsToShow[i]) {
      cardsToShow[i].style.display = 'none';
    }
  }

  // показать следующие 20 карточек
  for (let i = currentIndex; i < currentIndex + cardsPerPage; i++) {
    if (cardsToShow[i]) {
      cardsToShow[i].style.display = 'block';
    }
  }

  // обновляем индекс текущей позиции
  currentIndex += cardsPerPage;

  // скрываем кнопку, если показаны все карточки
  if (currentIndex >= cardsToShow.length) {
    showMoreBtn.style.display = 'none';
  }
}

// добавляем обработчик клика на кнопку "Показать еще"
showMoreBtn.addEventListener('click', showCards);






// document.getElementById("filter-form").addEventListener("submit", function(event) {
//     event.preventDefault();
    
//     var book = document.getElementById("book-filter").value;
//     var author = document.getElementById("author-filter").value;
//     var pages = document.getElementById("pages-filter").value;
//     var publisher = document.getElementById("publisher-filter").value;
    
//     var xhr = new XMLHttpRequest();
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 var cardContainer = document.querySelector(".card-container");
//                 cardContainer.innerHTML = xhr.responseText;
//             } else {
//                 console.log("Error: " + xhr.status);
//             }
//         }
//     };
    
//     xhr.open("GET", "/filter-books?book=" + book + "&author=" + author + "&pages=" + pages + "&publisher=" + publisher, true);
//     xhr.send();
// });