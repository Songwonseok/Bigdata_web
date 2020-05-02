<template>
  <v-container class="mt-5 back2">
    <v-card-text class="text-center">
      <v-btn large color="orange lighten-2 white--text ma-5" to="/search">
        <v-icon>mdi-human-greeting</v-icon>이모!
      </v-btn>
    </v-card-text>
  </v-container>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  computed:{
     ...mapState({
      currentUser: state => state.data.currentUser
    }),
  },
  mounted() {
    this.checkLogin()
  },
  methods: {
    ...mapActions("data", ["getUser"]),
    getUserInfo() {
      this.getUser(sessionStorage.userId);
    },
    checkLogin() {
      if (sessionStorage.userId != null && this.currentUser.token ==''){
        this.getUserInfo();
      }
    }
  }
};
</script>
