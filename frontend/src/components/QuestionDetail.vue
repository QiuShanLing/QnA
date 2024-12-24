<template>
  <div class="question-detail">
    <div class="nav-bar">
      <button class="back-button" @click="goBack">
        <span class="icon">←</span> 返回列表
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadQuestion" class="retry-button">重试</button>
    </div>
    
    <div v-else-if="question" class="content">
      <div class="question-card">
        <div class="question-header">
          <h1>{{ question.title }}</h1>
          <div class="meta-info">
            <span class="id">#{{ question.id }}</span>
          </div>
        </div>
        
        <div class="section question-content">
          <h2>问题描述</h2>
          <div class="markdown-content" v-html="renderMarkdown(question.content)"></div>
        </div>
        
        <div class="section answer-section">
          <h2>答案</h2>
          <div v-if="!isEditing && question.answer" class="answer markdown-content" v-html="renderMarkdown(question.answer)"></div>
          <div v-if="!isEditing && !question.answer" class="no-answer">暂无答案</div>
          
          <div v-if="isEditing" class="answer-editor">
            <div class="editor-header">
              <span>编辑答案 (支持 Markdown 和 LaTeX 格式)</span>
              <a href="#" @click.prevent="showMarkdownHelp = true" class="markdown-help-link">格式帮助</a>
            </div>
            <textarea 
              v-model="editedAnswer" 
              class="answer-textarea markdown-textarea"
              placeholder="请输入答案（支持 Markdown 和 LaTeX 格式）

# Markdown 示例
- 支持**粗体**、*斜体*
- 支持代码块
- 支持数学公式

行内公式: $x^2$

块级公式:
$$
\sum_{i=1}^n i = \frac{n(n+1)}{2}
$$"
            ></textarea>
            <div class="preview-header">预览</div>
            <div class="markdown-preview" v-html="renderMarkdown(editedAnswer)"></div>
          </div>

          <div class="button-group">
            <template v-if="!isEditing">
              <button v-if="!question.answer" @click="startEditing" class="add-answer-btn">添加答案</button>
              <button v-else @click="startEditing" class="edit-answer-btn">编辑答案</button>
            </template>
            <template v-else>
              <button @click="saveAnswer" class="save-btn">保存</button>
              <button @click="cancelEditing" class="cancel-btn">取消</button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- Markdown 和 LaTeX 帮助对话框 -->
    <div v-if="showMarkdownHelp" class="dialog-overlay">
      <div class="dialog markdown-help-dialog">
        <h3>Markdown 与 LaTeX 语法帮助</h3>
        <div class="markdown-help-content">
          <h4>Markdown 基本语法</h4>
          <ul>
            <li><code># 标题1</code> - 一级标题</li>
            <li><code>## 标题2</code> - 二级标题</li>
            <li><code>**粗体**</code> - <strong>粗体</strong></li>
            <li><code>*斜体*</code> - <em>斜体</em></li>
            <li><code>[链接](URL)</code> - <a href="#">链接</a></li>
            <li><code>- 列表项</code> - 无序列表</li>
            <li><code>1. 列表项</code> - 有序列表</li>
          </ul>
          
          <h4>代码</h4>
          <ul>
            <li><code>`行内代码`</code> - 行内代码</li>
            <li>代码块：使用三个反引号包裹，可以指定语言</li>
          </ul>
          <pre><code>```python
def example():
    return "Hello World"
```</code></pre>

          <h4>LaTeX 数学公式</h4>
          <ul>
            <li><code>$...$</code> - 行内公式，例如：$E = mc^2$</li>
            <li><code>$$...$$</code> - 独立公式块，例如：</li>
          </ul>
          <pre><code>$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$</code></pre>
          <p>常用数学符号：</p>
          <ul>
            <li><code>\frac{a}{b}</code> - 分数</li>
            <li><code>^</code> - 上标，例如：$x^2$</li>
            <li><code>_</code> - 下标，例如：$x_i$</li>
            <li><code>\sum_{i=1}^n</code> - 求和符号</li>
            <li><code>\int</code> - 积分符号</li>
            <li><code>\sqrt{}</code> - 平方根</li>
          </ul>
        </div>
        <div class="dialog-buttons">
          <button @click="showMarkdownHelp = false" class="confirm-button">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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
      highlight: null,
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
  name: 'QuestionDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const question = ref(null)
    const isEditing = ref(false)
    const editedAnswer = ref('')
    const showMarkdownHelp = ref(false)
    const loading = ref(false)
    const error = ref(null)

    const loadQuestion = async () => {
      loading.value = true
      error.value = null
      try {
        const response = await axios.get(`http://localhost:8000/questions/${route.params.id}/`)
        question.value = response.data
      } catch (err) {
        console.error('Failed to load question:', err)
        error.value = '加载问题失败'
      } finally {
        loading.value = false
      }
    }

    const startEditing = () => {
      editedAnswer.value = question.value.answer || ''
      isEditing.value = true
    }

    const cancelEditing = () => {
      isEditing.value = false
      editedAnswer.value = ''
    }

    const saveAnswer = async () => {
      try {
        await axios.put(`http://localhost:8000/questions/${route.params.id}/answer`, {
          answer: editedAnswer.value
        })
        question.value.answer = editedAnswer.value
        isEditing.value = false
      } catch (error) {
        console.error('Error saving answer:', error)
        alert('保存答案失败')
      }
    }

    const goBack = () => {
      router.push('/')
    }

    onMounted(() => {
      loadQuestion()
    })

    return {
      question,
      loading,
      error,
      renderMarkdown,
      goBack,
      isEditing,
      editedAnswer,
      showMarkdownHelp,
      startEditing,
      cancelEditing,
      saveAnswer
    }
  }
}
</script>

