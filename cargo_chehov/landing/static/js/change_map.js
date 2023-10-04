document.addEventListener('DOMContentLoaded', function () {
    function resizeMap() {
        var mapElement = document.getElementById("map");
        var windowWidth = window.innerWidth;

        if (windowWidth <= 350) {
          mapElement.classList.remove("smallMap_540");
          mapElement.classList.remove("smallMap_600");
          mapElement.classList.add("smallMap_350");
        } else if (windowWidth <= 545) {
          mapElement.classList.remove("smallMap_350");
          mapElement.classList.remove("smallMap_600");
          mapElement.classList.add("smallMap_540");
        } else if (windowWidth <= 767) {
          mapElement.classList.remove("smallMap_350");
          mapElement.classList.remove("smallMap_540");
          mapElement.classList.add("smallMap_600");
        } else {
          mapElement.className = "map"; // Восстановление класса по умолчанию
        }
      }

      // Слушаем событие изменения размера окна
      window.addEventListener("resize", resizeMap);

      // Вызываем функцию при загрузке страницы
      window.addEventListener("load", resizeMap);
});