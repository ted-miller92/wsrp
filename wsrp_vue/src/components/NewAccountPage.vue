<script setup>
import Welcome from "./Welcome.vue";
import NewAccountForm from "./NewAccountForm.vue";
import NavBar from "./NavBar.vue";
import { useRoute } from 'vue-router';

const route = useRoute();
const userProfile = {
  user: {
    user_name: route.query.user_name,
    user_id: route.query.user_id
  }
};
</script>

<template>
  <NavBar />
  <header>
    <div class="wrapper">
      <Welcome msg="Gold Standard Bank" />
    </div>
  </header>

  <main class="account-container">
    <NewAccountForm :userProfile="userProfile" />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  margin-top: 60px; /* Added to accommodate navbar */
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
