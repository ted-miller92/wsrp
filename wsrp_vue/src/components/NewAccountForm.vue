<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  userProfile: {
    type: Object,
    required: true,
  },
});

const router = useRouter();
const accountType = ref('CHECKING');
const initialBalance = ref(0);
const error = ref('');

async function createAccount(event) {
  event.preventDefault();
  
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
      'Access-Control-Allow-Methods': '*',
      'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers',
    },
    body: JSON.stringify({
      account_type: accountType.value,
      initial_balance: parseFloat(initialBalance.value),
      user_name: props.userProfile.user.user_name // ONLY included for customer dashboard
    }),
  };

  try {
    const response = await fetch('http://127.0.0.1:5000/api/accounts/create', options);
    if (response.ok) {
      const data = await response.json();
      router.push('/dashboard'); // Redirect back to dashboard
    } else {
      error.value = 'Failed to create account';
    }
  } catch (err) {
    error.value = 'Error connecting to server';
    console.error(err);
  }
}
</script>

<template>
  <div class="new-account-form">
    <div class="user-info">
      <p class="user-type">{{ props.userProfile.user.user_type }}</p>
      <p class="user-name">{{ props.userProfile.user.first_name }} {{ props.userProfile.user.last_name }}</p>
    </div>

    <form @submit="createAccount">
      <div class="form-group">
        <label for="accountType">Account Type</label>
        <select v-model="accountType" id="accountType" required>
          <option value="CHECKING">Checking</option>
          <option value="SAVINGS">Savings</option>
          <option value="INVESTMENT">Investment</option>
        </select>
      </div>

      <div class="form-group">
        <label for="initialBalance">Initial Balance</label>
        <input
          v-model="initialBalance"
          type="number"
          id="initialBalance"
          min="0"
          step="0.01"
          required
        />
      </div>

      <div v-if="error" class="error">{{ error }}</div>

      <button type="submit">Create Account</button>
    </form>
  </div>
</template>

<style scoped>
.new-account-form {
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
}

.user-info {
  margin-bottom: 2rem;
  text-align: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(207, 181, 59, 0.2);
}

.user-type {
  color: var(--bank-gold);
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}

.user-name {
  color: var(--bank-white);
  font-size: 1.3rem;
  font-weight: 500;
}

h2 {
  color: var(--bank-gold);
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  color: var(--bank-gold);
  margin-bottom: 0.5rem;
}

select, input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--bank-white);
}

button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, var(--bank-gold) 0%, var(--bank-gold-dark) 100%);
  border: none;
  border-radius: 8px;
  color: var(--bank-blue-dark);
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(207, 181, 59, 0.3);
}

.error {
  color: #ff4444;
  margin-bottom: 1rem;
  text-align: center;
}
</style>