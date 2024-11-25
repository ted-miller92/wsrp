import './assets/main.css'

import { createApp} from 'vue'
import { createRouter , createWebHistory} from 'vue-router'
import { createPinia } from 'pinia'

import App from './App.vue'
import RegisterPage from './components/RegisterPage.vue'
import LoginPage from './components/LoginPage.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import CustomerDashboard from './components/CustomerDashboard.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/register', component: RegisterPage },
        { path: '/login', component: LoginPage},
        { path: '/adminDashboard', component: AdminDashboard },
        { path: '/customerDashboard', component: CustomerDashboard },
    ],
})

router.beforeEach((to, from) => {
    
})

const app = createApp(App)
app.use(router)
app.use(createPinia())

app.mount('#app')
