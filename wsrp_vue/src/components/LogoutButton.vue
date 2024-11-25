<script setup>
import { ref, onMounted } from 'vue'
import {useRouter } from 'vue-router'

const router = useRouter();

onMounted(() => {
    const logoutButton = document.getElementById('logout');
    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        router.push('/login');
    })
})
</script>

<template>
    <button id="logout">Log out</button>
</template>