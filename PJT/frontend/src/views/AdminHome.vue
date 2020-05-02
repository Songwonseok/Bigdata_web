<template>
  <div class="d-flex flex-column mt-10">
    <div class="pa-2">
      <h1 class="text-center">관리자 페이지 홈</h1>
    </div>
    <v-row align="center" style="height: 600px;">
      <v-col class="mx-auto" cols="3" md="3">
        <MaterialCard color="orange lighten-2" to="/Admin/store">
          <template v-slot:heading>
            <div class="display-5 font-weight-light">
              등록된 상점
            </div>
          </template>
          <v-card class="mx-auto " width="500" height="100">
            <v-card-text class="d-flex flex-column">
              <div class="display-1 text--primary text-center">
                {{ storeCount }} 점포
              </div>
            </v-card-text>
          </v-card>
        </MaterialCard>
      </v-col>
      <v-col class="mx-auto" cols="3" md="3">
        <MaterialCard color="orange lighten-2" to="/Admin/review">
          <template v-slot:heading>
            <div class="display-5 font-weight-light">
              등록된 리뷰
            </div>
          </template>
          <v-card class="mx-auto " width="500" height="100">
            <v-card-text class="d-flex flex-column">
              <div class="display-1 text--primary text-center">
                {{ reviewCount }} 개
              </div>
            </v-card-text>
          </v-card>
        </MaterialCard>
      </v-col>
      <v-col class="mx-auto" cols="3" md="3">
        <MaterialCard color="orange lighten-2" to="/Admin/user">
          <template v-slot:heading>
            <div class="display-5 font-weight-light">
              등록된 회원
            </div>
          </template>
          <v-card class="mx-auto " width="500" height="100">
            <v-card-text class="d-flex flex-column">
              <div class="display-1 text--primary text-center">
                {{ userCount }} 명
              </div>
            </v-card-text>
          </v-card>
        </MaterialCard>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import MaterialCard from "@/components/MaterialCard";
export default {
  components: {
    MaterialCard,
  },
  computed: {
    ...mapState({
      userCount: (state) => state.data.userCount,
      storeCount: (state) => state.data.storeCount,
      reviewCount: (state) => state.data.reviewCount,
    }),
  },
  mounted() {
    this.getCounts();
  },
  methods: {
    ...mapActions("data", ["adminCount"]),
    async getCounts() {
      await this.adminCount();
    },
  },
};
</script>
