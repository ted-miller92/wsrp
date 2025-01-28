<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Menu from '../components/Menu.vue';
import NavBar from '../components/NavBar.vue';

const isLoggedIn = ref(false);
const layoutKey = ref(0);

const checkIsLoggedIn = () => {
    const token = localStorage.getItem("access_token");
    isLoggedIn.value = !!token;
    layoutKey.value += 1;
};

onMounted(() => {
    checkIsLoggedIn();
    window.addEventListener('storage', checkIsLoggedIn);
});

onUnmounted(() => {
    window.removeEventListener('storage', checkIsLoggedIn);
});

watch(() => localStorage.getItem("access_token"), checkIsLoggedIn);
</script>

<template>
    <!-- <Menu /> -->
    <NavBar :isLoggedIn="isLoggedIn" :key="layoutKey" />
    <slot />
</template>