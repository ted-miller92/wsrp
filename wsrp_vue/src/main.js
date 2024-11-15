import './assets/main.css'

import { createApp} from 'vue'
import { createRouter , createWebHistory} from 'vue-router'

import App from './App.vue'
import Register from './components/Register.vue'
import Login from './components/Login.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import CustomerDashboard from './components/CustomerDashboard.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/register', component: Register },
        { path: '/login', component: Login },
        { path: '/adminDashboard', component: AdminDashboard },
        { path: '/customerDashboard', component: CustomerDashboard },
    ],
})

const app = createApp(App)
app.use(router)

app.mount('#app')
