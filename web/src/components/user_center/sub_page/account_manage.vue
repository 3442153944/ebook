<template>
  <div class="account_manage">
    <h2>账户管理</h2>
    <div class="menu_list">
      <span>基本信息</span>
      <span>头像和背景设置</span>
      <span>密码修改</span>
    </div>
    <div class="content">
      <div class="base_info">
        <div class="base_title_list">
          <span>昵称：</span>
          <span>ID：</span>
          <span>性别</span>
          <span>简介</span>
        </div>
        <div class="base_info_item">
          <span></span>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref,computed } from 'vue'
import {useStore} from '@/model/store'

const store = useStore()
const user=computed(()=>{
  return store.$state.user
})

</script>

<style scoped>
  
</style>