<script setup>
import { ref, onMounted } from 'vue';
import {jwtDecode} from 'jwt-decode'
import Menu from './Menu.vue'

// parse the user_name from the current jwt token
const decodedToken = jwtDecode(localStorage.getItem('access_token'));
const user_name = decodedToken.sub;
const userProfile = ref(null);

const options = {
	method: 'GET',
	headers: {
		'Content-Type': 'application/json',
		'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
		'Access-Control-Allow-Methods': '*',
		'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers',
		'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
	},
}

const fetchUserProfile = async () => {
	try {
		const response = await fetch('http://127.0.0.1:5000/api/users?user_name=\'' + user_name + '\'', options)
		if (response.ok) {
			userProfile.value = await response.json();
			console.log('User profile:', userProfile.value); // Add logging
		} else {
			console.error('Failed to fetch profile:', response.status);
		}
	} catch (error) {
		console.error('Error fetching profile:', error);
	}
}

onMounted(async () => {
	await fetchUserProfile(); // Fetch user profile
});
</script>

<template>
	<Menu />
	<div class="greetings">
		<h3>User Profile</h3>
		<p>Hello {{ user_name }}</p>
	</div>

	<div class="item" v-if="userProfile">
		<p>User type: {{ userProfile.user.user_type }}</p>
		<p>First name: {{ userProfile.user.first_name }}</p>
		<p>Last name: {{ userProfile.user.last_name }}</p>
		<p>Email: {{ userProfile.user.email }}</p>
	</div>
	<div v-else>
		<p>Loading profile...</p>
	</div>
</template>

<style scoped>
h1 {
	font-weight: 500;
	font-size: 2.6rem;
	position: relative;
	top: -10px;
}

h3 {
	font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
	text-align: center;
}

@media (min-width: 1024px) {
	.greetings h1,
	.greetings h3 {
		text-align: left;
	}
}
</style>
