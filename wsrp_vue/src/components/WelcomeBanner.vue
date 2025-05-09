<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>An Insecure Banking App</h3>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 600;
  font-size: 3rem;
  background: linear-gradient(
    135deg,
    var(--bank-gold-light) 0%,
    var(--bank-gold-dark) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 10px rgba(207, 181, 59, 0.3);
  margin-bottom: 0.5rem;
  white-space: nowrap;
}

h3 {
  font-size: 1.5rem;
  color: var(--bank-white);
  opacity: 0.9;
  font-weight: 400;
  animation: slideIn 1s ease-out 0.5s both;
  white-space: nowrap;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.greetings {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-left: 2rem;
}

.greetings h1,
.greetings h3 {
  text-align: left;
  margin: 0;
}
</style>
