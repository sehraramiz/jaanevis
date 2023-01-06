const { createApp } = Vue;

createApp({
  name: 'Jaanevis',
  data() {
    return {
      title: 'Jaanevis',
      version: '0.0.1',
      baseUrl: 'http://127.0.0.1:8000',
      panelView: "details",
      note: {
        code: "code",
        creator: "default",
        url: "",
        lat: "0.0",
        long: "0.0"
      }
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
      this.map.on('click', this.showNoteCreateForm);
    },
    onEachFeature: function (feature, layer) {
      var content = `
          <p><b>creator</b>: ${feature.properties.creator}</p>
          <span><b>link</b>: </span>
          <a target="_blank" href="${feature.properties.url}">${feature.properties.url}</a>
      `;
      layer.on('click', this.showNoteDetailsForm);
      if (feature.properties && feature.properties.creator) {
          layer.bindPopup(content);
      }
    },
    clearMapNotes: function () {
      if (this.notesLayer)
        this.notesLayer.clearLayers();
    },
    showNotesOnMap: async function () {
      this.clearMapNotes();

      let notes = await this.readNotes();

      var notesCollection = {
          'type': 'FeatureCollection',
          'features': notes
      };
      this.notesLayer = L.geoJSON(notesCollection, {
          pointToLayer: function (feature, latlng) {
              return L.circleMarker(latlng, {});
          },
          onEachFeature: this.onEachFeature,
      }).addTo(this.map);
    },
    readNotes: async function () {
      let url = this.baseUrl + '/note/geojson';
      const response = await fetch(url);
      return await response.json();
    },
    createNewNote: async function () {
      let note = {
        url: this.note.url,
        lat: this.note.lat,
        long: this.note.long
      };
      const response = await fetch(this.baseUrl + "/note", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(note)
      });
      const content = await response.json();
      this.showNotesOnMap();
      alert("Note created!");
    },
    deleteNote: async function () {
      const response = await fetch(this.baseUrl + `/note/${this.note.code}`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
        },
      });
      const content = await response.json();
      this.showNotesOnMap();
      alert("Note deleted!");
    },
    updateNote: async function () {
      let note = {
        url: this.note.url,
        lat: this.note.lat,
        long: this.note.long
      };
      const response = await fetch(this.baseUrl + `/note/${this.note.code}`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(note)
      });
      const content = await response.json();
      this.showNotesOnMap();
      alert("Note updated!");
    },
    showNoteDetailsForm: function (e) {
      this.panelView = 'details';
      var properties = e.target.feature.properties;
      this.note = {
        code: properties.code,
        creator: properties.creator,
        url: properties.url,
        lat: e.latlng.lat,
        long: e.latlng.lng,
      };
    },
    showNoteCreateForm: function (e) {
      this.panelView = 'create';
      this.note = {
        code: "",
        creator: "",
        url: "",
        lat: e.latlng.lat,
        long: e.latlng.lng
      }
    },
  },
  mounted() {
    this.initMap();
    this.showNotesOnMap();
  },
}).mount('#app')
