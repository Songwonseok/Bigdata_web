<template>
  <v-container fluid grid-list-xl>
    <card title="맛집추천">
      <v-layout justify-center row wrap x12 md8>
        <!--  -->
        <v-row dense>
          <!-- <v-col v-for="store in stores" :key="store.id" :cols="6" pa-4>
            <store-list-card
              :id="store.id"
              :name="store.name"
              :categories="store.categories"
              :address="store.address"
              :tel="store.tel"
              :image="store.image"
            />
          </v-col> -->

          <!-- 일단 20개씩 -->
          <v-col v-for="i in 10" :key="i" :cols="6" pa-4>
            <store-list-card
              :id="stores[i-1].id"
              :name="stores[i-1].name"
              :categories="stores[i-1].categories"
              :address="stores[i-1].address"
              :tel="stores[i-1].tel"
              :image="stores[i-1].image"
            />
          </v-col>
        </v-row>
      </v-layout>
    </card>
  </v-container>
</template>

<script>
import Card from "@/components/Card";
import StoreListCard from "@/components/StoreListCard";
import { mapActions, mapState } from "vuex";
export default {
  components: {
    Card,
    StoreListCard
  },
  computed: {
    ...mapState({
      stores: state => state.data.KNNStoreList,
      currentUser: state=> state.data.currentUser
    })
  },
  mounted() {
    this.checkLogin();
  },
  methods: {
    ...mapActions("data", ["getKNN","getUser"]),
    checkLogin() {
      if (sessionStorage.userId == null)
        this.$router.push("/login");
      else {
        console.log("KNN")
        this.getStores();
        if(sessionStorage.userId != null && this.currentUser.token =='')
          this.getUserInfo();
        }
    },
    getStores: async function() {
      const params = {
        user: sessionStorage.userId,
        page: 1,
        append: false
      };
      if (this.stores.length == 0) {
        await this.getKNN(params);
      }
    },
    getUserInfo() {
      this.getUser(sessionStorage.userId);
    },
  }
};
</script>
