const { createApp } = Vue;

createApp({
  name: 'Jaanevis',
  data() {
    return {
      title: 'Jaanevis',
      version: '0.0.1',
      baseUrl: 'http://127.0.0.1:8000',
    }
  },
  methods: {
    initMap: function () {
      const initLat = 29.6147
      const initLong = 52.5043
      this.map = L.map('map').setView([initLat, initLong], 5);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 10,
          attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(this.map);
    },
    onEachFeature: function (feature, layer) {
      var content = `
          <p><b>creator</b>: ${feature.properties.creator}</p>
          <span><b>link</b>: </span>
          <a target="_blank" href="${feature.properties.url}">${feature.properties.url}</a>
      `;
      if (feature.properties && feature.properties.creator) {
          layer.bindPopup(content);
      }
    },
    showNotesOnMap: async function () {
      let url = this.baseUrl + '/note/geojson';
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
          onEachFeature: this.onEachFeature
      }).addTo(this.map);
    }
  },
  mounted() {
    this.initMap();
    this.showNotesOnMap();
  },
}).mount('#app')
