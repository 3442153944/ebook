<template>
  <div class="left_menu">
    <div class="menu_item" v-for="(item,index) in menu_dict" :key="index">
        <router-link :to="`/book_list?id=${item.id}`">
            <span>{{item.name}}</span>
            <span>{{item.count}}</span>
        </router-link>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted } from 'vue'

let menu_dict = ref([
    { name: '科幻', count: 0 ,id:1},
    { name: '玄幻', count: 0,id:2 },
    { name: '奇幻', count: 0,id:3 },
    { name: '武侠', count: 0 ,id:4},
    { name: '仙侠', count: 0 ,id:5},
    { name: '都市', count: 0 ,id:6},
    { name: '现实', count: 0,id:7 },
    { name: '军事', count: 0 ,id:8},
    { name: '历史', count: 0 ,id:9},
    { name: '游戏', count: 0 ,id:10},
    { name: '体育', count: 0 ,id:11},
    { name: '诸天无限', count: 0 ,id:12},
    { name: '悬疑', count: 0 ,id:13},
    { name: '轻小说', count: 0 ,id:14},
]);

</script>

<style scoped>
  
</style>