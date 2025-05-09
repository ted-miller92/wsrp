<script setup>
import WelcomeBanner from "./WelcomeBanner.vue";
import RegisterForm from "./RegisterForm.vue";
import NavBar from "./NavBar.vue";
</script>

<template>
  <NavBar />
  <header>
    <div class="wrapper">
      <WelcomeBanner msg="Gold Standard Bank" />
    </div>
  </header>

  <main class="register-container">
    <RegisterForm />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  margin-top: 100px; /* Increased to move WelcomeBanner further down */
  margin-bottom: 2rem;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}

.register-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
