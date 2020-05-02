<template>
  <v-card height="100%" @click="$router.push({name: 'about', params: { id: id}})">
    <v-container>
      <v-row justify="space-between">
        <v-col cols="3">
          <v-img :src="image" contain />
        </v-col>

        <v-col>
          <v-row class="flex-column ma-0 fill-height" justify="center">
            <v-col>
              <div class="headline font-weight-bold">{{index}}. {{ name }}</div>
              <div class="font-weight-light">{{ tags }}</div>
            </v-col>

            <v-col>
              <div class="font--gray subtitle-2 font-weight-light">
                <v-icon>mdi-map-marker-outline</v-icon>
                {{ address }}
              </div>
              <div v-if="tel != ''" class="subtitle-2 font-weight-light">
                <v-icon>mdi-notebook-outline</v-icon>
                {{ tel }}
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    index: {
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
