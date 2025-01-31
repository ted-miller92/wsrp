<script setup>
import LogoutButton from "./LogoutButton.vue";
import { ref, watch, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const currentRoute = computed(() => router.path);

const isLoggedIn = ref(false);

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
</style>
