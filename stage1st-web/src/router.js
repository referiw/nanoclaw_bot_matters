import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('./pages/IndexPage.vue') },
  { path: '/:pathMatch(.*)*', component: () => import('./pages/IndexPage.vue') }
]

export default createRouter({ history: createWebHistory(), routes })
