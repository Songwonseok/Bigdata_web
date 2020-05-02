<template>
  <v-app-bar id="app-toolbar" app flat color="#f6bf4f" height="100" class="back">
    <v-btn v-if="responsive" dark icon @click.stop="onClickDrawer">
      <v-icon color="white">mdi-view-list</v-icon>
    </v-btn>
    <v-spacer />
    <v-menu bottom left offset-y origin="top right" transition="scale-transition">
      <template v-slot:activator="{ attrs, on }">
        <v-btn class="ml-2" min-width="0" text v-bind="attrs" v-on="on">
          <v-icon color="white">mdi-account</v-icon>
          <v-text v-if="currentUser.token == ''" class="white--text font-weight-bold">로그인</v-text>
          <v-text v-else class="white--text font-weight-bold">환영합니다</v-text>
        </v-btn>
      </template>

      <v-list :tile="false" nav>
        <div v-if="currentUser.token == ''">
          <app-bar-item v-for="link in links" :key="link.text" router :to="link.route">
            <v-list-item-title v-text="link.text" />
          </app-bar-item>
        </div>
        <div v-else>
          <app-bar-item v-for="link in loginLinks" :key="link.text" router :to="link.route">
            <v-list-item-title v-text="link.text" />
          </app-bar-item>
        </div>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { VHover, VListItem } from "vuetify/lib";
import { mapMutations, mapState, mapActions } from "vuex";

export default {
  components: {
    AppBarItem: {
      render(h) {
        return h(VHover, {
          scopedSlots: {
            default: ({ hover }) => {
              return h(
                VListItem,
                {
                  attrs: this.$attrs,
                  class: {
                    "black--text": !hover,
                    "white--text secondary elevation-12": hover
                  },
                  props: {
                    activeClass: "",
                    dark: hover,
                    link: true,
                    ...this.$attrs
                  }
                },
                this.$slots.default
              );
            }
          }
        });
      }
    }
  },
  data: () => ({
    currUser: sessionStorage.userId,
    login: false,
    responsive: false,
    links: [
      { text: "로그인", route: "/login" },
      { text: "회원가입", route: "/signup" }
    ],
    loginLinks: [
      { text: "내 정보", route: "/mypage" },
      { text: "로그아웃", route: "/logout" }
    ]
  }),
  computed: {
    ...mapState({
      currentUser: state => state.data.currentUser
    }),
    ...mapState("app", ["drawer"]),
    loginCheck() {
      if (sessionStorage.userId != null) login = true;
      return login;
    }
  },
  mounted() {
    this.checkLogin()
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },

  methods: {
    ...mapActions("data", ["getUser"]),
    ...mapMutations("app", ["setDrawer"]),
    onClickDrawer() {
      this.setDrawer(!this.drawer);
    },
    onResponsiveInverted() {
      if (window.innerWidth < 2000) {
        this.responsive = true;
      } else {
        this.responsive = false;
      }
    },
    getUserInfo() {
      this.getUser(sessionStorage.userId);
    },
    checkLogin() {
      if (sessionStorage.userId != null || this.currentUser.token ==''){
        this.getUserInfo(); 
      }
    }
  }
};
</script>
