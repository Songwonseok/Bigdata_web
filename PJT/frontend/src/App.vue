<template>
  <v-app id="app">
    <toolbar />
    <drawer />
    <route-view />
    <go-top />
  </v-app>
</template>

<script>
import Drawer from "@/components/Drawer";
import Toolbar from "@/components/Toolbar";
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";

export default {
  components: {
    Drawer,
    Toolbar,
    RouteView,
    GoTop
  },
  mounted() {
    var self = this;
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(pos) {
        self.$store.state.userLat = pos.coords.latitude;
        self.$store.state.userLng = pos.coords.longitude;
      });
    }
  }
};
</script>
<style>
  .back {
  background-image: url(./assets/images/back1.png);
  background-size: contain;
  background-position: center;
}
.back2 {
  background-image: url(./assets/images/back2.jpg);
  background-size: cover;
  height: 100%;
}
#inspire {
  background: none;
}
</style>