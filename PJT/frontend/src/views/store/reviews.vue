<template>
  <v-card>
    <v-row height="300px">
      <v-col mx-5 align-self="center">
        <v-flex text-center>
          <v-icon size="150px" color="yellow darken-2">mdi-star-circle-outline</v-icon>
          <br />
          <v-text class="display-1">{{ getReviewAvg }}/5.0</v-text>
        </v-flex>
      </v-col>
      <v-col mx-5 align-self="center">
        <GChart
          :settings="{ packages: ['bar'] }"
          :data="getScoreCount"
          :options="chartOptions"
          :create-chart="(el, google) => new google.charts.Bar(el)"
          @ready="onChartReady"
        />
      </v-col>
    </v-row>
    <v-divider />
    <div v-if="user_id != null">
      <ReviewWrite />
    </div>
    <v-flex v-for="(review, index) in reviews" :key="review.id" pa-4>
      <review-list-card
        :id="review.id"
        :index="index"
        :total-score="review.total_score"
        :content="review.content"
        :reg-time="review.reg_time"
        :store-id="review.store_id"
        :user-id="review.user_id"
      />
    </v-flex>
  </v-card>
</template>

<script>
import { GChart } from "vue-google-charts";
import ReviewWrite from "@/components/ReviewWrite";
import ReviewListCard from "@/components/ReviewListCard ";
import { mapState, mapGetters } from "vuex";
export default {
  components: {
    ReviewWrite,
    ReviewListCard,
    GChart
  },
  data() {
    return {
      chartsLib: null,
      user_id: sessionStorage.userId
    };
  },
  computed: {
    ...mapState({
      currentUser: state => state.data.currentUser,
      reviews: state => state.data.storeReviewList
    }),
    ...mapGetters("data", ["getReviewAvg", "getScoreCount"]),
    chartOptions() {
      if (!this.chartsLib) return null;
      return this.chartsLib.charts.Bar.convertOptions({
        chart: {},
        bars: "horizontal", // Required for Material Bar Charts.
        hAxis: { format: "decimal" },
        height: "auto",
        colors: ["#FFD700"]
      });
    }
  },
  mounted() {
  },
  methods: {
    onChartReady(chart, google) {
      this.chartsLib = google;
    }
  }
};
</script>
<style></style>
