<template>
  <div :class="['register-page', { dark: isDark }]">
    <div class="content">
      <h2>注册新账号</h2>
      <form @submit.prevent="handleSubmit">
        <!-- 头像上传 -->
        <div class="avatar-upload">
          <label for="avatar">
            <img
              :src="avatarPreview || '/default-avatar.png'"
              class="avatar-preview"
            />
            <input
              type="file"
              id="avatar"
              accept="image/*"
              @change="handleAvatarUpload"
              hidden
            />
          </label>
          <span class="upload-hint">点击上传头像</span>
        </div>

        <!-- 表单字段 -->
        <div class="form-group">
          <input
            v-model="formData.username"
            placeholder="用户名"
            type="text"
            required
            @blur="validateField('username')"
          />
          <span class="error" v-if="errors.username">{{
            errors.username
          }}</span>
        </div>

        <div class="form-group">
          <input
            v-model="formData.password"
            placeholder="密码"
            type="password"
            required
            @blur="validatePassword"
          />
          <span class="error" v-if="errors.password">{{
            errors.password
          }}</span>
        </div>

        <div class="form-group">
          <input
            v-model="formData.confirmPassword"
            placeholder="确认密码"
            type="password"
            required
            @blur="validateConfirmPassword"
          />
          <span class="error" v-if="errors.confirmPassword">{{
            errors.confirmPassword
          }}</span>
        </div>

        <div class="form-group">
          <input
            v-model="formData.email"
            placeholder="电子邮箱"
            type="email"
            required
            @blur="validateField('email')"
          />
          <span class="error" v-if="errors.email">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <input
            v-model="formData.phone"
            placeholder="手机号码"
            type="tel"
            @blur="validateField('phone')"
          />
          <span class="error" v-if="errors.phone">{{ errors.phone }}</span>
        </div>

        <div class="form-group">
          <select v-model="formData.sex">
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>

        <div class="form-group">
          <textarea
            v-model="formData.signature"
            placeholder="个性签名"
            maxlength="100"
          ></textarea>
        </div>

        <!-- 状态提示 -->
        <div class="status-message" :class="statusClass">
          {{ statusMessage }}
        </div>

        <!-- 提交按钮 -->
        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? "注册中..." : "立即注册" }}
        </button>

        <!-- 已有账号登录 -->
        <div class="login-link">
          已有账号？
          <router-link to="/login">立即登录</router-link>
        </div>
      </form>

      <!-- 主题切换 -->
      <button class="theme-toggle" @click="toggleTheme">
        {{ isDark ? "🌞 白天模式" : "🌙 夜间模式" }}
      </button>
    </div>
  </div>
</template>

  <script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { BaseApi } from "@assets/base_api";

const router = useRouter();
const api = new BaseApi();

// 响应式数据
const isDark = ref(false);
const isSubmitting = ref(false);
const avatarFile = ref(null);
const avatarPreview = ref(null);

const formData = reactive({
  username: "",
  password: "",
  confirmPassword: "",
  email: "",
  phone: "",
  sex: "女",
  signature: "",
});

const errors = reactive({
  username: "",
  password: "",
  confirmPassword: "",
  email: "",
  phone: "",
});

const statusMessage = ref("");
const statusClass = ref("");

// 验证规则
const validationRules = {
  username: (value) => value.length >= 3 || "用户名至少3个字符",
  password: (value) => value.length >= 6 || "密码至少6个字符",
  email: (value) =>
    /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/.test(value) || "邮箱格式不正确",
  phone: (value) => !value || /^1[3-9]\d{9}$/.test(value) || "手机号格式不正确",
};

// 头像上传处理
const handleAvatarUpload = (e) => {
  const file = e.target.files[0];
  if (file) {
    if (!file.type.startsWith("image/")) {
      showStatus("请选择图片文件", "error");
      return;
    }
    avatarFile.value = file;
    avatarPreview.value = URL.createObjectURL(file);
  }
};

// 字段验证
const validateField = (field) => {
  const rule = validationRules[field];
  if (rule) {
    const isValid = rule(formData[field]);
    errors[field] = typeof isValid === "string" ? isValid : "";
    return isValid === true;
  }
  return true;
};

const validatePassword = () => {
  const valid = validateField("password");
  if (valid && formData.password !== formData.confirmPassword) {
    errors.confirmPassword = "两次密码输入不一致";
    return false;
  }
  return valid;
};

const validateConfirmPassword = () => {
  const valid = formData.password === formData.confirmPassword;
  errors.confirmPassword = valid ? "" : "两次密码输入不一致";
  return valid;
};

// 显示状态提示
const showStatus = (message, type = "error") => {
  statusMessage.value = message;
  statusClass.value = type;
  setTimeout(() => {
    statusMessage.value = "";
    statusClass.value = "";
  }, 3000);
};

// 提交处理
const handleSubmit = async () => {
  // 执行所有验证
  const validations = [
    validateField("username"),
    validateField("password"),
    validateConfirmPassword(),
    validateField("email"),
    validateField("phone"),
  ];

  if (validations.includes(false)) {
    showStatus("请正确填写所有必填字段");
    return;
  }

  isSubmitting.value = true;

  try {
    const form = new FormData();
    if (avatarFile.value) {
      form.append("file", avatarFile.value);
    }

    // 构造数据对象
    const payload = {
      username: formData.username,
      password: formData.password,
      email: formData.email,
      phone: formData.phone,
      sex: formData.sex,
      signature: formData.signature,
      background: "default_back.jpg",
    };

    form.append("data", JSON.stringify(payload));
    console.log(form.get("data"));

    const response = await fetch('http://localhost:8000/api/user/register',{
        method: 'POST',
        body:form
    })
    const response_data = await response.json()

    if (response_data.code === 200) {
      showStatus("注册成功，即将跳转到登录页面", "success");
      setTimeout(() => router.push("/login"), 1000);
    } else {
      showStatus(response_data.msg || "注册失败，请稍后重试");
    }
  } catch (error) {
    console.error("注册请求失败:", error);
    showStatus("网络错误，请检查连接后重试");
  } finally {
    isSubmitting.value = false;
  }
};

// 主题切换
const toggleTheme = () => {
  isDark.value = !isDark.value;
};
</script>

  <style scoped>
/* 基础样式 */
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  transition: background 0.3s, color 0.3s;
}

.content {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background: var(--bg-color);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* 夜间模式 */
.dark {
  background: #1a1a1a;
  color: #e6e6e6;
}

.dark .content {
  background: #2d2d2d;
}

/* 头像上传 */
.avatar-upload {
  text-align: center;
  margin-bottom: 1.5rem;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  cursor: pointer;
  object-fit: cover;
  border: 2px solid #ddd;
}

.upload-hint {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

/* 表单组 */
.form-group {
  margin-bottom: 1.2rem;
  position: relative;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  background: inherit;
  color: inherit;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #2196f3;
  outline: none;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2);
}

.error {
  display: block;
  color: #ff4444;
  font-size: 0.875rem;
  margin-top: 4px;
  text-align: left;
}

/* 状态提示 */
.status-message {
  margin: 1rem 0;
  padding: 10px;
  border-radius: 6px;
  text-align: center;
}

.status-message.success {
  background: #d4edda;
  color: #155724;
}

.status-message.error {
  background: #f8d7da;
  color: #721c24;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 12px;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:disabled {
  background: #90caf9;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  background: #1976d2;
  transform: translateY(-1px);
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.login-link a {
  color: #2196f3;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

/* 主题切换按钮 */
.theme-toggle {
  margin-top: 1.5rem;
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.8;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.3s;
}

.theme-toggle:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.1);
}
</style>