<template>
  <div class="home">
    <div class="top-bar">
      <div class="search-box">
        <input 
          type="text" 
          class="search-input" 
          placeholder="搜索问题..."
          v-model="searchQuery"
          @keyup.enter="handleSearch"
        >
        <button class="search-button" @click="handleSearch">搜索</button>
      </div>
      <button @click="showAddDialog = true" class="add-question-button">添加问题</button>
    </div>

    <!-- 问题列表 -->
    <div v-if="searchResults !== null" class="search-results">
      <div class="search-results-header">
        <div class="back-button" @click="clearSearch">
          <span class="arrow-left">←</span>
        </div>
        <h2>搜索结果</h2>
      </div>
      <div class="questions-grid">
        <router-link 
          v-for="question in searchResults" 
          :key="question.id" 
          :to="{ name: 'QuestionDetail', params: { id: question.id }}"
          class="question-card"
          :class="{ 'has-answer': question.answer }"
        >
          <div class="question-header">
            <span class="question-id">#{{ question.id }}</span>
            <span class="answer-status" :class="{ 'answered': question.answer }">
              {{ question.answer ? '已解答' : '待解答' }}
            </span>
          </div>
          <h3 class="question-title">{{ question.title }}</h3>
          <p class="question-content" v-if="question.content">{{ question.content }}</p>
        </router-link>
      </div>
    </div>
    <template v-else>
      <div class="questions-grid">
        <router-link 
          v-for="question in questions" 
          :key="question.id" 
          :to="{ name: 'QuestionDetail', params: { id: question.id }}"
          class="question-card"
          :class="{ 'has-answer': question.answer }"
        >
          <div class="question-header">
            <span class="question-id">#{{ question.id }}</span>
            <span class="answer-status" :class="{ 'answered': question.answer }">
              {{ question.answer ? '已解答' : '待解答' }}
            </span>
          </div>
          <h3 class="question-title">{{ question.title }}</h3>
          <p class="question-content" v-if="question.content">{{ question.content }}</p>
        </router-link>
      </div>
    </template>
    <!-- 添加问题对话框 -->
    <div v-if="showAddDialog" class="dialog-overlay">
      <div class="dialog">
        <h2>添加新问题</h2>
        <div class="form-group">
          <label>标题：</label>
          <input v-model="newQuestion.title" type="text">
        </div>
        <div class="form-group">
          <label>内容：</label>
          <div class="editor-container">
            <textarea 
              v-model="newQuestion.content" 
              placeholder="支持 Markdown 和 LaTeX 公式"
            ></textarea>
            <div v-if="newQuestion.content" class="preview">
              <h4>预览：</h4>
              <div class="markdown-content" v-html="renderMarkdown(newQuestion.content)"></div>
            </div>
          </div>
          <button class="help-button" @click="showMarkdownHelp = true">
            Markdown & LaTeX 帮助
          </button>
        </div>
        <div class="dialog-buttons">
          <button @click="addQuestion">保存</button>
          <button @click="showAddDialog = false">取消</button>
        </div>
      </div>
    </div>

    <!-- Markdown 帮助对话框 -->
    <div v-if="showMarkdownHelp" class="dialog-overlay">
      <div class="dialog markdown-help">
        <h2>Markdown & LaTeX 帮助</h2>
        <div class="help-content">
          <h3>Markdown 语法：</h3>
          <ul>
            <li><code># 标题1</code></li>
            <li><code>## 标题2</code></li>
            <li><code>**粗体**</code></li>
            <li><code>*斜体*</code></li>
            <li><code>[链接](URL)</code></li>
            <li><code>- 列表项</code></li>
            <li><code>1. 有序列表</code></li>
            <li><code>\`代码\`</code></li>
          </ul>
          <h3>LaTeX 公式：</h3>
          <ul>
            <li>行内公式：<code>$E = mc^2$</code></li>
            <li>块级公式：<code>$$\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$</code></li>
          </ul>
          <p>注意：块级公式需要前后换行</p>
        </div>
        <button @click="showMarkdownHelp = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import katex from 'katex'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import 'katex/dist/katex.css'

// 处理数学公式
function renderLatex(text) {
  if (!text) return ''
  
  // 先处理块级公式
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
    try {
      return katex.renderToString(formula.trim(), { displayMode: true })
    } catch (err) {
      console.warn('Failed to render block formula:', err)
      return match
    }
  })
  
  // 再处理行内公式
  text = text.replace(/([^$])\$([^$]+?)\$([^$])/g, (match, p1, formula, p2) => {
    try {
      return p1 + katex.renderToString(formula.trim(), { displayMode: false }) + p2
    } catch (err) {
      console.warn('Failed to render inline formula:', err)
      return match
    }
  })
  
  return text
}

// 渲染 Markdown
function renderMarkdown(text) {
  if (!text) return ''
  
  try {
    // 先处理数学公式
    const processedText = renderLatex(text)
    
    // 再渲染 Markdown
    const renderer = new marked.Renderer()
    
    // 配置代码高亮
    renderer.code = (code, language) => {
      const validLanguage = hljs.getLanguage(language) ? language : 'plaintext'
      return `<pre><code class="hljs ${validLanguage}">${
        hljs.highlight(code, { language: validLanguage }).value
      }</code></pre>`
    }
    
    marked.setOptions({
      renderer,
      highlight: null, // 因为我们在 renderer.code 中已经处理了高亮
      breaks: true,
      gfm: true
    })
    
    return marked(processedText)
  } catch (error) {
    console.error('Markdown parsing error:', error)
    return text
  }
}

export default {
  name: 'HomePage',
  setup() {
    const questions = ref([])
    const searchQuery = ref('')
    const searchResults = ref(null)
    const showAddDialog = ref(false)
    const showMarkdownHelp = ref(false)
    const newQuestion = ref({
      title: '',
      content: ''
    })
    const loading = ref(false)
    const error = ref(null)

    // 加载所有问题
    const loadQuestions = async () => {
      loading.value = true
      error.value = null
      try {
        const response = await axios.get('http://localhost:8000/questions/')
        questions.value = response.data
      } catch (err) {
        console.error('Failed to load questions:', err)
        error.value = '加载问题失败'
      } finally {
        loading.value = false
      }
    }

    // 搜索问题
    const handleSearch = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = null
        return
      }

      loading.value = true
      error.value = null
      try {
        const response = await axios.get(`http://localhost:8000/questions/search/?keyword=${encodeURIComponent(searchQuery.value)}`)
        searchResults.value = response.data
      } catch (err) {
        console.error('Search failed:', err)
        error.value = '搜索失败'
      } finally {
        loading.value = false
      }
    }

    // 清除搜索
    const clearSearch = () => {
      searchQuery.value = ''
      searchResults.value = null
    }

    // 添加新问题
    const addQuestion = async () => {
      if (!newQuestion.value.title.trim() || !newQuestion.value.content.trim()) {
        alert('标题和内容不能为空')
        return
      }

      loading.value = true
      error.value = null
      try {
        await axios.post('http://localhost:8000/questions/', newQuestion.value)
        await loadQuestions()
        showAddDialog.value = false
        newQuestion.value = { title: '', content: '' }
      } catch (err) {
        console.error('Failed to add question:', err)
        error.value = '添加问题失败'
      } finally {
        loading.value = false
      }
    }

    // 导航到问题页面
    const navigateToQuestion = (question) => {
      // 使用前端路由
      const baseUrl = window.location.origin
      window.location.href = `${baseUrl}/#/question/${question.id}`
    }

    // 在组件挂载时加载问题
    onMounted(() => {
      loadQuestions()
    })

    return {
      questions,
      searchQuery,
      searchResults,
      showAddDialog,
      showMarkdownHelp,
      newQuestion,
      loading,
      error,
      renderMarkdown,
      handleSearch,
      clearSearch,
      addQuestion,
      navigateToQuestion
    }
  }
}
</script>

