import { createApp } from 'vue'
import { Quasar, Notify, Loading, Dialog } from 'quasar'
import quasarLang from 'quasar/lang/zh-CN.esm'

import App from './App.vue'
import router from './router'

import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import './css/app.scss'

const app = createApp(App)
app.use(router)
app.use(Quasar, { plugins: { Notify, Loading, Dialog }, lang: quasarLang })
app.mount('#app')
