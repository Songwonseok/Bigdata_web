<template>
  <v-flex class="mx-auto">
    <v-card-actions>
      <v-spacer />
      <v-card-title>리뷰작성</v-card-title>
      <v-btn
        icon
        @click="show = !show"
      >
        <v-icon>{{ show ? 'mdi-close-circle' : 'mdi-lead-pencil' }}</v-icon>
      </v-btn>
    </v-card-actions>
    <v-expand-transition>
      <div v-show="show">
        <v-divider />

        <v-form ref="form" v-model="form" class="pa-4 pt-6">
          <v-text class="subtitle-1">평점</v-text>
          <star-rating
            v-model="rating"
            :star-size="30"
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
              17
            ]"
          />
          <p />
          <v-textarea
            v-model="content"
            auto-grow
            filled
            color="deep-purple"
            label="내용"
            rows="1"
          />
        </v-form>
        <v-card-actions>
          <v-btn text @click="$refs.form.reset()">
            <v-icon>mdi-eraser</v-icon>
            Clear
          </v-btn>
          <v-spacer />
          <v-btn v-if="rating !=0 && content !=''"
                 class="white--text"
                 color="deep-purple accent-4"
                 depressed @click="submit"
          ><v-icon>mdi-lead-pencil</v-icon>Submit</v-btn>
        </v-card-actions>
      </div>
    </v-expand-transition>
  </v-flex>
</template>

<script>
import StarRating from "vue-star-rating";
import { mapState, mapActions } from "vuex";
export default {
  components: {
    StarRating
  },
    data: () => ({
      show: false,
      content:"",
      rating:0,
      user_id: sessionStorage.userId,
    }),
    computed:{
        ...mapState({
      store: state => state.data.store
    }),
    },
    methods: {
    ...mapActions("data", [
      "createReview",
      "storeReviews"
    ]),
    async submit(){
        const params={
            "id" : 1,
            "store": this.store.id,
            "user": this.user_id,
            "score": this.rating,
            "content": this.content
        };
        await this.createReview(params);
        this.allClear();
        const params2 = {
        id: this.store.id,
        page: 1,
        append: false
      }
        await this.storeReviews(params2);
        
    },
    allClear(){
      this.content = "",
      this.rating = 0
    }
  }
};
</script>
