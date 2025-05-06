<script setup>
import Welcome from "./Welcome.vue";
import MarketDashboard from "./MarketDashboard.vue";
import NavBar from "./NavBar.vue";
import { ref, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import ChatBot from "./ChatBot.vue";

const router = useRouter();

const navigateToLogin = () => {
  router.push({ path: "/login" });
};
</script>

<template>
  <NavBar />
  <div class="wrapper">

    <div class="page-container">
      <Welcome msg="Gold Standard Bank" />

      <main>
        <div class="home-container">
          <div class="content">
            <h2>Welcome to Gold Standard Bank</h2>
            <p>
              This is a demonstration banking application designed to showcase
              various web security vulnerabilities and their mitigations.
            </p>
            <p>
              Please note that this is a research project and should not be used
              for actual banking purposes.
            </p>
          </div>
          <MarketDashboard />
        </div>
      </main>
    </div>
    <footer class="footer">
      <div class="footer-content">
        <a
          href="https://github.com/ted-miller92/wsrp"
          target="_blank"
          class="github-button"
        >
          GitHub Repo
        </a>
        <div class="team">
          Development Team:
          <a href="https://github.com/ted-miller92" target="_blank"
            >Ted Miller
          </a>
          <a href="https://github.com/SDL101" target="_blank">Scott Lindsay </a>
          <a href="https://github.com/acoalson" target="_blank"
            >Aria Coalson
          </a>
          <a href="https://github.com/CyberSully" target="_blank"
            >Brett Sullivan
          </a>
        </div>
      </div>
    </footer>
  </div>
  <ChatBot />
</template>

<style scoped>
.wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.page-container {
  margin-top: 60px;
  padding-top: 2rem;
  flex: 1;
}

.home-container {
  display: flex;
  justify-content: space-between;
  padding: 2rem;
}

.content {
  flex: 1;
  max-width: 800px;
  margin-right: 2rem;
}

h2 {
  color: var(--bank-gold);
  margin-bottom: 1rem;
}

p {
  color: var(--bank-white);
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-size: 1.25rem;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(26, 35, 126, 0.4);
  border-top: 1px solid var(--bank-gold);
  padding: 1rem 0;
  text-align: center;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
}

.github-button {
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.github-button:hover {
  background: var(--bank-gold-light);
  transform: translateY(-2px);
}

.team {
  color: var(--bank-white);
  font-size: 1.1rem;
}

.team a {
  color: var(--bank-gold);
  text-decoration: none;
  transition: color 0.3s ease;
}

.team a:hover {
  color: var(--bank-gold-light);
}
</style>
