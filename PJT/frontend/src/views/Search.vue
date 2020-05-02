<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center row wrap mt-5>
        <v-flex xs12 md8>
          <card title="맛집 검색">
            <v-form>
              <v-container py-0>
                <v-layout row>
                  <v-flex 3 xs3 md>
                    <v-select
                      v-model="selectedOption"
                      item-text="text"
                      item-value="value"
                      :items="options"
                      label="검색조건"
                    />
                  </v-flex>
                  <v-flex xs8 md8>
                    <v-text-field v-model="searchWord" label="검색어" @keyup.enter="onSubmit" />
                  </v-flex>
                  <v-flex xs1 md1 align-self-center>
                    <!-- Modal 부분 -->
                    <v-row justify="center">
                      <v-dialog v-model="dialog" persistent max-width="500">
                        <template v-slot:activator="{ on }">
                          <v-btn
                            class="indigo white--text"
                            color="blue-grey lighten-2"
                            v-on="on"
                            rounded
                          >
                            <v-icon>mdi-cog</v-icon>
                          </v-btn>
                        </template>
                        <v-card>
                          <v-card-title class="headline">검색옵션</v-card-title>

                          <v-card-text mx-10>
                            <v-slider v-model="count" min="0" max="100" label="최소리뷰" thumb-label />
                            <v-text-field v-model="count" label="개수" />
                          </v-card-text>
                          <v-card-actions>
                            <v-spacer />
                            <v-btn color="primary" text @click="dialog = false">적용</v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>
                    </v-row>
                    <!-- Modal 부분 -->
                  </v-flex>

                  <v-flex xs12 text-center>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="orange lighten-2"
                      @click="onSubmit"
                    >
                      <v-icon>mdi-magnify</v-icon>검색
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </card>
          <v-divider class="mx-4" />
        </v-flex>

        <v-flex xs12 md8>
          <!-- <v-layout justify-center row wrap x12 md8> -->
          <v-row dense>
            <v-col v-for="store in stores" :key="store.id" :cols="6" pa-4>
              <store-list-card
                :id="store.id"
                :name="store.name"
                :categories="store.categories"
                :address="store.address"
                :tel="store.tel"
                :image="store.image"
              />
            </v-col>
          </v-row>

          <!-- </v-layout>   -->
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Card from "@/components/Card";
import StoreListCard from "@/components/StoreListCard";
import { mapState, mapActions, mapMutations } from "vuex";
export default {
  components: {
    Card,
    StoreListCard
  },
  // created(){
  //   this.clearStoreList();
  // },
  data: () => ({
    dialog: false,
    count: 0,
    searchWord: "",
    selectedOption: "name",
    options: [
      {
        text: "이름",
        value: "name"
      },
      {
        text: "주소",
        value: "address"
      },
      {
        text: "카테고리",
        value: "category"
      }
    ],
    loading: true
  }),
  computed: {
    ...mapState({
      stores: state => state.data.storeSearchList,
      page: state => state.data.resultPage,
      reviewCnt: state => state.app.reviewCnt,
      currentUser: state => state.data.currentUser,
    })
  },
  mounted(){
    this.checkLogin();
  }
  ,
  methods: {
    ...mapActions("data", ["getStores","getUser"]),
    ...mapMutations("data", ["clearStoreList"]),
    getUserInfo() {
      this.getUser(sessionStorage.userId);
    },
    checkLogin() {
      if(sessionStorage.userId != null && this.currentUser.token =='')
        this.getUserInfo();
    },
    onSubmit: async function() {
      let params = {
        name: "",
        address: "",
        category: "",
        count: this.count - 1,
        page: 1,
        append: false
      };
      if (this.selectedOption === "name") {
        params.name = this.searchWord;
      } else if (this.selectedOption === "address") {
        params.address = this.searchWord;
      } else {
        params.category = this.searchWord;
      }
      await this.getStores(params);
      this.loading = false;
    },
    loadMore: async function() {
      this.loading = true;
      let params = {
        name: "",
        address: "",
        category: "",
        page: this.page,
        append: true
      };
      if (this.selectedOption === "name") {
        params.name = this.searchWord;
      } else if (this.selectedOption === "address") {
        params.address = this.searchWord;
      } else {
        params.category = this.searchWord;
      }
      await this.getStores(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    }
  }
};
</script>
