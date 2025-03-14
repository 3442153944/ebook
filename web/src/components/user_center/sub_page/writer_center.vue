<template>
  <div class="writer_center">
    作家中心
    <div class="menu">
      <div class="menu_item">
        <span>我的作品</span>
      </div>
      <div class="menu_item">
        <span>开始写作</span>
      </div>
    </div>
    <div class="content">

    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'

let work_list=ref([
  {
    name:'作品1',
    id:1,
    time:'2025-3-14 23:57:19',
    work_data:{
      'read':100,
      'chapter':10,
      'most_new_chapter':'第10章',
      'most_new_time':'2025-3-14 23:57:19',
      'status':1,
      'word_count':0,
      'comment':0,
    },
    cover:'default_cover.jpg'
  }
])

</script>

<style scoped>
  
</style>