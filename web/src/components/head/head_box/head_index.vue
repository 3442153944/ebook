<template>
  <div class="head_index">
    <div class="item">
      <h2><router-link to="/">升升</router-link></h2>
    </div>
    <div class="search_box">
      <input type="text" placeholder="搜索">
      <div class="search_btn">提问</div>
    </div>
    <div class="msg_box">
      <div class="msg">
        <div class="icon" style="cursor:pointer" @click="show_drop_box('msg')" ref="icon">
          <img src="@/assets/通知.svg" alt="通知">
          <span>消息</span>
        </div>
        <div class="drop_box" v-if="msg_box_show" ref="msgDropBox">
          <notice_box></notice_box>
        </div>
      </div>
      <div class="chat">
        <router-link to="/chat">
          <div class="icon" @click="show_drop_box('chat')" ref="icon2" style="cursor:pointer">
            <img src="@/assets/消息.svg" alt="消息">
            <span>聊天</span>
          </div>
        </router-link>
        <!-- <div class="drop_box" v-if="chat_show" ref="chatDropBox"></div> -->
      </div>
    </div>
    <div class="user" @click="min_box_show=!min_box_show" ref="min_box">
      <div class="user_avatar">
        <img :src="'http://localhost:8000/static/img/'+(user.avatar||'default.jpg')" alt="头像">
      </div>
      <div class="mini_box"  v-if="min_box_show" >
        <span>{{store.$state.user.username}}</span>
        <span><router-link to="/user_center">个人主页</router-link></span>
        <span @click="close_login">退出登录</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted,watchEffect } from 'vue'
import { useStore } from '@/model/store';
import { useRouter } from 'vue-router';
import notice_box from './notice_box.vue';

const store = useStore();
const router = useRouter();

const msg_box_show = ref(false);
const chat_show = ref(false);
const icon = ref(null);
const icon2 = ref(null);
const msgDropBox = ref(null);
const chatDropBox = ref(null);

let min_box_show=ref(false)
let min_box=ref(null)

const close_login=()=>{
  localStorage.removeItem('token');
  router.push('/login');
}

const handleClickOutside = (e) => {
  const isClickInsideIcon = icon.value.contains(e.target) || icon2.value.contains(e.target);
  const isClickInsideMsg = msgDropBox.value?.contains(e.target);
  const isClickInsideChat = chatDropBox.value?.contains(e.target);
  const minBox=min_box.value?.contains(e.target);
  
  if (!isClickInsideIcon && !isClickInsideMsg && !isClickInsideChat&&!minBox) {
    msg_box_show.value = false;
    chat_show.value = false;
    min_box_show.value=false
  }
};

function show_drop_box(box) {
  if (box === 'msg') {
    msg_box_show.value = !msg_box_show.value;
    chat_show.value = false;
  } else if (box === 'chat') {
    chat_show.value = !chat_show.value;
    msg_box_show.value = false;
  }
}

const user = computed(() => {
  return store.$state.user;
});

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.head_index {
  width: 85%;
  height: 80px;
  display: flex;
  margin: 0 auto;
  justify-content: space-between;
  align-items: center;
  min-width: 850px;
}
.icon{
  display: flex;
  flex-direction: column;
  gap:2px;
}
.icon img{
  width: 25px;
  height: 25px;
  object-fit: contain;
}
.user{
  position: relative;
}
.user_avatar img{
  width: 50px;
  height: 50px;
  border-radius: 50%;
 object-fit: cover; 
}
.mini_box{
  position: absolute;
  top:100%;
  left: 0px;
  display: flex;
  flex-direction: column;
  width: 100px;
  gap:10px;
  padding: 5px;
  border-radius: 5px;
  background-color: rgb(228, 226, 226);
  border:1px solid #ccc;
}
.mini_box span{
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 1px solid rgb(33,33,33);
}
.mini_box span:hover{
  background-color: rgb(133,133,133);
  transform: scale(1.03);
}
.mini_box span:active{
  background-color: rgb(133,133,133);
  transform: scale(0.98);
}
.search_box{
  width: fit-content;
  min-width: 350px;
  max-width: 450px;
  display: flex;
  gap:10px;
  align-items: center;
}
.search_box input{
  width: calc(100% - 80px);
  height: calc(100% - 10px);
  border-radius: 5px;
  border:1px solid #ccc;
  padding: 5px;
}
.search_btn{
  width: fit-content;
  padding: 3px 10px;
  background-color: rgb(0,150,250);
  color: white;
  font-size: 18px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}
.search_btn:hover{
  opacity: 0.8;
  transform: scale(1.05);
}
.search_btn:active{
  opacity: 0.8;
  transform: scale(0.95);
}
.msg_box{
  display: flex;
  gap:20px;
}
.msg{
  position: relative;
}
.chat{
  position: relative;
}
.drop_box{
  display: flex;
  position: absolute;
  left: -100%;
  top:100%;
  width: 450px;
  height: fit-content;
  max-height: 500px;
  max-width: 500px;
  min-width: 250px;
  border-radius: 5px;
  padding: 5px;
  background-color: rgb(238, 238, 238);
  border:1px solid #ccc;
}
</style>