<template>
  <div :class="['login-page', { dark: isDark }]">
    <div class="content">
      <h2>登录</h2>
      <div class="input">
        <!-- 用户名输入 -->
        <div class="input-group">
          <input
            placeholder="用户名"
            id="username"
            type="text"
            v-model="login_key"
            @blur="validateUsername"
          />
          <span class="error" v-if="usernameError">{{ usernameError }}</span>
        </div>

        <!-- 密码输入 -->
        <div class="input-group">
          <input
            placeholder="密码"
            id="password"
            type="password"
            v-model="password"
            @blur="validatePassword"
          />
          <span class="error" v-if="passwordError">{{ passwordError }}</span>
        </div>

        <!-- 登录状态提示 -->
        <div class="login-status">
          <span :class="['status-msg', statusClass]">{{ statusMsg }}</span>
        </div>

        <!-- 操作按钮区域 -->
        <div class="action-links">
          <div class="link-group">
            <span>没有账号？</span>
            <router-link to="/register" class="link">注册</router-link>
          </div>
          <div class="link-group">
            <span>忘记密码？</span>
            <router-link to="/reset_password" class="link"
              >重置密码</router-link
            >
          </div>
        </div>

        <!-- 登录按钮 -->
        <button class="login-btn" @click="handleLogin">登录</button>
      </div>

      <!-- 主题切换 -->
      <button class="theme-toggle" @click="toggleTheme">
        {{ isDark ? "🌞 白天模式" : "🌙 夜间模式" }}
      </button>
    </div>
  </div>
</template>

  <script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { BaseApi } from "@assets/base_api";

const router = useRouter();
const base_api = new BaseApi();

// 响应式数据
const login_key = ref("");
const password = ref("");
const isDark = ref(false);
const usernameError = ref("");
const passwordError = ref("");
const statusMsg = ref("");
const statusClass = ref("");

// 验证逻辑
const validateUsername = () => {
  if (!login_key.value.trim()) {
    usernameError.value = "＊用户名不能为空";
    return false;
  }
  usernameError.value = "";
  return true;
};

const validatePassword = () => {
  if (!password.value.trim()) {
    passwordError.value = "＊密码不能为空";
    return false;
  }
  passwordError.value = "";
  return true;
};

// 登录处理
async function handleLogin() {
  if (!validateUsername() | !validatePassword()) return;

  try {
    const res = await base_api.post("login/", {
      login_key: login_key.value,
      password: password.value,
    });

    if (res.status === 200) {
      statusClass.value = "success";
      statusMsg.value = "登录成功，正在跳转...";
      localStorage.setItem("token", res.result.token);
      setTimeout(() => router.push("/"), 1000);
    } else {
      statusClass.value = "error";
      statusMsg.value = res.msg || "登录失败，请检查输入";
    }
  } catch (e) {
    console.error(e);
    statusClass.value = "error";
    statusMsg.value = "网络错误，请稍后重试";
  }
}

// 主题切换
const toggleTheme = () => {
  isDark.value = !isDark.value;
};
</script>

  <style scoped>
/* 基础样式 */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  transition: all 0.3s ease;
}

/* 白天模式 */
.login-page {
  background: #f0f2f5;
  color: #333;
}

/* 夜间模式 */
.login-page.dark {
  background: #1a1a1a;
  color: #e6e6e6;
}

.content {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background: inherit;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 1.5rem;
  position: relative;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: inherit;
  color: inherit;
}

/* 输入框焦点样式 */
input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2);
}

/* 错误提示 */
.error {
  display: block;
  color: #ff4444;
  font-size: 0.875rem;
  margin-top: 4px;
  text-align: left;
}

/* 登录状态提示 */
.login-status {
  margin: 1rem 0;
  min-height: 24px;
}

.status-msg {
  font-size: 0.875rem;
}

.status-msg.success {
  color: #00c851;
}

.status-msg.error {
  color: #ff4444;
}

/* 操作链接 */
.action-links {
  display: flex;
  justify-content: space-between;
  margin: 1.5rem 0;
}

.link-group {
  font-size: 0.875rem;
}

.link {
  color: #2196f3;
  text-decoration: none;
  transition: color 0.3s ease;
}

.link:hover {
  color: #1976d2;
  text-decoration: underline;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 12px;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background: #1976d2;
  transform: translateY(-1px);
}

/* 主题切换按钮 */
.theme-toggle {
  margin-top: 1.5rem;
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.theme-toggle:hover {
  opacity: 1;
}

/* 夜间模式适配 */
.login-page.dark input {
  border-color: #555;
}

.login-page.dark input:focus {
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.3);
}

.login-page.dark .link {
  color: #64b5f6;
}

.login-page.dark .link:hover {
  color: #42a5f5;
}
</style>