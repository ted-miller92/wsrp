<script setup>
import { defineProps } from 'vue'

defineProps({
    data: {
        type: Object,
        required: true,
    },  
});
</script>

<template>
    <div v-if="data.length === 0">
        <p>{{ data.length }} accounts found.</p>
    </div>
    <ul>
        <li v-for="(account, index) in data" :key="index">
            <strong>Account Number:</strong> {{ account.account_number }}<br />
            <strong>Balance:</strong> {{ account.account_balance }}<br />
        </li>
    </ul>
</template>

<style scoped>
.item {
  margin-top: 2rem;
  display: flex;
  position: relative;
}
.details {
  flex: 1;
  margin-left: 1rem;
}
input {
	display:block;
	margin: 6px 0px 6px 0px;
}
button {
	margin: 6px 12px 6px 0px;
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}
</style>

