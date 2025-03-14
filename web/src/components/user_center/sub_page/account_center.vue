<template>
  <div class="account_center">
    <h2>票夹</h2>
    <div class="vote_wallet">
      <div class="icon">
        <img src="@/assets/月票.svg" alt="月票">
      </div>
      <div><span>0月票  </span></div>
    </div>
    <div class="content">
      <div class="menu_item">
        <span @click="set_now_list(0)" :class="{is_change:now_index==0}">投票记录</span>
        <span @click="set_now_list(1)" :class="{is_change:now_index==1}">月票获取记录</span>
      </div>
      <div class="list">
        <div class="list_title">
          <div class="title_item" v-for="(item,index) in now_title" :key="index">
            <span>{{item}}</span>
          </div>
        </div>
        <div class="list_content" v-for="(item,index) in now_list" :key="index">
          <span>{{item.time}}</span>
          <span>{{item.num}}</span>
          <span>{{item.title}}</span>
          <span>{{item.type}}</span>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted } from 'vue'

let vote_data=ref({
  post:{
    title:['投票时间','票数','投票小说','月票类型'],
    data:[
      {time:'2025-3-14 18:44:20',num:1,title:'标题',type:'月票'},
    ]
  },
  get:{
    title:['获取时间','票数','获取途径','月票类型'],
    data:[
      {time:'2025-3-14 18:44:20',num:1,title:'标题',type:'月票'},
    ]
  }
})

let now_list=ref([])
let now_title=ref([])
let now_index=ref(0)

function set_now_list(index){
  now_index.value=index
  if(index==0){
    now_list.value=vote_data.value.post.data
    now_title.value=vote_data.value.post.title
  }
  else{
    now_list.value=vote_data.value.get.data
    now_title.value=vote_data.value.get.title
  }
}
onMounted(()=>{
  set_now_list(0)
})

</script>

<style scoped>
.is_change{
  background-color: rgb(0,150,250);
  color: white;
  font-size: 18px;
  font-weight: bold;
}
.account_center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.vote_wallet {
  background: linear-gradient(135deg, #409eff, #2979ff);
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  color: white;
  display: flex;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.vote_wallet .icon img {
  width: 80px;
  height: 80px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  padding: 12px;
}

.vote_wallet div span {
  font-size: 1.8rem;
  font-weight: bold;
  letter-spacing: 1px;
}

.content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.menu_item {
  display: inline-flex;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.menu_item span {
  padding: 1rem 2rem;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
  position: relative;
}

.menu_item span:hover {
  background: #eef0f3;
}

.menu_item span.is_change {
  background: #409eff;
  color: white;
  border-radius: 8px;
  font-weight: 500;
}

.list {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
}

.list_title {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr 1fr;
  padding: 1rem;
  background: #fafafa;
  font-weight: 500;
  color: #909399;
}

.title_item span {
  padding: 0 1rem;
}

.list_content {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr 1fr;
  padding: 1.2rem;
  border-bottom: 1px solid #f5f7fa;
  transition: background 0.2s;
}

.list_content:hover {
  background: #fafafa;
}

.list_content span {
  padding: 0 1rem;
  color: #606266;
}

.list_content span:nth-child(2) {
  color: #67c23a;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .vote_wallet {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }

  .menu_item {
    width: 100%;
    justify-content: space-between;
  }

  .list_title {
    display: none;
  }

  .list_content {
    grid-template-columns: 1fr;
    padding: 1rem;
    position: relative;
  }

  .list_content span {
    padding: 0.5rem;
    display: block;
  }

  .list_content span::before {
    content: attr(data-label);
    display: inline-block;
    width: 80px;
    color: #909399;
    margin-right: 1rem;
  }
}
</style>