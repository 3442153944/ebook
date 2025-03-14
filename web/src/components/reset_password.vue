<script setup lang="ts">
import { BaseApi } from '@assets/base_api';
import { useStore } from '@/model/store';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const api = new BaseApi()
const store = useStore()
const router = useRouter()

// 响应式数据
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const infoMsg = ref('')
const showPassword = ref(false)
const isLoading = ref(false)

// 密码复杂度正则
const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{6,}$/

// 计算属性
const passwordsMatch = computed(() => 
  password.value === confirmPassword.value && password.value !== ''
)

const isValidEmail = computed(() => 
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)
)

// 表单验证
const validateForm = () => {
  if (!username.value) {
    infoMsg.value = '请输入用户名'
    return false
  }
  if (!email.value) {
    infoMsg.value = '请输入邮箱'
    return false
  }
  if (!isValidEmail.value) {
    infoMsg.value = '邮箱格式不正确'
    return false
  }
  if (!password.value) {
    infoMsg.value = '请输入新密码'
    return false
  }
  if (!passwordRegex.test(password.value)) {
    infoMsg.value = '密码需至少8位且包含字母和数字'
    return false
  }
  if (!passwordsMatch.value) {
    infoMsg.value = '两次输入的密码不一致'
    return false
  }
  return true
}

// 密码重置逻辑
async function resetPassword() {
  if (!validateForm()) return
  
  try {
    isLoading.value = true
    const res = await api.post('api/user/reset_password', {
      username: username.value,
      email: email.value,
      password: password.value
    })

    if (res.status === 200) {
      infoMsg.value = '密码重置成功，即将跳转到登录页'
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      handleError(res.status)
    }
  } catch (error) {
    infoMsg.value = '请求失败，请检查网络连接'
  } finally {
    isLoading.value = false
  }
}

// 错误处理
const handleError = (status: number) => {
  const errors: Record<number, string> = {
    401: '用户名或邮箱验证失败',
    404: '用户不存在',
    500: '服务器错误，请稍后再试'
  }
  infoMsg.value = errors[status] || '密码重置失败'
}

// 切换密码可见性
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>

<template>
  <div class="auth-page">
    <div class="card">
      <h2>重置密码</h2>
      
      <div class="form-group">
        <input 
          type="text" 
          placeholder="用户名"
          v-model="username"
          :disabled="isLoading"
        >
      </div>

      <div class="form-group">
        <input
          type="email"
          placeholder="注册邮箱"
          v-model="email"
          :disabled="isLoading"
        >
      </div>

      <div class="form-group password-input">
        <input
          :type="showPassword ? 'text' : 'password'"
          placeholder="新密码（至少8位含字母和数字）"
          v-model="password"
          :disabled="isLoading"
        >
        <button 
          class="toggle-password"
          @click="togglePasswordVisibility"
          type="button"
        >
          {{ showPassword ? '👁️' : '👁️🗨️' }}
        </button>
      </div>

      <div class="form-group">
        <input
          :type="showPassword ? 'text' : 'password'"
          placeholder="确认新密码"
          v-model="confirmPassword"
          :disabled="isLoading"
          @keyup.enter="resetPassword"
        >
      </div>

      <div class="message" :class="{ error: infoMsg, success: infoMsg?.includes('成功') }">
        {{ infoMsg }}
      </div>

      <button 
        class="submit-btn"
        @click="resetPassword"
        :disabled="isLoading || !passwordsMatch"
      >
        <span v-if="!isLoading">重置密码</span>
        <span v-else>处理中...</span>
      </button>

      <div class="links">
        <router-link to="/login">返回登录</router-link>
        <router-link to="/register">注册账号</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
  position: relative;
}

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.message {
  margin: 1rem 0;
  padding: 8px;
  border-radius: 4px;
  text-align: center;
}

.message.error {
  background: #ffe3e3;
  color: #dc3545;
}

.message.success {
  background: #d4edda;
  color: #155724;
}

.links {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

.links a {
  color: #007bff;
  text-decoration: none;
  font-size: 0.9rem;
}

.links a:hover {
  text-decoration: underline;
}
</style>