import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";

import App from "./App.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import CustomerDashboard from "./components/CustomerDashboard.vue";
import HomeScreen from "./components/HomeScreen.vue";
import "./assets/main.css"; // ✅ Ensure this line is present

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomeScreen }, // Show HomeScreen at root path
    { path: "/home", redirect: "/" }, // Redirect /home to root path
    { path: "/register", component: RegisterPage },
    { path: "/login", component: LoginPage },
    { path: "/adminDashboard", component: AdminDashboard },
    { path: "/customerDashboard", component: CustomerDashboard },
  ],
});

const app = createApp(App);
app.use(router);
app.use(createPinia());

app.mount("#app");
