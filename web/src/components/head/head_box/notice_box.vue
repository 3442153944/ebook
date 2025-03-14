<template>
  <div class="notice_box">
    <h2>通知</h2>
    <div class="menu">
      <div class="menu_item">
        <span>通知</span>
      </div>
      <div class="menu_item">
        <span>作品</span>
      </div>
    </div>
    <div class="content" >
      <div class="user_list">
        <div class="user" v-for="(item,index) in notice_list_by_user" :key="index" :class="index==now_key?'is_choose_user':''">
          <div class="avatar" @click="set_now_notice_list(item.notice_list,index,item.user_info,item.total)" v-if="item.user_info">
            <img :src="'http://localhost:8000/static/img/'+(item.user_info.avatar||'default.jpg')" alt="用户头像">
          </div>
        </div>
      </div>
      <div class="notice_list">
        <div class="notice" v-for="(item,index) in now_notice_list" :key="index">
          <div class="notice_title">
            <span><strong>{{item.title}}</strong></span>
          </div>
          <div class="notice_content">
            <span>{{item.content}}</span>
            <div class="notice_time">
              <span>{{api.formatTimeAgo(item.time)}}</span>
            </div>
          </div>
        </div>
        <div class="page">
          <page_1 :total="total" :pageSize="limit" @page-change="get_more($event)"></page_1>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { BaseApi } from '@assets/base_api';
import page_1 from '@/model/page.vue'

const api = new BaseApi();
const notice_list = ref([]);
const notice_list_by_user = ref({}); // 改为对象结构
const limit = ref(3);
const offset = ref(0);
const total = ref(0);

// 分页计算
const page = computed(() => Math.ceil(total.value / limit.value));
let now_notice_list=ref([])
let now_key=ref()
let now_user=ref()

function set_now_notice_list(list,key,user,total_1){
  now_notice_list.value=list
  now_key.value=key
  now_user.value=user
  total.value=total_1
}

async function getNoticeList() {
  try {
    const res = await api.post('api/user/get_notice', {
      limit: limit.value,
      offset: offset.value
    });
    return res.status === 200 ? res.result : false;
  } catch (e) {
    console.error('获取通知列表失败:', e);
    return false;
  }
}

async function classifyNotices() {
  const userInfoCache = {}; // 用户信息缓存
  
  // 使用 Promise.all 并行处理用户信息请求
  await Promise.all(notice_list.value.map(async (notice) => {
    const userId = notice.send_user_id;
    
    if (!userId) {
      console.warn('发现无效用户ID的通知:', notice.id);
      return;
    }

    // 初始化用户条目
    if (!notice_list_by_user.value[userId]) {
      notice_list_by_user.value[userId] = {
        notice_list: [],
        total: 0,
        user_info: null
      };

      // 缓存用户信息请求
      userInfoCache[userId] = api.get_user_info_by_id(userId)
        .then(res => {
          if (res.status === 200) {
            notice_list_by_user.value[userId].user_info = res.result.data;
          }
        })
        .catch(e => {
          console.error(`获取用户${userId}信息失败:`, e);
        });
    }

    // 添加通知到对应分类
    notice_list_by_user.value[userId].notice_list.push(notice);
    notice_list_by_user.value[userId].total++;
  }));

  // 等待所有用户信息请求完成
  await Promise.all(Object.values(userInfoCache));
}

async function get_more(target_page) {
  offset.value = (target_page - 1) * limit.value;
  const res=await api.get_notice_by_id(now_user.value.user_id,limit.value, offset.value)
  if (res.status === 200) {
    now_notice_list.value = res.result.data;
  }
  else {
    console.error('获取通知列表失败');
  }
}

onMounted(async () => {
  const res = await getNoticeList();
  if (res) {
    notice_list.value = res.data;
    await classifyNotices();
    console.log('分类后的数据结构:', notice_list_by_user.value);
  } else {
    console.error('初始化获取通知列表失败');
  }
  for(let [key,value] of Object.entries(notice_list_by_user.value)){
    now_notice_list.value=notice_list_by_user.value[key].notice_list
    total.value=notice_list_by_user.value[key].total
    now_user.value=notice_list_by_user.value[key].user_info
    now_key.value=key
    return
  }
});
</script>

<style scoped>
.notice_box{
  width: 100%;
  display: flex;
  height: 100%;
  flex-direction: column;
  gap:5px;
}
.content{
  display: flex;
  gap:5px;
}
.user_list{
  display: flex;
  width:50px;
  flex-direction: column;
  gap:5px;
  max-height: 100%;
  overflow-y: auto;
}
.user{
  cursor: pointer;
  display: flex;
  padding: 3px;
  border-bottom: 1px solid rgb(114, 114, 114);
  transition: all 0.2s;
}
.user:hover{
  background-color: rgb(0,0,0,0.1);
  opacity: 0.8;
  border-radius: 50%;
}
.is_choose_user{
  background-color: rgb(0,0,0,0.1);
  opacity: 0.8;
  border-radius: 50%;
}
.avatar img{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}
.notice_list{
  display: flex;
  flex-direction: column;
  gap:5px;
  max-height: 100%;
  overflow-y: auto;
}
.notice{
  display: flex;
  flex-direction: column;
  padding: 3px;
  border-bottom: 1px solid rgb(114, 114, 114);
  gap:5px;
}
.notice_time{
  font-size: 12px;
  color:rgb(114, 114, 114);
}
</style>