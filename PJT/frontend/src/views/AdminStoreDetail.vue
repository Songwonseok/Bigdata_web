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
                      <p class="display-1 font-weight-bold">
                        {{ store.name }}
                      </p>
                    </v-card-text>
                    <v-card xs10 md10>
                      <v-img :src="store.image" aspect-ratio="2" contain />
                      <span class="title font-weight-bold">
                        <v-icon large color="yellow darken-2">mdi-star</v-icon>
                        4.5
                      </span>
                    </v-card>
                    <v-footer color="white">
                      <v-col class="text-center">
                        <p class="subtitle-1 font-italic">{{ tags }}</p>

                        <span class="font-weight-thin">{{
                          store.address
                        }}</span>
                        <p class="font-weight-thin">📞 {{ store.tel }}</p>
                      </v-col>
                    </v-footer>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </card>

          <v-divider class="mx-4" />
        </v-flex>
        <v-flex xs12 md8>
          <v-tabs v-model="tab" background-color="orange lighten-2" fixed-tabs>
            <v-tab key="menu">
              메뉴 관리
            </v-tab>
            <v-tab key="review">
              리뷰 관리
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item key="menu">
              <v-flex v-if="menus.length > 0">
                <StoreMenu :menus="menus" />
              </v-flex>
            </v-tab-item>
            <v-tab-item key="review">
              <v-flex xs12>
                <v-row dense>
                  <v-col v-for="review in reviews" :key="review.id" cols="6">
                    <admin-review-card
                      :id="review.id"
                      :total_score="review.total_score"
                      :content="review.content"
                      :reg_time="review.reg_time"
                      :store_id="review.store_id"
                      :user_id="review.user_id"
                    />
                  </v-col>
                </v-row>
              </v-flex>
            </v-tab-item>
          </v-tabs-items>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Card from "@/components/Card";
import AdminReviewCard from "@/components/AdminReviewCard";
import StoreMenu from "@/components/StoreMenu";
import { mapState, mapActions } from "vuex";
export default {
  components: {
    Card,
    AdminReviewCard,
    StoreMenu,
  },
  data: () => ({
    tab: null,
    sid: "",
    loading: true,
    e1: "recent",
  }),
  computed: {
    ...mapState({
      store: (state) => state.data.store,
      reviews: (state) => state.data.storeReviewList,
      page: (state) => state.data.resultPage,
      menus: (state) => state.data.storeMenuList,
      currentUser: (state) => state.data.currentUser,
    }),
    tags: function() {
      return this.store.categories.reduce((acc, v) => {
        return `${acc} #${v}`;
      }, "");
    },
  },
  mounted() {
    this.sid = this.$route.params.id;
    this.getStoreInfo();
    this.getReview();
    this.getMenu();
  },
  methods: {
    ...mapActions("data", ["storeReviews", "getOneStore", "storeMenu"]),
    async getStoreInfo() {
      const params = {
        id: this.sid,
      };
      await this.getOneStore(params);
    },
    async getReview() {
      const params = {
        id: this.sid,
        page: 1,
        append: false,
      };
      await this.storeReviews(params);
      this.loading = false;
    },
    async loadMore() {
      this.loading = true;
      const params = {
        id: this.sid,
        page: this.page,
        append: true,
      };
      await this.storeReviews(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    async getMenu() {
      const params = {
        store: this.sid,
      };
      await this.storeMenu(params);
    },
  },
};
</script>
