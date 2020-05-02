<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center wrap mt-5>
        <v-flex xs12 md8>
          <card title="식당 정보">
            <v-form>
              <v-container py-0>
                <v-layout row>
                  <v-flex xs12 text-center>
                    <v-card-text class="text-center">
                      <p class="display-1 font-weight-bold">{{ store.name }}</p>
                      <span class="title font-weight-bold">
                        <v-icon large color="yellow darken-2">mdi-star</v-icon>
                        {{ getReviewAvg }}
                      </span>
                    </v-card-text>
                    <v-img :src="store.image" aspect-ratio="2" contain />

                    <v-footer color="white">
                      <v-col class="text-center" />
                    </v-footer>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
            <v-card>
              <v-tabs fixed-tabs background-color="orange lighten-2" dark mx-12>
                <v-tab :to="{ name: 'about' }">
                  <v-icon>mdi-storefront</v-icon>정 보
                </v-tab>
                <v-tab :to="{ name: 'reviews' }">
                  <v-icon>mdi-playlist-star</v-icon>
                  리 뷰 ({{ getReviewCount }})
                </v-tab>
                <v-tab :to="{ name: 'recommand' }">
                  <v-icon>mdi-react</v-icon>추 천
                </v-tab>
              </v-tabs>
              <router-view />
            </v-card>
          </card>

          <v-divider class="mx-4" />
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Card from "@/components/Card";
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  components: {
    Card
  },
  data() {
    return {
      loading: false
    };
  },
  computed: {
    ...mapState({
      store: state => state.data.store,
      reviews: state => state.data.storeReviewList,
      page: state => state.data.resultPage,
      currentUser: state => state.data.currentUser
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
    this.checkLogin();
    this.getStoreInfo();
    this.getReview();
    this.getMenu();
    this.getBhour();
    this.getRecommand();
  },
  methods: {
    ...mapActions("data", [
      "storeReviews",
      "getOneStore",
      "storeMenu",
      "storeBhour",
      "storeRecomm",
      "getUser"
    ]),
    getUserInfo() {
      this.getUser(sessionStorage.userId);
    },
    checkLogin() {
      if(sessionStorage.userId != null && this.currentUser.token =='')
        this.getUserInfo();
    },
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
    alt() {
      this.image = require("../assets/images/defaultStore.jpg");
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
    }
  }
};
</script>
