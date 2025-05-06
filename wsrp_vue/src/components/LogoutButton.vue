<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter();

const logout = async () => {
    try {
        // Call backend logout to clear cookies (with credentials)
        await fetch(`${import.meta.env.VITE_API_URL}/api/auth/logout`, {
            method: 'POST',
            credentials: 'include', // important for cookies
        });
    } catch (e) {
        // Ignore errors, still clear local token
    }
    localStorage.removeItem('access_token');
    router.push('/');
    setTimeout(() => window.location.reload(), 100); // Force UI update
};

onMounted(() => {
    const logoutButton = document.getElementById('logout');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
});
</script>

<template>
    <button class="nav-link logout-btn" id="logout" type="button">Log out</button>
</template>

<style scoped>
/* Only keep white-space: nowrap for the logout button */
#logout {
    white-space: nowrap;
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
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  font: inherit;
  display: inline-block;
}

.nav-link:hover {
  color: var(--bank-gold-light);
  background: rgba(207, 181, 59, 0.1);
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