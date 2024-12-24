<template>
  <div class="question-list">
    <div class="header">
      <h2>编程语言示例</h2>
      <button class="add-button" @click="showAddDialog = true">添加问题</button>
    </div>

    <!-- 问题列表 -->
    <div v-for="question in questions" :key="question.id" 
         class="question-item" 
         :class="{ 'no-answer': !question.answer }"
         @click="selectQuestion(question)">
      <h3>{{ question.title }}</h3>
      <span class="status-badge" :class="{ 'answered': question.answer }">
        {{ question.answer ? '已解答' : '待解答' }}
      </span>
    </div>

    <!-- 添加问题对话框 -->
    <div v-if="showAddDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>添加新问题</h3>
        <input v-model="newQuestion.title" placeholder="问题标题" />
        <textarea v-model="newQuestion.content" placeholder="问题内容"></textarea>
        <div class="dialog-buttons">
          <button @click="addQuestion">确认</button>
          <button @click="showAddDialog = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'QuestionList',
  emits: ['select-question'],
  setup(props, { emit }) {
    const questions = ref([])
    const showAddDialog = ref(false)
    const newQuestion = ref({
      title: '',
      content: ''
    })

    const fetchQuestions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/questions/')
        questions.value = response.data
      } catch (error) {
        console.error('获取问题列表失败:', error)
      }
    }

    const addQuestion = async () => {
      try {
        await axios.post('http://localhost:8000/questions/', newQuestion.value)
        showAddDialog.value = false
        newQuestion.value = { title: '', content: '' }
        await fetchQuestions()
      } catch (error) {
        console.error('添加问题失败:', error)
      }
    }

    const selectQuestion = (question) => {
      emit('select-question', question)
    }

    onMounted(() => {
      fetchQuestions()
    })

    return {
      questions,
      selectQuestion,
      showAddDialog,
      newQuestion,
      addQuestion
    }
  }
}
</script>

<style scoped>
.question-list {
  padding: 20px;
  border-right: 1px solid #eee;
  position: relative;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-button:hover {
  background-color: #45a049;
}

.question-item {
  padding: 15px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-item:hover {
  background-color: #f5f5f5;
}

.question-item.no-answer {
  border-left: 3px solid #ff9800;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  background-color: #ff9800;
  color: white;
}

.status-badge.answered {
  background-color: #4CAF50;
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
}

.dialog {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.dialog input,
.dialog textarea {
  width: 100%;
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.dialog textarea {
  height: 100px;
  resize: vertical;
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
</style>