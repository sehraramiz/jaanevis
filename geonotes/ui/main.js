const initLat = 29.6147
const initLong = 52.5043
const map = L.map('map').setView([initLat, initLong], 5);
const baseUrl = 'http://127.0.0.1:8000';

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 10,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function onEachFeature(feature, layer) {
    var content = `
        <p><b>creator</b>: ${feature.properties.creator}</p>
        <span><b>link</b>: </span>
        <a target="_blank" href="${feature.properties.url}">${feature.properties.url}</a>
    `;
    if (feature.properties && feature.properties.creator) {
        layer.bindPopup(content);
    }
}

async function showNotesOnMap() {
    let url = baseUrl + '/note/geojson';
    const response = await fetch(url)
    const notes = await response.json()

    var notesCollection = {
        'type': 'FeatureCollection',
        'features': notes
    }

    L.geoJSON(notesCollection, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {});
        },
        onEachFeature: onEachFeature
    }).addTo(map);
}

showNotesOnMap(baseUrl);
