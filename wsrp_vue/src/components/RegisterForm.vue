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
      router.push("/login");
    }
  }
  registerButton.addEventListener("click", register);
});
</script>

<template>
  <div class="register-container">
    <div class="register-form">
      <h3>Create Your Account</h3>
      <form>
        <div class="form-grid">
          <div class="form-column">
            <div class="form-group">
              <label for="first_name">First Name</label>
              <input v-model="first_name" type="text" placeholder="First Name" />
            </div>

            <div class="form-group">
              <label for="username">Username</label>
              <input v-model="user_name" type="text" placeholder="Username" />
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input v-model="email" type="email" placeholder="Email" />
            </div>
          </div>

          <div class="form-column">
            <div class="form-group">
              <label for="last_name">Last Name</label>
              <input v-model="last_name" type="text" placeholder="Last Name" />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input v-model="password" type="password" placeholder="Password" />
            </div>

            <div class="form-group">
              <label for="user_type">User Type</label>
              <select v-model="user_type">
                <option value="CUSTOMER">Customer</option>
                <option value="EMPLOYEE">Admin</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button id="register" type="submit">Register</button>
          <p>
            Already have an account?
            <router-link to="/login" class="login-link">Login</router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  min-height: calc(100vh - 60px);
  padding: 2rem;
  margin-top: 60px;
}

.register-form {
  width: 100%;
  max-width: 1200px;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
  margin-left: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  margin-bottom: 2rem;
  padding: 0 2rem;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

h3 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--bank-gold);
  text-align: center;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--bank-white);
  transition: all 0.3s ease;
}

input:focus, select:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--bank-gold);
}

input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23CFB53B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1rem;
  padding-right: 2.5rem;
}

button {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem 2rem;
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

label {
  font-size: 1rem;
  color: var(--bank-gold);
  font-weight: 500;
}

p {
  text-align: center;
  color: var(--bank-white);
  margin: 0;
}

.login-link {
  color: var(--bank-gold);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: var(--bank-gold-light);
}

@media (max-width: 1024px) {
  .register-container {
    justify-content: center;
  }
  
  .register-form {
    margin-left: 0;
    max-width: 800px;
  }
  
  .form-grid {
    padding: 0;
  }
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .register-form {
    padding: 1.5rem;
  }
}
</style>
