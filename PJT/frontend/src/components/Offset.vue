<template>
  <div :style="styles" class="v-offset">
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    offset: {
      type: [Number, String],
      default: 0
    }
  },

  computed: {
    styles() {
      return {
        top: `-${this.offset}px`,
        marginBottom: `-${this.offset}px`
      };
    }
  }
};
</script>

<style>
.v-offset {
  margin: 0 auto;
  max-width: calc(100% - 32px);
  position: relative;
}
</style>
