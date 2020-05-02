<template>
  <v-card
    height="100%"
    @click="$router.push({ name: 'adminStoreDetail', params: { id: id } })"
  >
    <v-card-text class="text-center">
      <p class="headline font-weight-bold">{{ name }}</p>
      <v-img :src="image" aspect-ratio="2" contain />
      <p class="subtitle-1 font-italic">{{ tags }}</p>
    </v-card-text>
    <v-footer color="white">
      <v-col class="text-center">
        <span class="grey--text caption font-italic">{{ address }} / 📞 {{ tel }}</span>
      </v-col>
    </v-footer>
  </v-card>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    name: {
      type: String,
      default: ""
    },
    categories: {
      type: Array,
      default: () => new Array()
    },
    address: {
      type: String,
      default: ""
    },
    tel: {
      type: String,
      default: ""
    },
    image: {
      type: String,
      default: ""
    }
  },
  computed: {
    tags: function() {
      return this.categories.reduce((acc, v) => {
        return `${acc} #${v}`;
      }, "");
    }
  }
};
</script>
