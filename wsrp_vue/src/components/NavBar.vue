<script setup>
import LogoutButton from "./LogoutButton.vue";
import { ref, watch, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useVulnerabilityStore } from "@/stores/vulnerabilityStore";

const router = useRouter();
const currentRoute = computed(() => router.path);

const isLoggedIn = ref(false);

// load the pinia store so we can access state variables
const vulnerabilityStore = useVulnerabilityStore();

watch(
    () => localStorage.getItem("access_token"),
    () => {
        updateLoggedIn();
    }
);
const updateLoggedIn = () => {
    isLoggedIn.value = !!localStorage.getItem("access_token");
};

onMounted(() => {
    updateLoggedIn();

});

</script>

<template>
  <nav class="nav-bar">
    <div class="nav-links">
      <router-link
        to="/"
        class="nav-link"
        :class="{ active: currentRoute === '/' }"
      >
        Home
      </router-link>
      <router-link
        v-if="!isLoggedIn"
        to="/login"
        class="nav-link"
        :class="{ active: currentRoute === '/login' }"
      >
        Login
      </router-link>
      <router-link
        v-if="!isLoggedIn"
        to="/register"
        class="nav-link"
        :class="{ active: currentRoute === '/register' }"
      >
        Register
      </router-link>
      <router-link
        v-if="isLoggedIn"
        to="/userProfile"
        class="nav-link"
        :class="{ active: currentRoute === '/userProfile' }"
      >
        Profile
      </router-link>

      <router-link
        v-if="isLoggedIn"
        to="/dashboard"
        class="nav-link"
        :class="{ active: currentRoute === '/dashboard' }"
      >
       Dashboard
      </router-link>
      
      <LogoutButton v-if="isLoggedIn"/>
    </div>
    <div class="toggle-container">
      <div class="toggle-item">
        <label class="toggle">
          <span class="toggle-label">SQL Injection {{ vulnerabilityStore.sqliVulnerable ? 'Vulnerable' : 'Secure'  }} </span>
          <input type="checkbox" v-model="vulnerabilityStore.sqliVulnerable" />
          <span class="slider secure"></span>
        </label>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--bank-gold);
  padding: 1rem;
  z-index: 1000;
}

.nav-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-link {
  color: var(--bank-white);
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: var(--bank-gold-light);
}

.nav-link.active {
  color: var(--bank-gold);
  background: rgba(207, 181, 59, 0.1);
}

@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
  }

  .nav-link {
    font-size: 1rem;
    padding: 0.4rem 0.8rem;
  }
}

/* Vulnerability Section Styles */
.vulnerability-section {
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid var(--bank-gold);
}

.vulnerability-section h3 {
  color: var(--bank-gold);
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 1rem;
  text-align: center;
}

.toggle-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
}

.toggle-item {
  display: flex;
  align-items: center;
}

.toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.toggle-label {
  margin-right: 0.5rem;
  color: var(--bank-white);
  font-size: 0.9rem;
}

/* Toggle Switch Styling */
.toggle input {
  display: none;
}

.slider {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: var(--bank-white);
  border-radius: 50%;
  transition: all 0.3s ease;
}

/* Default Secure Version Toggle Style */
.slider.secure {
  background-color: #4caf50;
}

.toggle input:checked + .slider {
  background-color: red;
}

.toggle input:checked + .slider:before {
  transform: translateX(20px);
}

/* Hover effects */
.toggle:hover .slider {
  box-shadow: 0 0 8px var(--bank-gold);
}

.toggle:hover .slider.secure {
  box-shadow: 0 0 8px #4caf50;
}

.toggle:hover .toggle-label {
  color: var(--bank-gold-light);
}
</style>
