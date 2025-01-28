<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from "vue";
import { useRoute } from "vue-router";
import LogoutButton from "./LogoutButton.vue";

defineProps({
  isLoggedIn: {
    type: Boolean,
    required: true,
  },
}
)

const route = useRoute();
const currentRoute = computed(() => route.path);
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
        to="/login"
        class="nav-link"
        :class="{ active: currentRoute === '/login' }"
      >
        Login
      </router-link>
      <router-link
        to="/register"
        class="nav-link"
        :class="{ active: currentRoute === '/register' }"
      >
        Register
      </router-link>
      <div v-if="isLoggedIn">
        <LogoutButton />
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
</style>
