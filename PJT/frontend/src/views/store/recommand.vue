<template>
  <v-card>
    <v-container fluid grid-list-xl>
      <v-layout justify-center row wrap x12 md8>
        <v-flex>
          <v-row dense>
            <v-col v-for="(store,i) in randomStores" :key="store.id" :cols="12">
              <StoreRecomandCard
                :id="store.id"
                :index="i+1"
                :name="store.name"
                :categories="store.categories"
                :address="store.address"
                :tel="store.tel"
                :image="store.image"
              />
            </v-col>
          </v-row>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
import { mapState, mapActions } from "vuex";
import StoreRecomandCard from "@/components/StoreRecomandCard";
export default {
  components: {
    StoreRecomandCard
  },
  data(){
    return{
      storeList:[],
      randomStores:[],
    }
  },
  computed: {
    ...mapState({
      store: state => state.data.store,
      stores: state => state.data.TFIDFStoreList
    })
  },
  mounted() {
    this.storeList = this.stores
    this.getRecommand();
    this.selectRandom();
  },
  methods:{
    ...mapActions("data",["storeRecomm","getRecommand"]),
    async getRecommand() {
      if(this.randomStores.length ==0 || this.storeList.length ==0){
        const params = {
          store: this.store.id
        };
        await this.storeRecomm(params);
      }
    },
    selectRandom(){
      for(let i=0;i<20;i++){
        const max = this.storeList.length;
        const index = Math.floor(Math.random()*max);
        this.randomStores.push(this.storeList[index]);
        this.storeList.splice(index,1);
      }
    },
  }
};
</script>
