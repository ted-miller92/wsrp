<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const user_name = ref("");
const password = ref("");
const endpoint = ref(
  router.currentRoute.value.query.endpoint || "/api/auth/login"
); // Default to secure login

onMounted(() => {
  const loginButton = document.getElementById("login");

  async function login(event) {
    event.preventDefault();

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

    const response = await fetch(
      `http://127.0.0.1:5000${endpoint.value}`,
      options
    );
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      // Handle successful login (e.g., redirect to dashboard)
    } else {
      // Handle login error
    }
  }

  loginButton.addEventListener("click", login);
});
</script>

<template>
  <div class="item">
    <div class="details">
      <h3>Login</h3>
      <form>
        <label for="username">Username</label>
        <input v-model="user_name" type="text" placeholder="Username" />
        <label for="password">Password</label>
        <input v-model="password" type="password" placeholder="password" />
        <button id="login" type="submit">Login</button>

        <p>
          Don't have an account?
          <router-link to="/register">Register</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.item {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
}

.details {
  flex: 1;
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

input::placeholder {
  color: rgba(255, 255, 255, 0.6);
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

h3 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--bank-gold);
  text-align: center;
}

.error-message {
  color: #f44336;
  font-size: 1rem;
  margin-top: 0.5rem;
  text-align: center;
}

label {
  display: block;
  font-size: 1.1rem;
  color: var(--bank-gold);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.register-link {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
  color: var(--bank-gold);
  font-size: 1rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.register-link:hover {
  color: var(--bank-gold-light);
}

@media (max-width: 768px) {
  .item {
    margin: 1rem;
    padding: 1.5rem;
  }
}
</style>
