<template>
  <div infinite-scroll-disabled="loading" infinite-scroll-distance="10">
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center row wrap mt-5>
        <v-flex xs12 md8>
          <MaterialCard color="orange lighten-2">
            <template v-slot:heading>
              <div class="display-5 font-weight-light">
                리뷰 관리
              </div>
            </template>

            <v-form>
              <v-container py-0>
                <v-layout row>
                  <v-flex xs12 text-center>
                    <template v-if="reviews.length > 0">
                      <v-btn
                        large
                        class="indigo white--text ma-5"
                        rounded
                        color="orange lighten-1"
                        @click="onSubmitt"
                      >
                        <v-icon>mdi-chevron-double-left</v-icon>
                        이전
                      </v-btn>
                    </template>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="orange lighten-1"
                      @click="onSubmit"
                    >
                      <v-icon>mdi-chevron-double-right</v-icon>
                      다음
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </MaterialCard>
          <v-divider class="mx-4" />
        </v-flex>

        <v-flex xs12 md8>
          <!-- <v-layout justify-center row wrap x12 md8> -->
          <v-row dense>
            <v-col v-for="(review, index) in reviews" :key="index" cols="6">
              <v-card class="mx-auto">
                <v-card-text>
                  <v-icon>mdi-account-circle</v-icon>
                  User_{{ review.user }} 등록일 : {{ review.reg_time }}
                  <v-btn color="red" text class="float-right">
                    <v-icon>mdi-trash-can</v-icon>
                  </v-btn>
                </v-card-text>

                <v-card-text>
                  <star-rating
                    v-model="review.score"
                    :star-size="20"
                    :border-width="3"
                    border-color="#d8d8d8"
                    :rounded-corners="true"
                    :star-points="[
                      23,
                      2,
                      14,
                      17,
                      0,
                      19,
                      10,
                      34,
                      7,
                      50,
                      23,
                      43,
                      38,
                      50,
                      36,
                      34,
                      46,
                      19,
                      31,
                      17,
                    ]"
                  />
                </v-card-text>

                <v-card-text class="text--primary">
                  <v-textarea
                    v-model="review.content"
                    value="reviseContent"
                    auto-grow
                    disabled
                  />
                </v-card-text>
                <v-spacer />

                <v-card-actions>
                  <v-spacer />
                  <v-btn color="orange" text @click="blind(index)">
                    블라인드
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>

          <!-- </v-layout>   -->
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import MaterialCard from "@/components/MaterialCard";
import StarRating from "vue-star-rating";
import { mapState, mapActions } from "vuex";
export default {
  components: {
    MaterialCard,
    StarRating,
  },
  data: () => ({
    cur: 0,
    value1: 0,
    searchWord: "",
    selectedOption: "name",
    options: [
      {
        text: "내용",
        value: "name",
      },
    ],
    loading: true,
  }),
  computed: {
    ...mapState({
      page: (state) => state.data.resultPage,
      reviews: (state) => state.data.adminReview,
    }),
  },
  methods: {
    ...mapActions("data", ["getAdminReview", "changeBlind"]),
    onSubmit: async function() {
      this.cur = this.cur + 1;
      await this.getAdminReview({ page: this.cur, page_size: 10 });
    },
    onSubmitt: async function() {
      if (this.cur != 1) this.cur = this.cur - 1;
      await this.getAdminReview({ page: this.cur, page_size: 10 });
    },
    async blind(index) {
      console.log(this.reviews[index]);
      this.reviews[index].content = "블라인드 처리 되었습니다.";
      console.log(this.reviews[index].id);
      await this.changeBlind({ id: this.reviews[index].id });
    },
  },
};
</script>
