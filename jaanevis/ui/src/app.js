const { createApp } = Vue;
import './main.css';
import fa from "./locales/fa.json";
import en from "./locales/en.json";
import NoteItem from './components/NoteItem.js'


var routes = [];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes,
})

const i18n = VueI18n.createI18n({
  locale: 'fa',
  fallbackLocale: 'en',
  messages: {fa, en},
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
      authUser: {username: ""},
      filters: {},
      supportedLocales: process.env.SUPPORTED_LOCALES.split(",")
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
    '$i18n.locale': function (newLocale){
      document.querySelector("html").setAttribute("lang", newLocale)
    },
    'panelView': function (){this.errors = []},
    'latLng': function (){
      // set this offset to set map center a little lower on smaller screens
      // to show map marker in top section of viewport (above the bottom panel)
      const offset = 100 / this.map.getZoom() ** 2
      this.map.panTo(new L.LatLng(this.note.lat - offset, this.note.long), 5);
      this.showPointer(this.note.lat, this.note.long);
    }
  },
  computed: {
    direction () {
      return this.$i18n.locale !== 'fa' ? 'ltr' : 'rtl'
    },
    latLng () {
      return this.note.lat + this.note.long;
    }
  },
  components: {
    NoteItem
  },
  methods: {
    initMap: function () {
      const initLat = 32.0
      const initLong = 52.0
      this.map = L.map(
        'map', {
          zoomControl: false,
          attributionControl: false
        }
      ).setView([initLat, initLong], 5);

      var southWest = L.latLng(-100.98155760646617, -180),
          northEast = L.latLng(89.99346179538875, 180);
      var bounds = L.latLngBounds(southWest, northEast);

      var mapWatermark = `
          <a href="https://t.me/jaanevis">Telegram</a> |
          &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>
        `
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          //maxBoundsViscosity: 1.0,
          maxZoom: 8,
          minZoom: 2,
          attribution: mapWatermark
      }).addTo(this.map);
      L.control.attribution({
        position: 'topright'
      }).addTo(this.map);
      L.control.zoom({
          position: 'topright'
      }).addTo(this.map);
      this.map.on('click', this.showNoteCreateForm);
      //this.map.setMaxBounds(bounds);
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
      const response = await fetch(
        url,
        {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accept-Language': this.$i18n.locale
          }
        }
      );
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
          'Content-Type': 'application/json',
          'Accept-Language': this.$i18n.locale
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
          'Accept-Language': this.$i18n.locale
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
          'Content-Type': 'application/json',
          'Accept-Language': this.$i18n.locale
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
      this.openPanel();
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

      this.panelView = 'create';
      this.openPanel();
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
        this.errors.push(this.$t('invalidLat'));

      if (!validLong)
        this.errors.push(this.$t('invalidLong'));
    },
    clearErrors: function () {
      this.errors = [];
    },
    checkLoginForm: function (e) {
      this.errors = []

      if (this.username && this.password)
        return true;

      if (!this.username)
        this.errors.push(this.$t('requiredUsername'));

      if (!this.password)
        this.errors.push(this.$t('requiredPassword'));
    },
    checkRegisterForm: function (e) {
      this.errors = [];

      if (!this.username)
        this.errors.push(this.$t('requiredUsername'));

      if (!this.email)
        this.errors.push(this.$t('requiredEmail'));

      if (!this.password)
        this.errors.push(this.$t('requiredPassword'));

      if (!this.password2)
        this.errors.push(this.$t('requiredConfirmPassword'));

      if (this.password != this.password2)
        this.errors.push(this.$t('passwordsNotMatch'));

      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      var emailValid = re.test(this.email);
      if (!emailValid)
        this.errors.push(this.$t('invalidEmail'));

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
          'Content-Type': 'application/json',
          'Accept-Language': this.$i18n.locale
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
          'Content-Type': 'application/json',
          'Accept-Language': this.$i18n.locale
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
        email: this.email,
        username: this.username,
        password: this.password,
      };
      const response = await fetch(this.baseUrl + "/user/register", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Accept-Language': this.$i18n.locale
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
    updateAccount: async function () {
      const response = await fetch(this.baseUrl + `/user/own`, {
        method: 'PUT',
        credentials: "include",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Accept-Language': this.$i18n.locale
        },
        body: JSON.stringify({"username": this.authUser.username})
      })
      .then(response => {
        if (!response.ok)
          return Promise.reject(response);
        return response.json();
      })
      .then(data => {
        this.showNotesOnMap();
        alert("Account updated!");
      })
      .catch(error => {
        console.log("Acccount update error", error);
        return;
      });
    },
    initAuth: function () {
      if (this.$cookies.get("username")) {
        this.authenticated = true;
        this.authUser.username = this.$cookies.get("username");
      }
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
    urlText: function (text, maxLength = 50) {
      var shortText = text.slice(0, maxLength);
      return shortText + ((shortText.length == text.length) ? "" : "...")
    },
    togglePanel: function () {
      const panel = document.querySelector('.panel');
      panel.classList.toggle('panel_small');
    },
    openPanel: function () {
      const panel = document.querySelector('.panel');
      if (panel.classList.contains("panel_small"))
        panel.classList.toggle('panel_small');
    }
  },
  mounted() {
    this.$cookies = window.$cookies;
    this.initAuth();
    this.initMap();
    this.showNotesOnMap();
    if (!this.supportedLocales)
      this.supportedLocales = this.$i18n.availableLocales;
  },
}).use(router)
  .use(i18n)
  .mount('#app')
