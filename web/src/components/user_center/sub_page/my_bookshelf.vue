<template>
  <div class="my_bookshelf">
    书架
    <div class="content">
      <div class="title">
        <span>书名</span>
        <span>最新章节</span>
        <span>作者</span>
        <span>类型</span>
        <span>更新时间</span>
        <span>操作</span>
      </div>
      <div class="list" v-for="(item,index) in bookshelf" :key="index">
        <span>{{item.name}}</span>
        <span>{{item.most_new_chapter}}</span>
        <span>{{item.author}}</span>
        <span>{{item.type}}</span>
        <span>{{ api.formatTimeAgo(item.update_time)}}</span>
        <span class="delete">删除</span>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref ,computed,onMounted} from 'vue'
import { useStore } from '@/model/store';
import { useRouter } from 'vue-router';
import { BaseApi } from '@assets/base_api';

const store = useStore();
const router = useRouter();
const api=new BaseApi();

let bookshelf=ref([
  {
    name: '书名',
    author: '作者',
    type: '类型',
    most_new_chapter: '最新章节',
    update_time:'2025-3-15 11:04:41'
  }
]);

</script>

<style scoped>
.my_bookshelf{
  display: flex;
  width: 100%;
  flex-direction: column;
  gap:10px;
}
.content{
  display: flex;
  flex-direction: column;
  gap:10px;
}
.title{
  display: grid;
  grid-template-columns:2fr 2fr 1fr 1fr 1fr 1fr;
  font-weight: bold;
  border-bottom: 1px solid rgb(187, 182, 182);
  padding-bottom: 5px;
}
.list{
  display: grid;
  grid-template-columns:2fr 2fr 1fr 1fr 1fr 1fr;
  min-height: 50px;
  align-items: center;
  border-bottom: 1px solid rgb(187, 182, 182);
  background-color: rgb(233,233,233);
}
/*list的第一个节点*/
.list span:first-child{
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}
.list span:first-child:hover{
  color: rgb(233, 49, 49);
  text-decoration: underline;
}
.delete{
  color: white;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 5px;
  border: 1px solid rgb(187, 182, 182);
  background-color: rgb(233, 49, 49);
  width: fit-content;
  transition: all 0.3s;
}
.delete:hover{
  opacity: 0.8;
  transform: scale(1.05);
}

</style>