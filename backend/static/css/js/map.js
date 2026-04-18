document.addEventListener("DOMContentLoaded", function () {
    // Создаём карту и ставим центр на Бишкек
    var map = L.map("map").setView([42.8746, 74.5698], 7);

    // Подключаем слой OpenStreetMap
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    // Пример маркеров
    var crafts = [
        { name: "Шырдак", coords: [42.0, 75.0], desc: "Традиционный войлочный ковёр" },
        { name: "Кузнечное дело", coords: [41.5, 72.5], desc: "Изготовление инструментов и украшений" },
        { name: "Резьба по дереву", coords: [43.0, 76.0], desc: "Декоративные изделия из дерева" }
    ];

    crafts.forEach(function (craft) {
        L.marker(craft.coords).addTo(map)
            .bindPopup("<b>" + craft.name + "</b><br>" + craft.desc);
    });
});
