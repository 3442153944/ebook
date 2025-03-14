<template>
  <div class="account_manage">
    <h2>账户管理</h2>
    <div class="menu_list">
      <span @click="change_index(0)" :class="{is_change:now_index==0}">基本信息</span>
      <span @click="change_index(1)" :class="{is_change:now_index==1}">头像和背景设置</span>
      <span @click="change_index(2)" :class="{is_change:now_index==2}">密码修改</span>
    </div>
    <div class="content">
      <div class="base_info" v-if="now_index==0">
        <div class="info_item">
          <div class="base_title_list">
            <span>昵称：</span>
            <span>ID：</span>
            <span>性别</span>
            <span>简介</span>
          </div>
          <div class="base_info_item">
            <input v-model="user.username" type="text">
            <span>{{user.user_id}}</span>
            <div style="display:flex;align-items:center;justify-content:center;max-width:200px;">
              <input type="radio" name="sex" value="男" checked v-model="user.sex"> 男
            <input type="radio" name="sex" value="女" v-model="user.sex"> 女
            </div>
            
            <textarea v-model="user.signature" maxlength="100" class="textarea" placeholder="请输入简介(不超过100字)"></textarea>
          </div>
        </div>
        <div class="sure_btn">
          <span>保存</span>
        </div>
      </div>
      <div class="avatar_bg" v-if="now_index==1">
        <div class="avatar">
          <img :src="'http://localhost:8000/static/img/'+(user.avatar||'default.jpg')" alt="头像" ref="avatar">
          <input type="file" @change="get_avatar_file" ref="avatar_change" style="display:none">
          <span @click="choose_avatar()">修改</span>
        </div>
        <div class="bg">
          <img :src="'http://localhost:8000/static/img/'+(user.background||'default_back.jpg')" alt="背景" ref="background">
          <input type="file" @change="get_background_file" ref="background_change" style="display:none">
          <span @click="choose_background()">修改</span>
        </div>
        <div class="sure_btn">
          <span>保存</span>
        </div>
      </div>
      <div class="password_change" v-if="now_index==2">
        <div class="old_password">
          <span>旧密码：</span>
          <input type="password" v-model="old_password">
        </div>
        <div class="new_password">
          <span>新密码：</span>
          <input type="password" v-model="new_password">
        </div>
        <div class="sure_btn" :class="{btn_disable:!btn_disable}">
          <span>保存</span>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref,computed,watch,onMounted } from 'vue'
import {useStore} from '@/model/store'
import { BaseApi } from '@assets/base_api'

const api=new BaseApi()

const store = useStore()
const user=computed(()=>{
  //user解引用
  return {...store.$state.user}
})
let now_index=ref(0)

function change_index(index){
  now_index.value=index
}
let avatar=ref(null)
let background=ref(null)
let avatar_change=ref(null)
let background_change=ref(null)
let avatar_file=ref(null)
let background_file=ref(null)

//选择文件
function choose_avatar(){
  avatar_change.value.click()
}
function choose_background(){
  background_change.value.click()
}
async function get_avatar_file(e){
  avatar_file.value=e.target.files[0]
  api.change_img(avatar.value,avatar_file.value)
}
function get_background_file(e){
  background_file.value=e.target.files[0]
  api.change_img(background.value,background_file.value)
}

let new_password=ref(null)
let old_password=ref(null)
let btn_disable=ref(true)
//修改密码
function check_password(){
  if(new_password.value==null||old_password.value==null){
    btn_disable.value=true
  }
  if(new_password.value==old_password.value){
    btn_disable.value=true
  }
  else{
    btn_disable.value=false
  }
}
watch([new_password,old_password],(new_value,old_value)=>{
  check_password()
})

</script>

<style scoped>
.is_change{
  color: white;
  background-color: rgb(0,150,250);
}
.avatar img{
  max-width: 200px;
  max-height: 200px;
  width: auto;
  height: auto;
  object-fit: cover;
}
.bg img{
  max-width: 300px;
  max-height: 200px;
  width: auto;
  height: auto;
  object-fit: cover;
}
.account_manage {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.account_manage h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

/* 菜单样式 */
.menu_list {
  display: flex;
  justify-content: center;
  border-bottom: 2px solid #eaeaea;
  margin-bottom: 20px;
}

.menu_list span {
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  color: #555;
  border-radius: 4px 4px 0 0;
  transition: background-color 0.3s;
}

.menu_list span:hover,
.menu_list span.is_change {
  background-color: rgb(0,150,250);
  color: #fff;
}

/* 内容区域 */
.content {
  padding: 20px;
}

/* 基本信息板块 */
.base_info {
  margin-top: 20px;
  display: flex;
  gap:10px;
  flex-direction: column;
}
.info_item{
  display: grid;
  grid-template-columns: minmax(50px,100px) minmax(100px,1fr);
  gap:10px;
}

.base_title_list {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr 3fr;
}

.base_info_item {
 display: grid;
 grid-template-rows: 1fr 1fr 1fr 3fr;
 align-items: center;
}

.base_info_item input {
  width: calc(100% - 100px);
  padding: 8px;
  margin: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.base_info_item textarea {
  width: calc(100% - 100px);
  padding: 8px;
  margin: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  height: 100px;
}

/* 头像和背景设置板块 */
.avatar_bg {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.avatar,
.bg {
  margin-bottom: 20px;
  position: relative;
}

.avatar img,
.bg img {
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.avatar span,
.bg span {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0,150,250,0.8);
  color: #fff;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s;
}

.avatar span:hover,
.bg span:hover {
  background: rgb(0,150,250);
}

/* 密码修改板块 */
.password_change {
  margin-top: 20px;
}

.password_change .old_password,
.password_change .new_password {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.password_change span {
  width: 80px;
  display: inline-block;
}

.password_change input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 保存按钮 */
.sure_btn {
  text-align: center;
  width: fit-content;
  margin: 10px auto;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
  cursor: pointer;
  color: #fff;
  background-color: rgb(0,150,250);
}

.sure_btn:hover {
  background-color: rgb(0,130,220);
}
.btn_disable{
  background-color: rgb(33, 73, 102);
  cursor: not-allowed;
  color: white;
}
/* 响应式设计 */
@media (max-width: 768px) {
  .base_info_item {
    flex-direction: column;
  }
  
  .base_info_item input[type="text"],
  .base_info_item textarea {
    width: 100%;
    margin: 5px 0;
  }
  
  .menu_list {
    flex-direction: column;
  }
  
  .menu_list span {
    margin: 5px 0;
  }
}
</style>