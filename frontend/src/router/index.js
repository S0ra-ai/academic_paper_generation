import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import ReportGenerator from '../components/ReportGenerator.vue'
import ReportList from '../components/ReportList.vue'
import ReportDetail from '../components/ReportDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/generate',
    name: 'ReportGenerator',
    component: ReportGenerator
  },
  {
    path: '/reports',
    name: 'ReportList',
    component: ReportList
  },
  {
    path: '/reports/:id',
    name: 'ReportDetail',
    component: ReportDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
