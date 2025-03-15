<template>
  <div class="write-container">
    <div class="head">
      <div class="work_info">
        <div class="work_name">
          《{{ work_info.name }}》{{ work_info.volume }}
        </div>
        <div class="last_time">
          上次提交：{{ work_info.last_time || "无记录" }} | 当前字数：{{
            now_work_info.word_count
          }}字
        </div>
      </div>
      <div class="submit">
        <button :disabled="isSubmitting" @click="handleSubmit">
          {{ isSubmitting ? "提交中..." : "提交章节" }}
        </button>
      </div>
    </div>

    <div class="main">
      <div class="title-input">
        <input
          v-model="now_work_info.chapter_num"
          type="number"
          min="1"
          placeholder="章节编号"
          class="chapter_num"
        />
        <input
          v-model="now_work_info.title"
          type="text"
          placeholder="章节标题（最多30字）"
          maxlength="30"
          class="chapter_name"
        />
      </div>

      <!-- 富文本编辑器 -->
      <QuillEditor
        v-model:content="now_work_info.content"
        contentType="html"
        :options="editorOptions"
        @text-change="updateWordCount"
      />
    </div>
  </div>
</template>
  
  <script setup>
import { ref, reactive } from "vue";
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import { BaseApi } from "@assets/base_api";

const api = new BaseApi();
const isSubmitting = ref(false);

// 作品信息
const work_info = reactive({
  name: "作品1",
  volume: "第一卷",
  last_time: "2023-08-20 14:30",
});

// 当前章节信息
const now_work_info = reactive({
  title: "",
  chapter_num: "",
  content: "",
  word_count: 0,
});

// 富文本编辑器配置
const editorOptions = {
  modules: {
    toolbar: {
      container: [
        ["bold", "italic", "underline", "strike"],
        ["blockquote", "code-block"],
        [{ header: 1 }, { header: 2 }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ script: "sub" }, { script: "super" }],
        [{ indent: "-1" }, { indent: "+1" }],
        [{ direction: "rtl" }],
        [{ size: ["small", false, "large", "huge"] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        [{ color: [] }, { background: [] }],
        [{ font: [] }],
        [{ align: [] }],
        ["link", "image", "video"],
        ["clean"],
      ],
      handlers: {
        image: imageHandler,
      },
    },
  },
  placeholder: "请输入正文内容...",
  theme: "snow",
};

// 图片上传处理
async function imageHandler() {
  const input = document.createElement("input");
  input.setAttribute("type", "file");
  input.setAttribute("accept", "image/*");
  input.click();

  input.onchange = async () => {
    const file = input.files[0];
    if (!file) return;

    try {
      const formData = new FormData();
      formData.append("image", file);

      const res = await api.post("/upload/image", formData);
      const quill = this.quill;
      const range = quill.getSelection(true);
      quill.editor.insertEmbed(range.index, "image", res.data.url);
      quill.setSelection(range.index + 1);
    } catch (error) {
      console.error("图片上传失败:", error);
    }
  };
}

// 字数统计
function updateWordCount() {
  const text = now_work_info.content.replace(/<[^>]*>/g, ""); // 去除HTML标签
  now_work_info.word_count = text.length;
}

// 提交章节
async function handleSubmit() {
  if (!validateForm()) return;

  try {
    isSubmitting.value = true;
    const res = await api.post("/chapter/create", {
      work_id: work_info.id,
      chapter_num: now_work_info.chapter_num,
      title: now_work_info.title,
      content: now_work_info.content,
    });

    if (res.status === 200) {
      work_info.last_time = new Date().toLocaleString();
      resetForm();
    }
  } finally {
    isSubmitting.value = false;
  }
}

// 表单校验
function validateForm() {
  if (!now_work_info.chapter_num) {
    alert("请填写章节编号");
    return false;
  }
  if (!now_work_info.title) {
    alert("请填写章节标题");
    return false;
  }
  if (!now_work_info.content) {
    alert("请填写正文内容");
    return false;
  }
  return true;
}

// 重置表单
function resetForm() {
  now_work_info.chapter_num = "";
  now_work_info.title = "";
  now_work_info.content = "";
  now_work_info.word_count = 0;
}
</script>
  
  <style scoped>
.write-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f5f7fa;
  border-radius: 8px;
}

.work_name {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1a1a1a;
}

.last_time {
  color: #909399;
  font-size: 0.9rem;
}

.submit button {
  padding: 0.8rem 2rem;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.submit button:hover:not(:disabled) {
  background: #3375e0;
}

.submit button:disabled {
  background: #a0cfff;
  cursor: not-allowed;
}

.title-input {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.title-input input {
  padding: 0.8rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.title-input input:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 富文本编辑器样式覆盖 */
:deep(.ql-toolbar) {
  border-radius: 8px 8px 0 0;
  border-color: #dcdfe6 !important;
}

:deep(.ql-container) {
  border-radius: 0 0 8px 8px;
  border-color: #dcdfe6 !important;
  min-height: 500px;
  font-size: 16px;
}
</style>