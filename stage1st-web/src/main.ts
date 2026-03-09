import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify, Loading, Dialog } from 'quasar'
import quasarLang from 'quasar/lang/zh-CN'

import App from './App.vue'
import router from './router'

import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'
import 'quasar/src/css/index.sass'
import './css/app.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: { Notify, Loading, Dialog },
  lang: quasarLang,
  config: {
    dark: 'auto'
  }
})

app.mount('#q-app')
