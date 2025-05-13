<script setup>
import LogoutButton from "./LogoutButton.vue";
import { ref, watch, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useVulnerabilityStore } from "@/stores/vulnerabilityStore";

const router = useRouter();
const currentRoute = computed(() => router.path);
const isLoggedIn = ref(false);
const isDropdownOpen = ref(false);
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

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

// close dropdown when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.dropdown')) {
    isDropdownOpen.value = false;
  }
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

      <router-link to="/file-upload-demo" class="nav-link">File Upload</router-link>

      <LogoutButton v-if="isLoggedIn" />
    </div>
    <div class="nav-actions">
      <router-link to="/instructions" class="instructions-tab">Instructions</router-link>
      <div class="dropdown">
        <button @click="toggleDropdown" class="dropdown-button">Vulnerabilities</button>
        <div v-if="isDropdownOpen" class="toggle-container">
          <div class="toggle-item">
            <label class="toggle">
              <input type="checkbox" v-model="vulnerabilityStore.sqliVulnerable" />
              <span class="slider secure"></span>
              <span class="toggle-label">
                SQL Injection
                {{ vulnerabilityStore.sqliVulnerable ? "Vulnerable" : "Secure" }}
              </span>
            </label>
          </div>
          <div class="toggle-item">
            <label class="toggle">
              <input type="checkbox" v-model="vulnerabilityStore.csrfVulnerable" />
              <span class="slider secure"></span>
              <span class="toggle-label">
                CSRF
                {{ vulnerabilityStore.csrfVulnerable ? "Vulnerable" : "Secure" }}
              </span>
            </label>
          </div>
          <div class="toggle-item">
            <label class="toggle">
              <input type="checkbox" v-model="vulnerabilityStore.xssVulnerable" />
              <span class="slider secure"></span>
              <span class="toggle-label">
                XSS
                {{ vulnerabilityStore.xssVulnerable ? "Vulnerable" : "Secure" }}
              </span>
            </label>
          </div>
          <div class="toggle-item">
            <label class="toggle">
              <input type="checkbox" v-model="vulnerabilityStore.fileUploadVulnerable" />
              <span class="slider secure"></span>
              <span class="toggle-label">
                File Upload
                {{ vulnerabilityStore.fileUploadVulnerable ? "Vulnerable" : "Secure" }}
              </span>
            </label>
          </div>
          <div class="toggle-item">
            <label class="toggle">
              <input type="checkbox" v-model="vulnerabilityStore.idorVulnerable" />
              <span class="slider secure"></span>
              <span class="toggle-label">
                IDOR
                {{ vulnerabilityStore.idorVulnerable ? "Vulnerable" : "Secure" }}
              </span>
            </label>
          </div>
          <div class="toggle-item">
            <label class="toggle">
              <input type="checkbox" v-model="vulnerabilityStore.bruteForceVulnerable" />
              <span class="slider secure"></span>
              <span class="toggle-label">
                Brute Force
                {{ vulnerabilityStore.bruteForceVulnerable ? "Vulnerable" : "Secure" }}
              </span>
            </label>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  width: 100%;
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
  margin-left:400px;
  margin-right: auto;
  justify-content: space-between;
  gap: 2rem;
  max-width: 60%;
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

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0;
  margin-right: 2rem;
}
.dropdown {
  width: 250px;
  margin-right: 0;
}
.instructions-tab {
  margin-left: 0;
}
.dropdown:hover{
  color: var(--bank-gold-light);
  background: rgba(207, 181, 59, 0.1);
}
.dropdown-button {
  background: none;
  border: none;
  color: var(--bank-white);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.dropdown-button:hover {
  color: var(--bank-gold-light);
}

.toggle-container {
  display: flex;
  flex-direction: column;
  width: 250px;
  margin-right: 400px;
  gap: 1rem;
  position: absolute;
  top: 100%;
  right: 0;
  background: rgba(26, 35, 126, 0.9);
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1001;
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
  margin-left: 0.5rem;
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

.instructions-tab {
  background: none;
  border: none;
  color: var(--bank-white);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-left: 1rem;
}
.instructions-tab:hover {
  color: var(--bank-gold-light);
  background: rgba(207, 181, 59, 0.1);
}
</style>