<script setup>
import NewAccountForm from "./NewAccountForm.vue";
import NavBar from "./NavBar.vue";
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const userProfile = {
  user: {
    user_name: route.query.user_name,
    user_id: route.query.user_id
  }
};

const handleBack = () => {
  router.push('/dashboard');
};
</script>

<template>
  <NavBar />
  <main class="account-container">
    <div class="form-header">
      <h2>Create New Account</h2>
    </div>
    <NewAccountForm :userProfile="userProfile" />
    <div class="button-container">
      <button class="back-button" @click="handleBack">
        Back to Dashboard
      </button>
    </div>
  </main>
</template>

<style scoped>
.account-container {
  max-width: 800px;
  margin: 80px auto 0;
  padding: 2rem;
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.button-container {
  margin-top: 2rem;
  text-align: center;
}

.back-button {
  background: none;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  color: var(--bank-gold);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.75rem 1.5rem;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: rgba(207, 181, 59, 0.1);
  color: var(--bank-gold-light);
  transform: translateY(-2px);
}

h2 {
  color: var(--bank-gold);
  margin: 0;
  font-size: 1.8rem;
}
</style>