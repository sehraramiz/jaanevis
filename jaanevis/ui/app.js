const { createApp } = Vue;

var routes = [];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes,
})

createApp({
  name: 'Jaanevis',
  data() {
    return {
      title: 'Jaanevis',
      version: '0.0.1',
      baseUrl: 'http://127.0.0.1:8000',
      panelView: "create",
      note: {
        code: "",
        creator: "",
        url: "",
        lat: "0.0",
        long: "0.0"
      },
      errors: [],
      authenticated: false,
      authUser: {username: ""},
    }
  },
  watch:{
    '$route': async function (to, from){
      if (this.$route.path == "/notes"){
        this.handleNotesPath();
      }
    },
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
      var creator = feature.properties.creator;
      var content = `
          <p><b>creator</b>: <a href="#/notes?creator=${creator}">${creator}</a></p>
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
    hidePointer: function () {
      if (this.pointer)
        this.map.removeLayer(this.pointer);
    },
    showPointer: function (lat, long) {
      if (this.pointer)
        this.map.removeLayer(this.pointer);
      this.pointer = new L.Marker([lat, long]).addTo(this.map);
    },
    showNotesOnMap: async function (notes) {
      this.clearMapNotes();

      if (!notes){
        var notes = await this.readNotes();
      }

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
      this.hidePointer();
      this.clearErrors();
    },
    readNotes: async function (filters) {
      var params = "";
      if (filters) {
        params = new URLSearchParams(filters).toString();
      }
      let url = this.baseUrl + '/note/geojson?' + params;
      const response = await fetch(url);
      return await response.json();
    },
    createNewNote: async function () {
      if (!this.checkForm())
        return;

      let note = {
        url: this.note.url,
        lat: this.note.lat,
        long: this.note.long
      };
      const response = await fetch(this.baseUrl + "/note", {
        method: 'POST',
        credentials: "include",
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
        credentials: "include",
        headers: {
          'Accept': 'application/json',
        },
      })
      .then(response => {
        if (!response.ok)
          return Promise.reject(response);
        return response.json();
      })
      .then(data => {
        this.showNotesOnMap();
        this.panelView = 'create';
        alert("Note deleted!");
      })
      .catch(error => {
        console.log("Note delete error", error);
        return;
      });
    },
    updateNote: async function () {
      if (!this.checkForm())
        return;

      let note = {
        url: this.note.url,
        lat: this.note.lat,
        long: this.note.long
      };
      const response = await fetch(this.baseUrl + `/note/${this.note.code}`, {
        method: 'PUT',
        credentials: "include",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(note)
      })
      .then(response => {
        if (!response.ok)
          return Promise.reject(response);
        return response.json();
      })
      .then(data => {
        this.showNotesOnMap();
        alert("Note updated!");
      })
      .catch(error => {
        console.log("Note update error", error);
        return;
      });
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
      let lat = e.latlng.lat;
      let long = e.latlng.lng;

      this.showPointer(lat, long);

      this.panelView = 'create';
      this.note = {
        code: "",
        creator: "",
        url: "",
        lat: lat,
        long: long
      }
    },
    checkForm: function (e) {
      // validate url
      var urlError = "";
      try {
        new URL (this.note.url);
      } catch (error) {
         urlError = error;
      }

      // validate lat long
      var lat = this.note.lat, long = this.note.long;
      var validLat = isFinite(lat) && Math.abs(lat) <= 90 && !isNaN(parseFloat(lat));
      var validLong = isFinite(long) && Math.abs(long) <= 180 && !isNaN(parseFloat(long));

      if (!urlError && validLat && validLong)
        return true;

      this.errors = [];

      if (urlError)
        this.errors.push(urlError);

      if (!validLat)
        this.errors.push('Latitude is not valid.');

      if (!validLong)
        this.errors.push('Longitude is not valid.');
    },
    clearErrors: function () {
      this.errors = [];
    },
    checkLoginForm: function (e) {
      if (this.username && this.password)
        return true;

      this.errors = [];

      if (!this.username)
        this.errors.push('Username is mandatory.');

      if (!this.password)
        this.errors.push('Password is mandatory.');
    },
    login: async function () {
      if (!this.checkLoginForm())
        return;

      let loginData = {
        username: this.username,
        password: this.password,
      };
      const response = await fetch(this.baseUrl + "/login", {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
      })
      .then(response => {
        if (!response.ok)
          return Promise.reject(response);
        return response.json();
      })
      .then(data => {
        this.authUser.username = loginData.username;
        this.authenticated = true;
        this.$cookies.set("username", loginData.username);
        this.panelView = 'create';
      })
      .catch(error => {
        console.log("Login error", error);
        return;
      });
    },
    logout: async function () {
      const response = await fetch(this.baseUrl + "/logout", {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
      })
      .then(response => {
        if (!response.ok)
          return Promise.reject(response);
        return response.json();
      })
      .then(data => {
        this.authUser = {username: ""};
        this.authenticated = false;
        this.$cookies.set("username", "");
        this.panelView = 'create';
      })
      .catch(error => {
        console.log("Logout error", error);
        return;
      });
    },
    initAuth: function () {
      if (this.$cookies.get("username")) {
        this.authenticated = true;
        this.authUser.username = this.$cookies.get("username");
      }
    },
    showLogin: function () {
      this.panelView = 'auth';
    },
    handleNotesPath: async function () {
      this.filters = this.$route.query
      var notes = await this.$root.readNotes(this.filters);
      this.$root.showNotesOnMap(notes);
    },
  },
  mounted() {
    this.$cookies = window.$cookies;
    this.initAuth();
    this.initMap();
    this.showNotesOnMap();
  },
}).use(router).mount('#app')

