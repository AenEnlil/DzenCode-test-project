import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { connectWS } from '@/services/websocket.js'
import {WS_BASE_URL} from '@/config.js'

connectWS(`${WS_BASE_URL}/ws/comments/`);
createApp(App).use(router).mount('#app')
