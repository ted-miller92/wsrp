import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";

import App from "./App.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import CustomerDashboard from "./components/CustomerDashboard.vue";
import UserProfile from "./components/UserProfile.vue";
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
    { path: "/userProfile", component: UserProfile },
  ],
});

// Add a global beforeEach guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");
  const isLoggedIn = !!token;

  // If the user is not logged in and tries to access a protected route, redirect to login
  if (!isLoggedIn && (to.path === "/adminDashboard" || to.path === "/customerDashboard")) {
    next("/login");
  } else {
    next();
  }
});

const app = createApp(App);
app.use(router);
app.use(createPinia());

app.mount("#app");
