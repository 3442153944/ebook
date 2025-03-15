<script setup>
import {ref} from 'vue'
import left_menu from './sub_com/left_menu.vue';
import auto_switch_media from '@/model/auto_switch_media/auto_switch_media.vue';
import recommend_work from './sub_com/recommend_work.vue';

</script>

<template>
<div class="root">
  <div class="content_head">
    <span>作品分类</span>
    <span>全部作品</span>
    <span>免费</span>
    <span>付费</span>
    <span>完本</span>
  </div>
  
  <div class="content">
    <left_menu style="max-width:300px;"></left_menu>
    <div class="content_right">
      <auto_switch_media style="max-height: 300px;min-height: 300px;overflow: hidden;"></auto_switch_media>
      <recommend_work></recommend_work>
    </div>
  </div>
</div>
</template>

<style scoped>
.root{
  width: 90%;
  margin: 0 auto;
  display: flex;
  gap:10px;
  flex-direction: column;
  gap:10px;
}
.content{
  display: grid;
  grid-template-columns: 1fr 5fr;
  align-items: center;
}
.content_head{
  display: grid;
  grid-template-columns: repeat(5,1fr);
  gap: 10px;
}
.content_head span{
  background-color: rgb(0,150,250);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  text-align: center;
}
.content_right{
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>