<template>
  <v-card v-if="write" class="mx-auto">
    <v-card-text>
      <v-icon>mdi-account-circle</v-icon>
      User {{ userId }}
      <v-text class="float-right">{{ regTime.substring(0,10) }}</v-text>
    </v-card-text>

    <v-card-text>
      <span class="font-weight-medium subtitle-2">
        <v-icon color="yellow darken-2">mdi-star</v-icon>
        {{ totalScore }}
      </span>
    </v-card-text>

    <v-card-text class="text--primary">
      <div>{{ content }}</div>
    </v-card-text>
    <v-spacer />

    <v-card-actions v-if="userId == user_id">
      <v-spacer />
      <v-btn color="orange" text @click="cancel">
        <v-icon>mdi-pencil-outline</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>

  <v-card v-else class="mx-auto">
    <v-card-text>
      <v-icon>mdi-account-circle</v-icon>
      User_{{ userId }}
      <v-btn color="red" text class="float-right" @click="deleteSubmit">
        <v-icon>mdi-trash-can</v-icon>
      </v-btn>
    </v-card-text>

    <v-card-text>
      <star-rating
        v-model="reviseRating"
        :star-size="20"
        :border-width="3"
        border-color="#d8d8d8"
        :rounded-corners="true"
        :star-points="[23,2, 14,17, 0,19, 10,34, 7,50, 23,43, 38,50, 36,34, 46,19, 31,17]"
      />
    </v-card-text>

    <v-card-text class="text--primary">
      <v-text-field v-model="reviseContent" value="reviseContent" />
    </v-card-text>
    <v-spacer />

    <v-card-actions v-if="userId == user_id">
      <v-spacer />
      <v-btn color="orange" text @click="submit">수정</v-btn>

      <v-btn color="orange" text @click="write = !write">취소</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import StarRating from "vue-star-rating";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";

export default {
  components: {
    StarRating
  },
  props: {
    index: {
      type: Number,
      default: 0
    },
    id: {
      type: Number,
      default: 0
    },
    totalScore: {
      type: Number,
      default: 0
    },
    content: {
      type: String,
      default: ""
    },
    regTime: {
      type: String,
      default: ""
    },
    storeId: {
      type: Number,
      default: 0
    },
    userId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      write: true,
      reviseContent: this.content,
      reviseRating: this.totalScore,
      user_id: sessionStorage.userId
    };
  },
  computed: {
    ...mapState({
      currentUser: state => state.data.currentUser
    }),
    ...mapGetters({})
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
        content: this.reviseContent
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
        id: this.id
      };
      await this.deleteReview(params);
      this.removeOneReview(this.index);
    }
  }
};
</script>
