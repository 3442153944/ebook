<script setup lang="ts">
import head_page from './head/head_page.vue';
import { useStore } from '@/model/store';
import { onMounted } from 'vue';
const store = useStore();

onMounted(async()=>{
  await store.verify_login();
  console.log(store.$state.user)
})

</script>

<template>
  <head_page></head_page>
  <router-view></router-view>
</template>

<style scoped>

</style>
