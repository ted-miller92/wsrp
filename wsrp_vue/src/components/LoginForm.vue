<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useVulnerabilityStore } from "@/stores/vulnerabilityStore";

const router = useRouter();
const user_name = ref("");
const password = ref("");
const responseContainerVisible = ref(false);
const requestText = ref("");
const responseText = ref("");
const loginError = ref(false);

// load the pinia store so we can access state variables
const vulnerabilityStore = useVulnerabilityStore();

// Default route to secure login
const endpoint = ref(
  router.currentRoute.value.query.endpoint || "/api/auth/login"
);

// close response container when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.response-container')) {
    responseContainerVisible.value = false;
  }
});

onMounted(() => {  
  const loginButton = document.getElementById("login");

  const login = async (event) => {
    event.preventDefault();

    // check store value for sqli vulnerability
    if (vulnerabilityStore.getSqliVulnerable() === true) {
      endpoint.value = "/api/sqli_vuln/auth/login";
    } else {
      endpoint.value = "/api/auth/login";
    }

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

    requestText.value = options.body;

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}${endpoint.value}`,
      options
    );
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      // Store the access token in local storage
      localStorage.setItem("access_token", data.access_token);
      // Redirect to the Customer Dashboard
      router.push("/dashboard");
    } else {
      // Handle login error
      console.error("Login failed");
      // show login error in the form
      loginError.value = true;
      const responseData = await response.json();
      responseText.value = JSON.stringify(responseData);
      responseContainerVisible.value = true;
    }
  };

  loginButton.addEventListener("click", login);
});
</script>

<template>
  <div class="item">
    <div class="details">
      <h2 class="login-title">Login</h2>
      <form>
        <label for="username">Username</label>
        <input v-model="user_name" type="text" placeholder="Username" />
        <label for="password">Password</label>
        <input v-model="password" type="password" placeholder="Password" />
        <p v-if="loginError" class="login-error">Login failed. Please try again.</p>
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
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
  margin-top: 2rem;
}

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

.login-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--bank-gold);
  text-align: center;
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

.response-container{
  position: absolute;
  z-index: 1000;
  bottom: 10%;
  left: 35%;
  transform: translateX(-50%);
  background-color: #000;
  padding: 1rem;
  padding-top: 0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 650px;
  max-width: 800px;
}
.response-container-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
button#close-response{
  top: 10px;
  right: 10px;
  background: linear-gradient( 135deg, var(--bank-gold) 0%, var(--bank-gold-dark) 100% );;
  border: none;
  color: #fff;
  cursor: pointer;
  width:fit-content;
  transition: color 0.3s ease;
}
.response-container h3{
  color: #fff;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}
.response-container h4{
  color: #fff;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}
.response-container pre{
  text-wrap: wrap;
  white-space: pre-line;
  word-wrap: break-word;
}

.login-error{
  color: red;
}
</style>
