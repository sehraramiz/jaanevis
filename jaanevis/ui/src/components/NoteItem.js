export default {
  props: {
    note: Object,
    user: Object
  },
  data() {
    return {
      editing: false
    }
  },
  computed: {
    editable() {
      if (this.user)
        return this.user.username == this.note.creator && this.editing;
      return false;
    }
  },
  methods: {
    hashtagText: function (text) {
      var repl = text.replace(/#([^\d&%$-]\S{2,49})/g, '<a href="#/notes?tag=$1">#$1</a>');
      return repl;
    },
  },
  template: `
  <p>{{ $t("code") }}: {{ note.code }}</p>
  <p>{{ $t("creator") }}: <a :href="'#/notes?creator=' + note.creator">{{ note.creator }}</a></p>
  <p>{{ $t("country") }}: <a :href="'#/notes?country=' + note.country">{{ note.country }}</a></p>
  <div v-if="editable">
      <label for="url">{{ $t("url") }}:</label>
      <input type="text" id="url" name="url" v-model="note.url">
      <label for="text">{{ $t("text") }}:</label>
      <textarea rows="2" cols="50" name="text" v-model="note.text"/>
      <label for="lat">{{ $t("latitude") }}:</label>
      <input type="number" step="any" id="lat" name="lat" v-model="note.lat">
      <label for="long">{{ $t("longitude") }}:</label>
      <input type="number" step="any" id="long" name="long" v-model="note.long">
      <div class="btn-group">
          <button @click="$emit('update')">{{ $t("update") }}</button><button @click="$emit('delete')" style="background: #d32f2f">{{ $t("delete") }}</button>
          <button @click="editing = !editing" style="background: #f57c00">{{ $t("cancelEdit") }}</button>
      </div>
  </div>
  <div v-else>
      <p>{{ $t("url") }}: <a target="_blank" :href="note.url">{{ this.$parent.urlText(note.url) }}</a></p>
      <p>{{ $t("text") }}:</p><p v-html="this.hashtagText(note.text)"></p>
      <p>{{ $t("latitude") }}: {{ note.lat }}</p>
      <p>{{ $t("longitude") }}: {{ note.long }}</p>
      <button v-if="user.username == note.creator"
          @click="editing = !editing">{{ $t("edit") }}</button>
    </div>
</div>
  `
}
