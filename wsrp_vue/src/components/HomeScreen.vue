<script setup>
import Welcome from "./Welcome.vue";
import MarketDashboard from "./MarketDashboard.vue";
import NavBar from "./NavBar.vue";
import { ref, watch, onMounted } from "vue";
import { useRouter } from "vue-router";

const isVulnerable = ref(false);
const isCSRFEnabled = ref(false);
const router = useRouter();

const navigateToLogin = () => {
  const endpoint = isVulnerable.value
    ? "/api/sqli_vuln/auth/login"
    : isCSRFEnabled.value
      ? "/api/csrf_vuln/transfer"
      : "/api/auth/login";
  router.push({ path: "/login", query: { endpoint } });
};

// Watch for changes in the isVulnerable and isCSRFEnabled states
watch([isVulnerable, isCSRFEnabled], ([newVulnerable, newCSRF]) => {
  console.log(
    `Vulnerability toggle is now: ${newVulnerable ? "SQL Injection Vulnerable" : "Secure"
    }`
  );
  console.log(`CSRF toggle is now: ${newCSRF ? "CSRF Vulnerable" : "Secure"}`);
  navigateToLogin(); // Call navigateToLogin whenever the toggle changes
});
</script>

<template>
  <div class="home-layout">
    <NavBar />
    <MarketDashboard />

    <div class="main-content">
      <header>
        <div class="header-container">
          <Welcome msg="Gold Standard Bank" />
        </div>

        <!-- Button moved below the headers, keeping spacing consistent -->
        <div class="login-button-container">
          <router-link to="/login" class="login-button">Go to Login</router-link>
        </div>
      </header>


      <footer class="dev-team">
        <div class="vulnerability-section">
          <h3>Vulnerability Versions</h3>
          <div class="toggle-container">
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" v-model="isVulnerable" />
                <span class="slider secure"></span>
                <span class="toggle-label">Default Secure Version</span>
              </label>
            </div>
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" v-model="isVulnerable" />
                <span class="slider"></span>
                <span class="toggle-label">SQL Injection</span>
              </label>
            </div>
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" v-model="isCSRFEnabled" />
                <span class="slider"></span>
                <span class="toggle-label">CSRF</span>
              </label>
            </div>
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" />
                <span class="slider"></span>
                <span class="toggle-label">XSS</span>
              </label>
            </div>
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" />
                <span class="slider"></span>
                <span class="toggle-label">File Upload Vulnerable</span>
              </label>
            </div>
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" />
                <span class="slider"></span>
                <span class="toggle-label">IDOR</span>
              </label>
            </div>
          </div>
        </div>

        <div class="footer-content">
          <div class="team-section">
            <h3>Development Team</h3>
            <div class="team-members">
              <a href="https://github.com/ted-miller92" target="_blank" class="member">Ted Miller</a>
              <a href="https://github.com/SDL101" target="_blank" class="member">Scott Lindsay</a>
              <a href="https://github.com/acoalson" target="_blank" class="member">Aria Coalson</a>
              <a href="https://github.com/CyberSully" target="_blank" class="member">Brett Sullivan</a>
              <a href="https://github.com/ted-miller92/wsrp" target="_blank" class="github-link">
                View Project on GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.home-layout {
  position: relative;
  min-height: 100vh;
  padding-top: 100px;
  /* Increased from 80px to add more space */
}

.main-content {
  margin-left: 340px;
  padding: 2rem;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  white-space: nowrap;
  /* Prevent text wrapping */
}

.login-button-container {
  display: flex;
  justify-content: left; /* Aligns button with headers */
  margin-top: 2rem; /* Keep vertical spacing the same */
}



.login-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: linear-gradient(135deg,
      var(--bank-gold) 0%,
      var(--bank-gold-dark) 100%);
  color: var(--bank-blue-dark);
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(207, 181, 59, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
  /* Prevent text wrapping */
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(207, 181, 59, 0.4);
  background: linear-gradient(135deg,
      var(--bank-gold-light) 0%,
      var(--bank-gold) 100%);
}

.github-link-container {
  text-align: center;
}

.github-link {
  color: var(--bank-gold);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  padding-bottom: 2px;
}

.github-link::after {
  content: "";
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 0;
  background: linear-gradient(90deg,
      var(--bank-gold) 0%,
      var(--bank-gold-light) 100%);
  transition: width 0.3s ease;
}

.github-link:hover::after {
  width: 100%;
}

.dev-team {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(26, 35, 126, 0.9);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--bank-gold);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.2);
  padding: 1rem;
  text-align: center;
}

.dev-team h3 {
  color: var(--bank-gold);
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 1rem;
}

.team-members {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.member {
  color: var(--bank-white);
  font-weight: 500;
  transition: color 0.3s ease;
}

.member:hover {
  color: var(--bank-gold-light);
}

/* Add animation for the welcome message */
.wrapper {
  animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    padding: 1rem;
  }

  .header-container {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .login-button-container {
    margin-left: 0;
  }

  /* Allow text wrapping on very small screens if needed */
  .header-container,
  .login-button {
    white-space: normal;
  }
}

/* Vulnerability Section Styles */
.vulnerability-section {
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid var(--bank-gold);
}

.vulnerability-section h3 {
  color: var(--bank-gold);
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 1rem;
  text-align: center;
}

.toggle-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
}

.toggle-item {
  display: flex;
  align-items: center;
}

.toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.toggle-label {
  margin-left: 0.5rem;
  color: var(--bank-white);
  font-size: 0.9rem;
}

/* Toggle Switch Styling */
.toggle input {
  display: none;
}

.slider {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: var(--bank-white);
  border-radius: 50%;
  transition: all 0.3s ease;
}

/* Default Secure Version Toggle Style */
.slider.secure {
  background-color: #4caf50;
}

.toggle input:checked+.slider {
  background-color: var(--bank-gold);
}

.toggle input:checked+.slider:before {
  transform: translateX(20px);
}

/* Hover effects */
.toggle:hover .slider {
  box-shadow: 0 0 8px var(--bank-gold);
}

.toggle:hover .slider.secure {
  box-shadow: 0 0 8px #4caf50;
}

.toggle:hover .toggle-label {
  color: var(--bank-gold-light);
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.team-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
  width: 100%;
}

.team-members {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.dev-team h3 {
  font-size: 0.9rem;
  margin-bottom: 0;
  white-space: nowrap;
}

.member,
.github-link {
  font-size: 0.9rem;
  white-space: nowrap;
}

.github-link {
  margin-left: auto;
}

/* Add margin to the MarketDashboard component */
:deep(.market-dashboard) {
  margin-top: 20px;
}
</style>