<style scoped>
.question-detail {
  padding: 1rem;
}

.nav-bar {
  margin-bottom: 2rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #1976D2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: #1565C0;
  transform: translateY(-1px);
}

.icon {
  font-size: 1.2rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1976D2;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 2rem;
  background: #fff3f3;
  border-radius: 8px;
  margin: 2rem 0;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.question-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  overflow: hidden;
}

.question-header {
  background: #f8f9fa;
  padding: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.question-header h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 2rem;
  line-height: 1.3;
}

.meta-info {
  margin-top: 0.5rem;
  color: #6c757d;
}

.section {
  padding: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.section:last-child {
  border-bottom: none;
}

.section h2 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.markdown-content {
  line-height: 1.6;
  color: #333;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.markdown-content :deep(p) {
  margin: 1rem 0;
}

.markdown-content :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.markdown-content :deep(code) {
  font-family: 'Fira Code', monospace;
  font-size: 0.9em;
}

.markdown-content :deep(.katex-display) {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  overflow-x: auto;
}

.markdown-content :deep(.katex) {
  font-size: 1.1em;
}

.answer-section {
  margin-top: 30px;
}

.answer-section h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.no-answer {
  color: #666;
  font-style: italic;
}

.answer {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.button-group {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.add-answer-btn,
.edit-answer-btn,
.save-btn,
.cancel-btn,
.confirm-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.add-answer-btn,
.save-btn,
.confirm-button {
  background-color: #4CAF50;
  color: white;
}

.edit-answer-btn {
  background-color: #2196F3;
  color: white;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: white;
}

.add-answer-btn:hover,
.save-btn:hover,
.confirm-button:hover {
  background-color: #45a049;
}

.edit-answer-btn:hover {
  background-color: #1976D2;
}

.cancel-btn:hover {
  background-color: #757575;
}

.answer-editor {
  margin-bottom: 20px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.markdown-help-link {
  color: #3498db;
  text-decoration: none;
  font-size: 13px;
}

.markdown-help-link:hover {
  text-decoration: underline;
}

.markdown-textarea {
  width: 100%;
  min-height: 200px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
  margin-bottom: 10px;
  resize: vertical;
}

.preview-header {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.markdown-preview {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  min-height: 100px;
  max-height: 300px;
  overflow-y: auto;
  background: #fff;
  margin-bottom: 15px;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.markdown-help-dialog {
  max-width: 600px;
}

.markdown-help-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 0 15px;
}

.markdown-help-content h4 {
  margin: 1em 0 0.5em;
  color: #2c3e50;
}

.markdown-help-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.markdown-help-content li {
  margin: 0.5em 0;
}

.markdown-help-content code {
  background: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
}

.markdown-help-content pre {
  background: #f6f8fa;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
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

@media (max-width: 768px) {
  .question-header {
    padding: 1.5rem;
  }
  
  .question-header h1 {
    font-size: 1.5rem;
  }
  
  .section {
    padding: 1.5rem;
  }
}
</style>