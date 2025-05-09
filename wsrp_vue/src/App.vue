<script setup>
import { onMounted } from 'vue';

onMounted(() => {
	// Ping the backend to keep it warm
	fetch(`${import.meta.env.VITE_API_URL}/api`).catch(() => {});
});
</script>

<template>
	<router-view/>
</template>