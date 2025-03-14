<template>
  <div class="my_comment">
    <h2>我的书评</h2>
    <div class="content">
      <div class="menu_list">
        <div class="menu_item" @click="change_comment(0)" :class="{change: now_menu_index == 0}">
          <span>我发布的书评</span>
        </div>
        <div class="menu_item" @click="change_comment(1)" :class="{change: now_menu_index == 1}">
          <span>回复的书评</span>
        </div>
      </div>
      <div class="comment_list">
        <div class="comment_title">
          <span>评论</span>
          <span>是否精华评论</span>
          <span>回复</span>
          <span>回复时间</span>
          <span>所在作品</span>
        </div>
        <div class="comment_item" v-for="(item,index) in now_list" :key="index">
          <span>{{ item.comment }}</span>
          <span>{{ item.is_essence ? '是' : '否' }}</span>
          <span>{{ item.reply }}</span>
          <span>{{ item.reply_time }}</span>
          <span><router-link :to="item.book.path">{{item.book.name}}</router-link></span>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted } from "vue";

let comment_list = ref({
  send_comment: [
    {
      comment: "这是一条评论这是一条评论这是一条评论这是一条评论",
      is_essence: true,
      reply: "这是一条回复",
      reply_time: "2025-3-14 17:50:49",
      book: {name: "书名1",path: "/book?id=1"},
    },
  ],
  reply_comment: [
    {
      comment: "这是一条评论这是一条评论这是一条评论这是一条评论这是一条评论",
      is_essence: true,
      reply: "这是一条回复",
      reply_time: "2025-3-14 17:50:49",
      book:{name: "书名2",path: "/book?id=2"},
    }
  ],
});
let now_list = ref([]);
let now_menu_index=ref(0)

function change_comment(index){
  if(index == 0){
    now_list.value = comment_list.value.send_comment;
    now_menu_index.value = 0
  }
  else{
    now_list.value = comment_list.value.reply_comment;
    now_menu_index.value = 1
  }
}

onMounted(()=>{
  change_comment(0)
})

</script>

<style scoped>
.my_comment {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h2 {
  font-size: 1.8rem;
  color: #1a1a1a;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #409eff;
  display: inline-block;
}

.content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.menu_list {
  display: flex;
  border-bottom: 1px solid #ebeef5;
  background: #f8f9fa;
}

.menu_item {
  flex: 1;
  text-align: center;
  padding: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  color: #606266;
}

.menu_item:hover {
  background: #f0f2f5;
}

.menu_item.active {
  color: #409eff;
  font-weight: 500;
}

.menu_item.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40%;
  height: 3px;
  background: #409eff;
  border-radius: 2px;
}

.comment_list {
  padding: 1rem;
}

.comment_title {
  display: grid;
  grid-template-columns: 3fr 1fr 2fr 1.5fr 1.5fr;
  gap: 1rem;
  padding: 1rem;
  background: #fafafa;
  color: #666;
  font-size: 0.9rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.comment_item {
  display: grid;
  grid-template-columns: 3fr 1fr 2fr 1.5fr 1.5fr;
  gap: 1rem;
  padding: 1.2rem;
  margin: 0.5rem 0;
  background: white;
  border-radius: 8px;
  transition: all 0.2s;
  border: 1px solid #f0f0f0;
}

.comment_item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

/* 特定列样式 */
.comment_item span:nth-child(1) {
  color: #1a1a1a;
  font-weight: 500;
}

.comment_item span:nth-child(2) {
  color: #67c23a;
  font-weight: 500;
}

.comment_item span:nth-child(2)::before {
  content: "✔️";
  margin-right: 4px;
}

.comment_item span:nth-child(4) {
  color: #909399;
  font-size: 0.9rem;
}

.comment_item span:nth-child(5) {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
}

/* 空状态提示 */
.comment_list:empty::before {
  content: "暂无相关书评";
  display: block;
  text-align: center;
  color: #909399;
  padding: 3rem 0;
}
.change{
  background-color: rgb(0,150,250);
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .comment_title,
  .comment_item {
    grid-template-columns: 1fr;
    padding: 1rem;
    gap: 0.5rem;
  }

  .comment_title {
    display: none;
  }

  .comment_item {
    position: relative;
    padding: 1.2rem;
  }

  .comment_item span {
    display: block;
    padding: 0.3rem 0;
  }

  .comment_item span::before {
    content: attr(data-label);
    display: inline-block;
    width: 80px;
    color: #909399;
    font-size: 0.9rem;
    margin-right: 1rem;
  }

  .comment_item span:nth-child(1)::before {
    content: "评论：";
  }
  .comment_item span:nth-child(2)::before {
    content: "精华评论：";
  }
  .comment_item span:nth-child(3)::before {
    content: "回复：";
  }
  .comment_item span:nth-child(4)::before {
    content: "回复时间：";
  }
  .comment_item span:nth-child(5)::before {
    content: "所在作品：";
  }
}
</style>