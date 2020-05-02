<template>
  <div>

  </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
    
    mounted(){
        this.logout()
    },
    methods:{
        ...mapMutations("data",["clearCurrentUser"]),
        logout(){
            this.clearCurrentUser();
            this.$router.push("/");
        }
    }
}
</script>

<style>

</style>