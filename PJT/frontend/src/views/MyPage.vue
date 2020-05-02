<template>
  <v-container id="user-profile" class="mt-12" fluid tag="section">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <material-card color="blue lighten-1">
          <template v-slot:heading>
            <div class="display-5 font-weight-light">내 정보</div>
          </template>

          <v-form>
            <v-container class="py-0">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="currentUser.user.username"
                    label="아이디"
                    readonly
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="currentUser.user.email"
                    label="E-mail"
                    readonly
                  />
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="currentUser.age"
                    label="나이"
                    readonly
                  />
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="currentUser.gender"
                    label="성별"
                    readonly
                  />
                </v-col>
                <v-col cols="12" class="text-right">
                  <v-btn color="warning" to="/userUpdate">정보 수정</v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </material-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import MaterialCard from "@/components/MaterialCard";
export default {
  components: {
    MaterialCard
  },
  computed: {
    ...mapState({
      currentUser: state => state.data.currentUser
    })
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
      if (sessionStorage.userId == "" || sessionStorage.userId == null)
        this.$router.push("/login");
      else
        this.getUserInfo();
    }
  }
};
</script>
