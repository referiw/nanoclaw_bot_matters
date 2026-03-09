import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('../pages/IndexPage.vue') },
  { path: '/report', name: 'Report', component: () => import('../pages/ReportPage.vue') },
  { path: '/history', name: 'History', component: () => import('../pages/HistoryPage.vue') },
  { path: '/about', name: 'About', component: () => import('../pages/AboutPage.vue') },
  { path: '/:catchAll(.*)*', component: () => import('../pages/ErrorNotFound.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
