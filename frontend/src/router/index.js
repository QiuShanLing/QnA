import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
import QuestionDetail from '../components/QuestionDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/question/:id',
    name: 'QuestionDetail',
    component: QuestionDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