<style scoped>
.home {
  padding: 1rem;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  background: white;
  padding: 0.5rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  align-items: center;
  width: 300px;
}

.search-input {
  flex: 1;
  padding: 0.4rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-button, .add-question-button {
  padding: 0.4rem 1rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  height: 30px;
  line-height: 1;
}

.search-button {
  background: #1976D2;
}

.add-question-button {
  background: #4CAF50;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.question-card {
  background: white;
  border-radius: 6px;
  padding: 0.75rem;
  text-decoration: none;
  color: inherit;
  border: 1px solid #eee;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
}

.question-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.question-card.has-answer {
  border-left: 3px solid #4CAF50;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4rem;
}

.question-id {
  color: #666;
  font-size: 0.85rem;
}

.answer-status {
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  background: #f0f0f0;
  color: #666;
}

.answer-status.answered {
  background: #E8F5E9;
  color: #2E7D32;
}

.question-title {
  margin: 0 0 0.4rem 0;
  font-size: 1rem;
  font-weight: 500;
  color: #2c3e50;
  line-height: 1.3;
}

.question-content {
  margin: 0;
  font-size: 0.85rem;
  color: #666;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-group textarea {
  min-height: 200px;
  font-family: monospace;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.dialog-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.dialog-buttons button:first-child {
  background-color: #4CAF50;
  color: white;
}

.dialog-buttons button:last-child {
  background-color: #f44336;
  color: white;
}

.help-button {
  margin-top: 10px;
  padding: 4px 8px;
  background-color: #607D8B;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.markdown-help {
  max-width: 600px;
}

.help-content {
  margin: 20px 0;
}

.help-content h3 {
  margin: 15px 0 10px;
}

.help-content ul {
  list-style: none;
  padding: 0;
}

.help-content li {
  margin: 5px 0;
}

.help-content code {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}

.editor-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.preview {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  background-color: #f9f9f9;
}

.preview h4 {
  margin: 0 0 10px 0;
  color: #666;
}

.search-results-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.back-button {
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.arrow-left {
  font-size: 1.5rem;
  line-height: 1;
  color: #666;
}

.search-results-header h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 500;
  color: #2c3e50;
}

.main-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin: 1rem 0;
}

/* LaTeX 样式 */
:deep(.katex-display) {
  margin: 1em 0;
  overflow-x: auto;
  overflow-y: hidden;
}

:deep(.katex) {
  font-size: 1.1em;
  font-family: KaTeX_Math, 'Times New Roman', Times, serif;
}

:deep(.katex-html) {
  overflow-x: auto;
  overflow-y: hidden;
}

:deep(.markdown-content) {
  line-height: 1.6;
}

:deep(.markdown-content p) {
  margin: 1em 0;
}

:deep(.hljs) {
  padding: 1em;
  border-radius: 4px;
  background-color: #f6f8fa;
}
</style>