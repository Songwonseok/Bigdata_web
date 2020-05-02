<template>
  <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    color="#FFF9C4"
    floating
    persistent
    mobile-break-point="900"
    width="250"
  >
    <v-layout column>
      <v-list dense nav>
        <v-list-item>
          <v-list-item-avatar class="align-self-center" color="white" contain>
            <v-img src="../assets/images/logo.png" max-height="30" contain />
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="font-weight-bold">
              이번에 모먹지
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider class="mb-2" />
      <v-list v-if="is_superuser" rounded>
        <v-list-item
          v-for="(link, i) in adminLinks"
          :key="i"
          :to="link.to"
          active-class="orange lighten-2 white--text"
          class="v-list-item ma-3"
        >
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="link.text" />
        </v-list-item>
      </v-list>
      <v-list v-else rounded>
        <v-list-item
          v-for="(link, i) in links"
          :key="i"
          :to="link.to"
          active-class="orange lighten-2 white--text"
          class="v-list-item ma-3"
        >
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="link.text" />
        </v-list-item>
      </v-list>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  props: {
    opened: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    searchIcon: "mdi-search",
    links: [
      {
        to: "/",
        icon: "mdi-home",
        text: "Home",
      },
      {
        to: "/signup",
        icon: "mdi-account",
        text: "회원가입",
      },
      {
        to: "/mypage",
        icon: "mdi-account",
        text: "내 정보",
      },
      {
        to: "/search",
        icon: "mdi-card-search",
        text: "맛집 검색",
      },
      {
        to: "/storeKNN",
        icon: "mdi-bowl-mix",
        text: "맛집 추천",
      },
    ],
    adminLinks: [
      {
        to: "/admin/home",
        icon: "mdi-home",
        text: "admin-Home",
      },
      {
        to: "/admin/store",
        icon: "mdi-card-search",
        text: "admin-Store",
      },
      {
        to: "/admin/review",
        icon: "mdi-mail",
        text: "admin-Review",
      },
      {
        to: "/admin/user",
        icon: "mdi-account",
        text: "admin-Account",
      },
    ],
  }),
  computed: {
    ...mapState("app", ["drawer"]),
    ...mapState("data",["is_superuser"]),
    inputValue: {
      get() {
        return this.drawer;
      },
      set(val) {
        this.setDrawer(val);
      },
    },
  },

  methods: {
    ...mapMutations("app", ["setDrawer"]),
  },
};
</script>
