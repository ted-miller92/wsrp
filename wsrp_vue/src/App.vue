<script setup>
import { onMounted } from 'vue';
import NavBar from './components/NavBar.vue';

onMounted(() => {
	// Ping the backend to keep it warm
	fetch(`${import.meta.env.VITE_API_URL}/api`).catch(() => {});
});
</script>

<template>
	<NavBar />
	<router-view/>
</template>