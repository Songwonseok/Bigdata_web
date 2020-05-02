<template>
  <v-card class="mx-auto">
    <v-card-text>
      <v-icon>mdi-account-circle</v-icon>
      User_{{ user_id }} 등록일 : {{ reg_time }}
      <v-btn color="red" text class="float-right">
        <v-icon>mdi-trash-can</v-icon>
      </v-btn>
    </v-card-text>

    <v-card-text>
      <star-rating
        v-model="total_score"
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
      <v-textarea v-model="content" value="reviseContent" auto-grow disabled />
    </v-card-text>
    <v-spacer />

    <v-card-actions>
      <v-spacer />
      <v-btn color="orange" text @click="blind(index)">
        블라인드
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import StarRating from "vue-star-rating";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";

export default {
  components: {
    StarRating,
  },
  props: {
    index: {
      type: Number,
      default: 0,
    },
    id: {
      type: Number,
      default: 0,
    },
    total_score: {
      type: Number,
      default: 0,
    },
    content: {
      type: String,
      default: "",
    },
    reg_time: {
      type: String,
      default: "",
    },
    storeId: {
      type: Number,
      default: 0,
    },
    user_id: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      write: true,
      reviseContent: this.content,
      reviseRating: this.totalScore,
      userId: localStorage.userId,
    };
  },
  computed: {
    ...mapState({
      currentUser: (state) => state.data.currentUser,
    }),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations("data", ["removeOneReview"]),
    ...mapActions("data", ["editReview", "deleteReview"]),
    async submit() {
      const params = {
        id: this.id,
        store: this.storeId,
        user: this.userId,
        score: this.reviseRating,
        content: this.reviseContent,
      };
      await this.editReview(params);
      this.content = this.reviseContent;
      this.totalScore = this.reviseRating;
      this.cancel();
    },
    cancel() {
      (this.reviseContent = this.content),
        (this.reviseRating = this.totalScore),
        (this.write = !this.write);
    },
    async deleteSubmit() {
      const params = {
        id: this.id,
      };
      await this.deleteReview(params);
      this.removeOneReview(this.index);
    },
    blind() {
      this.content = "블라인드 처리 되었습니다.";
    },
  },
};
</script>
