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
          <span>{{sava_status==0?'未保存':sava_status==1?'已保存':sava_status==2?'保存中...':'保存失败'}}</span>
        </div>
      </div>
      <div class="choose_vip_chapter" style="display:flex;align-items:center;">
        <div class="vip">VIP章节</div>
        <select v-model="work_info.is_vip">
          <option value="0">否</option>
          <option value="1">是</option>
        </select>
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

      <!-- 替换原来的 QuillEditor，预留一个容器 -->
      <div id="fluent-editor" class="editor"></div>
    </div>
  </div>
</template>
  
  
<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, watch } from "vue";
import FluentEditor from "@opentiny/fluent-editor";
import "@opentiny/fluent-editor/style.css";
import { BaseApi } from "@assets/base_api";

const api = new BaseApi();
const isSubmitting = ref(false);
let sava_status = ref(0);

// 作品信息
const work_info = reactive({
  name: "作品1",
  volume: "第一卷",
  last_time: "2023-08-20 14:30",
  novel_id:1, // 传入的书籍id
  is_vip:0
});

// 当前章节信息
const now_work_info = reactive({
  title: "",
  chapter_num: 10,
  content: "",
  word_count: 0,
  novel_id:1, // 传入的书籍id
});

let editorInstance = null;

// Fluent Editor 配置，与之前Quill类似，不过可扩展更多功能
const editorOptions = {
  theme: "snow",
  modules: {
    toolbar: {
      // 可参考 Fluent Editor 的内置工具栏选项，支持Quill内置按钮和扩展按钮
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
        // 例如增加格式刷、附件、@提醒等扩展按钮
        // ["format-painter", "file", "mention", "emoji"],
      ],
      handlers: {
        image: imageHandler, // 保持图片上传处理函数不变或根据Fluent Editor要求调整
      },
    },
  },
  placeholder: "请输入正文内容...",
};

async function imageHandler() {
  // 此处逻辑与Quill类似，根据Fluent Editor的API调用调整
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
      console.log("开始上传图片:", file);

      let res = await fetch("http://localhost:8000/api/upload/image", {
        method: "post",
        body: formData,
        headers: {
          Authorization: `token ${localStorage.getItem("token")}`,
        },
      });
      res = await res.json();
      console.log(res);
      if (res.code == 200) {
        // 根据 Fluent Editor 的 API 获取编辑器实例和当前选择
        const range = editorInstance.getSelection(true);
        console.log("图片上传成功:", res.data.url);
        editorInstance.insertEmbed(range.index, "image", res.data.url);
        editorInstance.setSelection(range.index + 1);
      } else {
        console.log("图片上传失败:", res);
      }
    } catch (error) {
      console.error("图片上传失败:", error);
    }
  };
}

watch(
  () => now_work_info,
  (newVal) => {
    sava_status.value = 2;
    updateWordCount();
    localStorage.setItem("temp_content", JSON.stringify(newVal)); // 监听内容变化并保存到本地存储
    setTimeout(() => {
      sava_status.value = 1;
    }, 100);
  },
  { deep: true }
);

function updateWordCount() {
  // 计算去除HTML标签的字数
  if (!now_work_info.content) {
    now_work_info.word_count = 0;
    return;
  }
  const text = now_work_info.content.replace(/<[^>]*>/g, "");
  now_work_info.word_count = text.length;
}

function handleContentChange(delta, oldDelta, source) {
  // 更新 now_work_info.content（可通过 editorInstance.root.innerHTML 获取内容）
  now_work_info.content = editorInstance.root.innerHTML;
  updateWordCount();
}

// 提交章节函数保持不变
async function handleSubmit() {
  if (!validateForm()) return;

  try {
    isSubmitting.value = true;
    const res = await api.post("api/upload/chapter", {
      novel_id: work_info.novel_id,
      chapter_num: now_work_info.chapter_num,
      title: now_work_info.title,
      content: now_work_info.content,
    });

    if (res.status === 200) {
      work_info.last_time = new Date().toLocaleString();
      resetForm();
      alert("提交成功");
      localStorage.removeItem("temp_content"); // 提交成功后清除本地存储
    }
    else{
      console.log(res)
    }
  } finally {
    isSubmitting.value = false;
  }
}

function validateForm() {
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

function resetForm() {
  now_work_info.chapter_num = "";
  now_work_info.title = "";
  now_work_info.content = "";
  now_work_info.word_count = 0;
}

//校验小说资质
async function check_work() {
  const res=await api.post('api/get_info/get_work_qualification',{
    novel_id:work_info.novel_id
  })
  if(res.status==200){
    work_info.is_vip=res.result.data.is_vip
    if(res.result.data.work_status==1){
      alert('小说已被封禁')
      window.location.href='/'
    }
  }
  else{
    console.log(res)
    work_info.is_vip=0
  }
}

onMounted(async () => {
  // 初始化 Fluent Editor，传入容器ID和配置
  editorInstance = new FluentEditor("#fluent-editor", editorOptions);

  // 如果 Fluent Editor 提供了事件监听（类似 Quill 的 'text-change'），绑定内容变化事件
  editorInstance.on("text-change", handleContentChange);
  let temp_content = localStorage.getItem("temp_content");
  if (temp_content) {
    temp_content = JSON.parse(temp_content);
    now_work_info.chapter_num = temp_content.chapter_num;
    now_work_info.title = temp_content.title;
    now_work_info.content = temp_content.content;
    // 同步加载内容到编辑器
    editorInstance.root.innerHTML = temp_content.content;
  }
  await check_work();
});

onBeforeUnmount(() => {
  if (editorInstance) {
    editorInstance.off("text-change", handleContentChange);
    editorInstance.destroy();
  }
});
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
/* Fluent Editor 的容器样式 */
.editor {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  min-height: 500px;
  font-size: 16px;
  padding: 1rem;
}
</style>