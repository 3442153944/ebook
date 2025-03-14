<template>
  <div class="chat_container">
    <!-- 用户列表侧边栏 -->
    <div class="user_sidebar">
      <div class="user_list">
        <div
          v-for="(user, index) in user_list"
          :key="index"
          class="user_item"
          :class="{ active: activeUser?.user_id === user.user_id }"
          @click="selectUser(user)"
        >
          <div class="avatar">
            <img :src="'http://localhost:8000/static/img/'+(user.avatar||'default.jpg')" alt="avatar" />
          </div>
          <div class="user_info">
            <span class="username">{{ user.user_name }}</span>
            <span class="status"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="main_chat">
      <!-- 消息显示区域 -->
      <div class="message_area" ref="messageArea">
        <div
          v-for="(msg, index) in now_msg_list"
          :key="index"
          class="message_wrapper"
          :class="{ 'own-message': msg.user_id !== currentUserId }"
        >
          <div class="message_bubble">
            <div v-if="msg.user_id !== currentUserId" class="avatar">
              <img :src="'http://localhost:8000/static/img/'+(msg.avatar||'default.jpg')" alt="avatar" />
            </div>
            <div class="message_content">
              <div class="message_text">{{ msg.msg }}</div>
              <div class="message_time">{{ api.formatTimeAgo(msg.time) }}</div>
            </div>
            <div v-if="msg.user_id === currentUserId" class="avatar">
              <img :src="'http://localhost:8000/static/img/'+(currentUserAvatar||'default.jpg')" alt="avatar" />
            </div>
          </div>
        </div>
      </div>

      <!-- 消息输入区域 -->
      <div class="input_area">
        <div class="input_wrapper">
          <input
            v-model="inputMessage"
            type="text"
            placeholder="输入消息..."
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage">
            <span>发送</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, watch,nextTick, onMounted} from "vue";
import { useStore } from "@/model/store";
import { BaseApi } from "@assets/base_api";

const store = useStore();
const api = new BaseApi();

let user_id = store.$state.user.user_id;
let inputMessage = ref("");
let ws=null

let user_list = ref([
  {
    user_id: 1,
    user_name: "admin",
    avatar: "default.jpg",
    msg_list: [
      { user_id: 1, msg: "hello", time: "2025-3-13 16:34:25" },
      { user_id: 184, msg: "hi", time: "2025-3-13 16:34:40" },
    ],
  },
  {
    user_id: 184,
    user_name: "testuser",
    avatar: "default.jpg",
    msg_list: [
      { user_id: 1, msg: "hello", time: "2025-3-13 16:34:25" },
      { user_id: 184, msg: "hi", time: "2025-3-13 16:34:40" },
    ],
  },
]);

let now_msg_list = ref([
  {
    user_id: 1,
    msg: "hello",
    time: "2025-3-13 16:34:25",
    avatar: "default.jpg",
  },
  {
    user_id: 184,
    msg: "hi",
    time: "2025-3-13 16:34:40",
    avatar: "default.jpg",
  },
]);

let currentUserId = ref(1);
let currentUserAvatar = ref("default.jpg");
let activeUser = ref(null);
let now_chat_user=ref()

function selectUser(user){
    currentUserId.value = user.user_id;
    currentUserAvatar.value = user.avatar;
    activeUser.value = user;
    now_chat_user.value=user
}

let date=new Date
let now=date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+' '+date.getHours()+':'+date.getMinutes()+':'+date.getSeconds()
let ws_url = "ws://127.0.0.1:2233/ts";

// 建立 WebSocket 连接时只传 token
async function connect() {
    let token = localStorage.getItem("token");
    let ws_url = `ws://127.0.0.1:2233/ts?token=${token}`;
    ws = new WebSocket(ws_url);

    ws.onopen = () => {
        console.log("WebSocket连接已打开");
        // 可在此处做一些初始化操作
    }

    ws.onmessage = (event) => {
        console.log("收到消息:", event.data);
        // 根据需要解析 event.data 更新页面
        let data = JSON.parse(event.data);
        if(data.msg){
            now_msg_list.value.push({
                user_id:now_chat_user.value.user_id,
                msg: data.msg,
                time: now,
                avatar:now_chat_user.value.avatar,
            })
        }
    }

    ws.onerror = (error) => {
        console.error("WebSocket连接发生错误:", error);
    }
}

const messageArea = ref(null)

// 新增：发送消息后自动滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messageArea.value) {
      messageArea.value.scrollTop = messageArea.value.scrollHeight
    }
  })
}

// 在发送消息或收到新消息时调用
const sendMessage = () => {
    const data=new Date
    let now=data.getFullYear()+'-'+(data.getMonth()+1)+'-'+data.getDate()+' '+data.getHours()+':'+data.getMinutes()+':'+data.getSeconds()
    now_msg_list.value.push({
        user_id: user_id,
        msg: inputMessage.value,
        time: now,
        avatar: "default.jpg",
    })
    
  // 发送逻辑...
  if (ws && ws.readyState === WebSocket.OPEN) {
        let payload = {
            target_user_id: now_chat_user.value.user_id,  // 目标用户ID
            msg: inputMessage.value               // 消息内容
        };
        ws.send(JSON.stringify(payload));
    } else {
        console.error("WebSocket连接未打开");
    }
    inputMessage.value = "";
  scrollToBottom()
}
onMounted(async () => {
    await connect();
})
</script>

<style scoped>
.chat_container {
  display: flex;
  height: calc(100vh - 200px);
  background: #f0f2f5;
  width: 85%;
  margin: 0 auto;
}

/* 用户侧边栏样式 */
.user_sidebar {
  width: 280px;
  background: #fff;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.user_list {
  overflow-y: auto;
  flex: 1;
}

.user_item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background 0.3s;
}

.user_item:hover {
  background: #f5f5f5;
}

.user_item.active {
  background: #e8f4ff;
}

.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user_info {
  margin-left: 12px;
  flex: 1;
}

.username {
  font-weight: 500;
  color: #1a1a1a;
}

.status {
  display: block;
  width: 8px;
  height: 8px;
  background: #ccc;
  border-radius: 50%;
  margin-top: 4px;
}

/* 主聊天区域 */
.main_chat {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.message_area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.message_wrapper {
  margin-bottom: 16px;
}

.message_bubble {
  display: flex;
  align-items: flex-start;
  max-width: 70%;
  gap: 12px;
}

.own-message .message_bubble {
  flex-direction: row-reverse;
  margin-left: auto;
}

.message_content {
  max-width: calc(100% - 52px);
}

.message_text {
  padding: 12px 16px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  line-height: 1.5;
  word-break: break-word;
}

.own-message .message_text {
  background: #0084ff;
  color: white;
}

.message_time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  padding: 0 8px;
}

/* 输入区域 */
.input_area {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  background: #fff;
}

.input_wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
}

input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 24px;
  outline: none;
}

input:focus {
  border-color: #0084ff;
}

button {
  padding: 10px 20px;
  background: #0084ff;
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: opacity 0.3s;
}

button:hover {
  opacity: 0.9;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
</style>