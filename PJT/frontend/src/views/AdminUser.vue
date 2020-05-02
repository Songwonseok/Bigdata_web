<template>
  <div infinite-scroll-disabled="loading" infinite-scroll-distance="10">
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center row wrap mt-5>
        <v-flex xs12 md8>
          <MaterialCard color="orange lighten-2">
            <template v-slot:heading>
              <div class="display-5 font-weight-light">
                유저 검색
              </div>
            </template>

            <v-form>
              <v-container py-0>
                <v-layout row>
                  <v-flex xs12 text-center>
                    <template v-if="users.length > 0">
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
          <v-row dense>
            <v-col v-for="(user, index) in users" :key="index" cols="6">
              <template v-if="user.is_superuser">
                <v-card class="mx-auto" color="orange" dark>
                  <v-card-text>
                    <v-icon>mdi-account-circle</v-icon>
                    User_{{ user.id }}
                  </v-card-text>

                  <v-card-text class="text--primary">
                    email : {{ user.email }}
                  </v-card-text>
                  <v-card-text class="text--primary">
                    아이디 : {{ user.username }}
                  </v-card-text>
                  <v-spacer />

                  <v-card-actions>
                    <v-spacer />
                    <v-btn text @click="delPer(index)">
                      권한 삭제
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </template>
              <template v-else>
                <v-card class="mx-auto">
                  <v-card-text>
                    <v-icon>mdi-account-circle</v-icon>
                    User_{{ user.id }}
                  </v-card-text>

                  <v-card-text class="text--primary">
                    email : {{ user.email }}
                  </v-card-text>
                  <v-card-text class="text--primary">
                    아이디 : {{ user.username }}
                  </v-card-text>
                  <v-spacer />

                  <v-card-actions>
                    <v-spacer />

                    <v-btn color="orange" text @click="addPer(index)">
                      권한 추가
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </template>
            </v-col>
          </v-row>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import MaterialCard from "@/components/MaterialCard";
import { mapState, mapActions, mapMutations } from "vuex";
export default {
  components: {
    MaterialCard,
  },
  data: () => ({
    cur: 0,
    value1: 0,
    searchWord: "",
    selectedOption: "name",
    options: [
      {
        text: "아이디",
        value: "name",
      },
    ],
    loading: true,
  }),
  computed: {
    ...mapState({
      users: (state) => state.data.adminUser,
    }),
  },
  methods: {
    ...mapActions("data", ["getAdminUser", "changePer"]),
    onSubmit: async function() {
      this.cur = this.cur + 1;
      await this.getAdminUser({ limit: 10, offset: this.cur });
    },
    onSubmitt: async function() {
      if (this.cur != 1) this.cur = this.cur - 1;
      await this.getAdminUser({ limit: 10, offset: this.cur });
    },
    addPer(index) {
      this.users[index].is_superuser = true;
      this.changePer(this.users[index]);
    },
    delPer(index) {
      this.users[index].is_superuser = false;
      this.changePer(this.users[index]);
    },
  },
};
</script>
