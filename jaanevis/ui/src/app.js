const { createApp } = Vue;
import './main.css';

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
      baseUrl: process.env.API_URL,
      panelView: "create",
      note: {
        code: "",
        creator: "",
        country: "",
        text: "",
        url: "",
        lat: "0.0",
        long: "0.0"
      },
      errors: [],
      authenticated: false,
      editing: false,
      authUser: {username: ""},
      filters: {},
    }
  },
  watch:{
    '$route.query': async function (to, from){
      if (JSON.stringify(from) == JSON.stringify(to))
        return;
      if (this.$route.path == "/notes"){
        this.handleNotesPath();
      }
    },
  },
  methods: {
    initMap: function () {
      const initLat = 32.0
      const initLong = 52.0
      this.map = L.map('map').setView([initLat, initLong], 5);

      var southWest = L.latLng(-89.98155760646617, -180),
          northEast = L.latLng(89.99346179538875, 180);
      var bounds = L.latLngBounds(southWest, northEast);

      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxBoundsViscosity: 1.0,
          maxZoom: 8,
          minZoom: 2,
          attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(this.map);
      this.map.on('click', this.showNoteCreateForm);
      this.map.setMaxBounds(bounds);
    },
    onEachFeature: function (feature, layer) {
      var creator = feature.properties.creator;
      var country = feature.properties.country;
      var urlTextShort = this.urlText(feature.properties.url)
      var content = `
          <p><b>creator</b>: <a href="#/notes?creator=${creator}">${creator}</a></p>
          <span><b>link</b>: </span>
          <a target="_blank" href="${feature.properties.url}">${urlTextShort}</a>
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
        text: this.note.text,
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
        text: this.note.text,
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
        country: properties.country,
        url: properties.url,
        text: properties.text,
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
        country: "",
        url: "",
        text: "",
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
      this.errors = []

      if (this.username && this.password)
        return true;

      if (!this.username)
        this.errors.push('Username is mandatory.');

      if (!this.password)
        this.errors.push('Password is mandatory.');
    },
    checkRegisterForm: function (e) {
      this.errors = [];

      if (!this.username)
        this.errors.push('Username is mandatory.');

      if (!this.password)
        this.errors.push('Password is mandatory.');

      if (!this.password2)
        this.errors.push('Password confirmation is mandatory.');

      if (this.password != this.password2)
        this.errors.push('Passwords do not match');

      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      var emailValid = re.test(this.username);
      if (!emailValid)
        this.errors.push('Invalid email address.');

      if (this.errors.length){
        return false;
      }
      return true;
    },
    login: async function () {
      if (!this.checkLoginForm())
        return;

      let loginData = {
        username: this.username,
        password: this.password,
      };
      const response = await fetch(this.baseUrl + "/user/login", {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
      })
      .then(async response => {
        if (response.ok)
          return response.json();
        const js = await response.json();
        return Promise.reject(js);
      })
      .then(data => {
        this.authUser.username = loginData.username;
        this.authenticated = true;
        this.$cookies.set("username", loginData.username);
        this.panelView = 'create';
      })
      .catch(error => {
        console.log("Login error", error);
        this.errors.push(error.message)
        return;
      });
    },
    logout: async function () {
      const response = await fetch(this.baseUrl + "/user/logout", {
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
    register: async function () {
      if (!this.checkRegisterForm())
        return;

      let registerData = {
        email: this.username,
        password: this.password,
      };
      const response = await fetch(this.baseUrl + "/user/register", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(registerData)
      })
      .then(async response => {
        if (response.ok)
          return response.json();
        const js = await response.json();
        return Promise.reject(js);
      })
      .then(data => {
        this.panelView = 'create';
        alert("Register successful");
      })
      .catch(error => {
        console.log("Register error", error);
        this.errors.push(error.message);
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
    showRegister: function () {
      this.panelView = 'register';
    },
    handleNotesPath: async function () {
      this.filters = {...this.filters, ...this.$route.query};
      var notes = await this.readNotes(this.filters);
      this.$root.showNotesOnMap(notes);
      this.$router.replace({
        path: this.$route.path,
        query: this.filters
      });
    },
    removeFilter(filter) {
      delete this.filters[filter];
      this.$router.replace({
        path: this.$route.path,
        query: this.filters
      });
    },
    hashtagText: function (text) {
      var repl = text.replace(/#([^\d&%$-]\S{2,49})/g, '<a href="#/notes?tag=$1">#$1</a>');
      return repl;
    },
    urlText: function (text, maxLength = 50) {
      var shortText = text.slice(0, maxLength);
      return shortText + ((shortText.length == text.length) ? "" : "...")
    }
  },
  mounted() {
    this.$cookies = window.$cookies;
    this.initAuth();
    this.initMap();
    this.showNotesOnMap();
  },
}).use(router).mount('#app')
