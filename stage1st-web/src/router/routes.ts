import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/IndexPage.vue') },
      { path: 'report', component: () => import('src/pages/ReportPage.vue') }
    ]
  },
  { path: '/:catchAll(.*)*', component: () => import('src/pages/ErrorNotFound.vue') }
]

export default routes
