<template>
  <v-card>
    <v-container>
      <v-card class="mx-auto my-12">
        <div id="map" class="text-center" style="width:100%;height:300px;" />
        <v-card-title class="display-1">{{ this.store.name }}</v-card-title>

        <v-card-text>
          <v-row align="center" class="mx-0">
            <v-rating
              :value="getReviewAvg"
              color="yellow darken-3"
              background-color="yellow darken-3"
              dense
              half-increments
              readonly
              size="20"
            />

            <div class="grey--text ml-5">{{ getReviewAvg }} ({{ this.getReviewCount }})</div>
          </v-row>

          <br />
          <div v-if="store.address !=''" class="subtitle-1 font-weight-medium">
            <v-icon>mdi-map-marker-outline</v-icon>
            {{ store.address }}
          </div>
          <div v-if="store.tel != ''" class="subtitle-1 font-weight-medium">
            <v-icon>mdi-notebook-outline</v-icon>
            {{ store.tel }}
          </div>
          <div v-if="tags !=''" class="subtitle-1 font-weight-medium">
            <v-icon>mdi-tag-outline</v-icon>
            {{ tags }}
          </div>
          <div v-if="bhour.length !=0" class="subtitle-1 font-weight-medium">
            <v-icon>mdi-clock-outline</v-icon>
            <span>{{ bhour[0].start_time.substring(0,5) }} ~ {{ bhour[0].end_time.substring(0,5) }}</span>
            <span v-if="bhour[0].etc !=''">({{ bhour[0].etc }})</span>
          </div>
        </v-card-text>
        <br />

        <v-flex v-if="menus.length !=0" xs12>
          <v-divider />
          <StoreMenu :menus="menus" />
        </v-flex>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import StoreMenu from "@/components/StoreMenu";
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  components: {
    StoreMenu
  },
  computed: {
    ...mapState({
      store: state => state.data.store,
      menus: state => state.data.storeMenuList,
      bhour: state => state.data.bhour
    }),
    ...mapGetters("data", ["getReviewCount", "getReviewAvg"]),
    tags: function() {
      return this.store.categories.reduce((acc, v) => {
        return `${acc} #${v}`;
      }, "");
    }
  },
  mounted() {
    this.sid = this.$route.params.id;
    this.getStoreInfo();
    this.getReview();
    this.getMenu();
    this.getBhour();
    this.getRecommand();
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
  },
  methods: {
    ...mapActions("data", [
      "storeReviews",
      "getOneStore",
      "storeMenu",
      "storeBhour",
      "storeRecomm"
    ]),
    async getStoreInfo() {
      const params = {
        id: this.sid
      };
      await this.getOneStore(params);
      window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
    },
    async getReview() {
      const params = {
        id: this.sid,
        page: 1,
        append: false
      };
      await this.storeReviews(params);
      this.loading = false;
    },
    async loadMore() {
      this.loading = true;
      const params = {
        id: this.sid,
        page: this.page,
        append: true
      };
      await this.storeReviews(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    async getMenu() {
      const params = {
        store: this.sid
      };
      await this.storeMenu(params);
    },
    async getBhour() {
      const params = {
        store: this.sid
      };
      await this.storeBhour(params);
    },
    async getRecommand() {
      const params = {
        store: this.sid
      };
      await this.storeRecomm(params);
    },
    initMap() {
      var container = document.getElementById("map");
      var options = {
        center: new kakao.maps.LatLng(this.store.lat, this.store.lng),
        level: 3
      };
      var map = new kakao.maps.Map(container, options);
      //마커추가하려면 객체를 아래와 같이 하나 만든다.
      var marker = new kakao.maps.Marker({ position: map.getCenter() });
      marker.setMap(map);
    },
    addScript() {
      const script = document.createElement("script"); /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=56abc3abfda9ad4b66eda2d0eea73a7e";
      document.head.appendChild(script);
    }
  }
};
</script>

<style></style>
