<template>
  <div class="container">
    <div class="item">
      <h2 class="login-title">Vulnerable Login</h2>
      <form @submit.prevent="login">
        <label for="username">Username</label>
        <input v-model="user_name" type="text" placeholder="Username" />
        <label for="password">Password</label>
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>

    <!-- Dropdown Section for Instructions -->
    <div class="instructions">
      <button @click="toggleInstructions" class="toggle-button">
        {{ showInstructions ? "Hide Instructions" : "How to use this version" }}
      </button>
      <div v-if="showInstructions" class="instructions-content">
        <h3>How to Use the SQL Vulnerable Version</h3>
        <p>
          This version of the login form is intentionally vulnerable to SQL
          injection attacks. To demonstrate this vulnerability, follow these
          steps:
        </p>
        <ol>
          <li>Enter a valid username.</li>
          <li>
            In the password field, enter a SQL injection payload, such as
            <code>' OR '1'='1'</code>.
          </li>
          <li>Click the "Login" button.</li>
          <li>If successful, you will see a list of users in the console.</li>
        </ol>
        <p>
          Please use this version responsibly and only in a controlled
          environment. For more information, please view the project's README.md
          file.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const user_name = ref("");
const password = ref("");
const showInstructions = ref(false); // Reactive variable to control dropdown visibility

const login = async () => {
  const endpoint = "/api/sqli_vuln/auth/login"; // Use the vulnerable endpoint directly
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_name: user_name.value,
      password: password.value,
    }),
  };

  const response = await fetch(`http://127.0.0.1:5000${endpoint}`, options);
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    // Handle successful login (e.g., redirect to dashboard)
  } else {
    // Handle login error
  }
};

const toggleInstructions = () => {
  showInstructions.value = !showInstructions.value; // Toggle the visibility of instructions
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
  margin-top: 2rem;
}

.item {
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
  width: 100%; /* Ensure it takes full width */
}

.login-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--bank-gold);
  text-align: center;
}

.instructions {
  margin-top: 1.5rem;
  width: 100%; /* Ensure it takes full width */
  background: rgba(255, 255, 255, 0.1); /* Light background for contrast */
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem; /* Add padding for better spacing */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.instructions-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--bank-gold);
  margin-bottom: 1rem;
}

.instructions-description {
  font-size: 1.1rem;
  color: var(--bank-white);
  margin-bottom: 1rem;
}

.instructions-steps {
  margin-left: 1.5rem; /* Indent the list */
  color: var(--bank-white);
}

.instructions-warning {
  margin-top: 1rem;
  font-weight: 600;
  color: var(--bank-red); /* Use a contrasting color for warnings */
}

.toggle-button {
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.toggle-button:hover {
  background: var(--bank-gold-dark);
}

.instructions-content {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
}

input {
  display: block;
  width: 100%;
  margin: 1rem 0;
  padding: 1rem;
  font-size: 1.1rem;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--bank-white);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--bank-gold);
}

button {
  margin: 1.5rem 0;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(
    135deg,
    var(--bank-gold) 0%,
    var(--bank-gold-dark) 100%
  );
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 100%;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(207, 181, 59, 0.4);
  background: linear-gradient(
    135deg,
    var(--bank-gold-light) 0%,
    var(--bank-gold) 100%
  );
}
</style>
