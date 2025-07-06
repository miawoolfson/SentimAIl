import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/alerts',
    name: 'alerts',
    component: () => import('../views/AlertsView.vue')
  },
  {
    path: '/sentiment-analysis',
    name: 'sentiment-analysis',
    component: () => import('../views/SentimentAnalysisView.vue')
  },
  {
    path: '/subjects',
    name: 'subjects',
    component: () => import('../views/SubjectsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router