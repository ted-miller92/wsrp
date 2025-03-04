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
      <button class="back-button" @click="handleBack">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h2>Create New Account</h2>
    </div>
    <NewAccountForm :userProfile="userProfile" />
  </main>
</template>

<style scoped>
.account-container {
  max-width: 500px;
  margin: 80px auto 0;
  padding: 2rem;
}

.form-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
}

.back-button {
  position: absolute;
  left: 0;
  background: none;
  border: none;
  color: var(--bank-gold);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: transform 0.2s ease;
}

.back-button:hover {
  transform: translateX(-3px);
}

h2 {
  flex: 1;
  text-align: center;
  color: var(--bank-gold);
  margin: 0;
}
</style>
