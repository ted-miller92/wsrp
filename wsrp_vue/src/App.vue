<script setup>
import Welcome from './components/Welcome.vue'
import LoginForm from './components/LoginForm.vue'
import DefaultLayout from './layouts/DefaultLayout.vue'

</script>

<template>
	<!-- <router-link to="/register">Register</router-link> -->
	<!-- <router-link to="/login">Login</router-link> -->
	<DefaultLayout>
		<router-view></router-view>
	</DefaultLayout>
	
	

</template>

