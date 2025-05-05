<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const user_name = ref("");
const password = ref("");
const email = ref("");
const first_name = ref("");
const last_name = ref("");
const user_type = ref({
  EMPLOYEE: "EMPLOYEE",
  CUSTOMER: "CUSTOMER",
});

onMounted(() => {
  const registerButton = document.getElementById("register");

  async function register(event) {
    event.preventDefault();

    const options = {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers":
          "Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers",
      },
      body: JSON.stringify({
        user_name: user_name.value,
        password: password.value,
        email: email.value,
        first_name: first_name.value,
        last_name: last_name.value,
        user_type: user_type.value,
      }),
    };

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/auth/register`,
      options
    );
    if (response.ok) {
      const data = await response.json();
      console.log(data);

      // Get the JWT access token
      // Store it in the local storage
      // Note: Storing as a cookie is perhaps better than local storage
      // Note: It may be better in the future to store it using a state management tool like Pinia
      // localStorage.setItem("access_token", data.access_token);
      router.push("/login");
    }
  }
  registerButton.addEventListener("click", register);
});
</script>

<template>
  <div class="item">
    <div class="details">
      <h3>Register</h3>
      <form>
        <label for="username">Username</label>
        <input v-model="user_name" type="text" placeholder="Username" />

        <label for="email">Email</label>
        <input v-model="email" type="email" placeholder="Email" />

        <label for="first_name">First Name</label>
        <input v-model="first_name" type="text" placeholder="First Name" />

        <label for="last_name">Last Name</label>
        <input v-model="last_name" type="text" placeholder="Last Name" />

        <label for="user_type">User type</label>
        <select v-model="user_type">
          <option value="CUSTOMER">Customer</option>
          <option value="EMPLOYEE">Admin</option>
        </select>

        <label for="password">Password</label>
        <input v-model="password" type="password" placeholder="Password" />
        <label for="confirm-password">Confirm Password</label>
        <input
          v-model="confirm_password"
          type="password"
          placeholder="Confirm Password"
        />
        <button id="register" type="submit">Register</button>

        <p>
          Already have an account?
          <router-link to="/login" class="login-link">Login</router-link>
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

p {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--bank-white);
}

.login-link {
  color: var(--bank-gold);
  text-decoration: none;
  margin-left: 0.5rem;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: var(--bank-gold-light);
}

@media (max-width: 768px) {
  .item {
    margin: 1rem;
    padding: 1.5rem;
  }
}
</style>
