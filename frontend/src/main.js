import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

const app = createApp(App)
app.use(ElementPlus)
app.config.globalProperties.$axios = axios.create({
  baseURL: 'http://localhost:5000'
})
app.mount('#app')
