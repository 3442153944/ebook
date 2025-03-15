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
import { BaseApi } from '@assets/base_api';

const api = new BaseApi();

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

//获取分类信息
async function get_menu_dict(){
    let res=await api.post('api/get_info/get_novel_count',{

    })
    if(res.status==200){
        menu_dict.value=res.result.data
    }
    else{
        console.log(res)
    }
}
onMounted(async ()=>{
    await get_menu_dict()
})

</script>

<style scoped>
.left_menu {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1px;
  background: #f0f2f5;
  border-radius: 8px;
  overflow: hidden;
}

.menu_item {
  background: white;
  transition: all 0.3s;
}

.menu_item:nth-child(4n+1),
.menu_item:nth-child(4n+2) {
  background: #f8f9fa;
}

.menu_item:hover {
  background: #e6f7ff !important;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.menu_item a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  color: #606266;
  text-decoration: none;
}

.menu_item span:first-child {
  font-size: 14px;
}

.menu_item span:last-child {
  font-size: 12px;
  color: #909399;
  background: rgba(0, 150, 250, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .left_menu {
    grid-template-columns: 1fr;
  }
  
  .menu_item:nth-child(odd) {
    background: #f8f9fa;
  }
  
  .menu_item:nth-child(even) {
    background: white;
  }
}
</style>