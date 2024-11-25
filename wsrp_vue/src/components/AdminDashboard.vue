<script setup>
import { onMounted } from 'vue';
import {jwtDecode} from 'jwt-decode'
import Menu from './Menu.vue'

// parse the user_name from the current jwt token
const decodedToken = jwtDecode(localStorage.getItem('access_token'));
const user_name = decodedToken.sub;

const options = {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
		'Access-Control-Allow-Origin': '*',
		'Access-Control-Allow-Methods': '*',
		'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers',
	},
	body: JSON.stringify({
		user_name: user_name,
	}),
}
async function fetchUserProfile() {
	const userProfileResponse = await fetch('http://127.0.0.1:5000/api/users', options)
	if (userProfileResponse.ok) {
		const data = await userProfileResponse.json();
		props.first_name = data[0].first_name
	}
}
fetchUserProfile();
</script>

<template>
	<Menu />
	<div class="greetings">
		<h1 class="green">{{ msg }}</h1>
		<h3>Customer Dashboard</h3>
		<p>Hello {{ user_name }}</p>
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
