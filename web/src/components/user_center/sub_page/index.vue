<template>
  <div class="user_center_index">
    <div class="background" :style="`background-image:url('http://localhost:8000/static/img/${user.background||'default_back.jpg'}')`">
      <div class="user_box">
        <div class="avatar">
          <img :src="'http://localhost:8000/static/img/'+(user.avatar||'default.jpg')" alt="头像">
        </div>
        <div class="user_info">
          <span>{{user.username}}</span>
          <span>关注：0 &nbsp; 粉丝：0</span>
        </div>
      </div>
    </div>
    <span class="introduce">
      <h2>个型签名：</h2>
      {{ user.signature || '这个人很懒，什么都没有留下' }}
    </span>
    <div class="content">
      <div class="item">
        <span class="title">
          <img src="@assets/人民币.svg" alt="余额">
          账户余额
        </span>
        <span class="value">
          0
        </span>
        <span>
          充值
        </span>
      </div>
      <div class="item">
        <span class="title">
          <img src="@assets/钱包.svg" alt="钱包">
          我的月票
        </span>
      </div>
      <div class="item">
        <span class="title">
          <img src="@assets/书架.svg" alt="书架">
          我的书架
        </span>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref,computed, onMounted} from 'vue'
import { useStore } from '@/model/store';
const store = useStore();

let user=computed(()=>{
  return store.$state.user
})

</script>

<style scoped>
.user_center_index{
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-rows: minmax(300px, 400px) 1fr;
}
.avatar img{
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}
.background{
  width: 100%;
  height: 100%;
  display: flex;
  position: relative;
  background-size: cover;
  background-position: center;
}
.user_box{
  width: 100%;
  background-color: rgb(233,233,233,0.5);
  height: 45%;
  align-self: flex-end;
  position: relative;
  display: flex;
  padding: 5px 10px;
  align-items: center;
  gap:10px;
  font-size: 24px;
}
.avatar{
  margin-top: -75px;
}
.user_info{
  display: flex;
  flex-direction: column;
  gap:10px;
}
.content {
  margin-top: 15vh;
  padding: 2rem;
  position: relative;
  z-index: 1;
}

.item {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease;
}

.item:hover {
  transform: translateY(-2px);
}

.title {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 1.1rem;
  color: #333;
}

.title img {
  width: 24px;
  height: 24px;
}

.value {
  font-size: 1.4rem;
  font-weight: 600;
  color: #409eff;
  margin-right: 1rem;
}
</style>