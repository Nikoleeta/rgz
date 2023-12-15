function showMore() {
    var cards = document.getElementsByClassName("card-container");
    var visibleCards = 0;
  
    // Считаем видимые карточки
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i];
      if (card.style.display !== "none") {
        visibleCards++;
      }
    }
    
    // Показываем следующие 20 карточек
    for (var j = visibleCards; j < visibleCards + 20 && j < cards.length; j++) {
      cards[j].style.display = "block";
    }
  }
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