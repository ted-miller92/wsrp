<script setup>
import { ref, onMounted } from 'vue'
import {useRouter } from 'vue-router'
import LogoutButton from './LogoutButton.vue'

const router = useRouter();

onMounted(() => {

})
</script>

<template>
    <div id="menu">
        <div id="linkContainer">
            <router-link to="/adminDashboard">Dashboard</router-link>
            <router-link to="/userProfile">Profile</router-link>
            <LogoutButton />
        </div>
    </div>  
</template>

<style scoped>
#menu {
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
}
#linkContainer {
    width: 80%;
    display: flex;
    justify-content: flex-end;
    gap: 15px;
}
</style>