<template>
  <div class="user_center_index">
    <div class="left_menu">
        <div class="menu_item" v-for="(item,index) in menu_list" :key="index">
            <span><router-link :to="item.path">{{item.name}}</router-link></span>
        </div>
    </div>
    <div class="content">
        <router-view></router-view>
    </div>
  </div>
</template>


<script setup>
import { ref ,computed} from 'vue'
import { useStore } from '@/model/store';

const store = useStore();
let is_self=computed(()=>{
  return store.$state.is_self
})

let menu_list=ref([
    {
        name:'首页',
        path:'/user_center'
    },
    {
        name:'我的评论',
        path:'/user_center/my_comment'
    },
    {
        name:'我的钱包',
        path:'/user_center/my_wallet'
    },
    {
        name:'月票',
        path:'/user_center/account_center'
    },
    {
        name:'账户管理',
        path:'/user_center/account_manage'
    },
    {
        name:'作家中心',
        path:'/user_center/writer_center'
    },
    {
        name:'书架',
        path:'/user_center/my_bookshelf'
    },
    {
        name:'用户作品',
        path:'/user_center/my_works'
    }

])

</script>

<style scoped>
.user_center_index {
  display: flex;
  min-height: calc(100vh - 100px);
  background: #f5f7fa;
  width: 95%;
  margin: 0 auto;
  gap:10px;
  margin-top: 10px;
}

.left_menu {
  width: 240px;
  background: #ffffff;
  box-shadow: 2px 0 8px rgba(0,0,0,0.05);
  padding: 20px 0;
  position: sticky;
  top: 0;
  height: 100%;
  overflow-y: auto;
  margin-top: 10px;
  margin-left: 10px;
}

.menu_item {
  margin: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
}

.menu_item:hover {
  background: #f8f9fa;
}

.menu_item a {
  display: block;
  padding: 12px 24px;
  color: #606266;
  text-decoration: none;
  font-size: 14px;
  position: relative;
  transition: color 0.3s;
}

.menu_item a:hover {
  color: #409eff;
}

.menu_item a.router-link-active {
  color: #409eff;
  font-weight: 500;
  background: #ecf5ff;
  border-radius: 6px;
}

.menu_item a.router-link-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  background: #409eff;
  border-radius: 0 2px 2px 0;
}

.content {
  flex: 1;
  padding: 10px;
  margin: 0 auto;
  background: white;
  min-height: calc(100vh - 200px);
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  margin-top: 10px;
  max-width: calc(95% - 240px);
  border-radius: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user_center_index {
    flex-direction: column;
  }

  .left_menu {
    width: 100%;
    height: auto;
    position: static;
    padding: 10px 0;
    box-shadow: none;
    border-bottom: 1px solid #ebeef5;
  }

  .menu_item {
    margin: 4px 8px;
  }

  .menu_item a {
    padding: 10px 16px;
  }

  .content {
    padding: 16px;
    box-shadow: none;
  }
}

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
  .user_center_index {
    background: #1a1a1a;
  }

  .left_menu {
    background: #242424;
  }

  .menu_item a {
    color: #cccccc;
  }

  .menu_item:hover {
    background: #2d2d2d;
  }

  .menu_item a.router-link-active {
    background: #2d2d2d;
    color: #58a6ff;
  }

  .content {
    background: #1e1e1e;
    color: #ffffff;
  }
}
</style>