<template>
  <div class="my_works">
    用户作品
    <div class="menu">
      <div class="menu_item">
        <span>我的作品</span>
      </div>
    </div>
    <div class="content">
      <div class="work_list">
        <div class="work_item" v-for="(item,index) in work_list" :key="index">
          <div class="cover">
            <img :src="'http://localhost:8000/static/img/'+item.cover" alt="封面">
          </div>
          <div class="info">
            <div class="name">{{item.name}}</div>
            <div class="update"><span>{{item.work_data.most_new_time}}&nbsp;</span><span>更新至：{{item.work_data.most_new_chapter}}</span></div>
            <div class="data"><span>章节数：{{item.work_data.chapter}}</span><span>字数：{{api.formatNumberCount(item.work_data.word_count)}}字</span>
              <span>状态：{{item.work_data.status}}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { BaseApi } from '@assets/base_api';
const api=new BaseApi()

let work_list=ref([
  {
    name:'作品1',
    id:1,
    time:'2025-3-14 23:57:19',
    work_data:{
      'read':100,
      'chapter':10,
      'most_new_chapter':'第10章',
      'most_new_time':'2025-3-14 23:57:19',
      'status':'连载中，已签约',
      'word_count':10001,
      'comment':0,
    },
    cover:'default_cover.jpg'
  }
])

</script>

<style scoped>
.writer_center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 标题样式 */
.writer_center > div:first-child {
  font-size: 2rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #409eff;
}

.menu {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem 0;
  border-bottom: 1px solid #ebeef5;
}

.menu_item {
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s;
  color: #606266;
}

.menu_item:hover {
  background: #f5f7fa;
  color: #409eff;
}

.work_list {
  display: grid;
  gap: 1.5rem;
}

.work_item {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  display: grid;
  grid-template-columns: 120px 1fr auto;
  gap: 1.5rem;
  transition: transform 0.2s;
}

.work_item:hover {
  transform: translateY(-2px);
}

.cover {
  width: 120px;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.name {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1a1a1a;
}

.update {
  display: flex;
  gap: 1rem;
  color: #909399;
  font-size: 0.9rem;
}

.data {
  display: flex;
  gap: 1.5rem;
  color: #606266;
}

.data span {
  padding: 0.4rem 0.8rem;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 0.9rem;
}

.work_settings {
  display: flex;
  align-items: flex-start;
}

.work_settings .item {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  min-width: 120px;
}

.work_settings span {
  padding: 0.6rem 1rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 0.9rem;
  color: #606266;
}

.work_settings span:hover {
  background: #f5f7fa;
  color: #409eff;
}

.create_chapter {
  background: #409eff!important;
  color: white!important;
}

.create_chapter:hover {
  background: #3375e0!important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .work_item {
    grid-template-columns: 1fr;
  }

  .cover {
    width: 100%;
    height: 200px;
  }

  .work_settings .item {
    flex-direction: row;
    flex-wrap: wrap;
    margin-top: 1rem;
  }

  .data {
    flex-wrap: wrap;
    gap: 0.8rem;
  }
}
</style>