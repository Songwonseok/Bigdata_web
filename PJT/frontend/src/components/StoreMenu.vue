<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">메 뉴</th>
          <th class="text-left">가 격</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in menus" :key="item.menu_name">
          <td>{{ item.menu_name }}</td>
          <td>{{ item.price }}원</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  props: {
    menus: {
      type: Array,
      default: () => new Array()
    }
  }
};
</script>

<style></style>
