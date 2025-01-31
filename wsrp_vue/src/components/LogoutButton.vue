<script setup>
import { onMounted } from 'vue'
import {useRouter } from 'vue-router'

const router = useRouter();

onMounted(() => {
    const logoutButton = document.getElementById('logout');
    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        router.push('/');
    })
})
</script>

<template>
    <a class="nav-link" id="logout">Log out</a>
</template>

<style scoped>
#logout{
    color: var(--bank-gold-light);
}
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