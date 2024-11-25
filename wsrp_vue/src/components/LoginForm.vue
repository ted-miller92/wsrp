<script setup>

import { ref, onMounted } from 'vue'
import {useRouter } from 'vue-router'

const router = useRouter();
const user_name = ref('');
const password = ref('');

onMounted(() => {
	const loginButton = document.getElementById('login');

	async function login(event) {
		event.preventDefault();

		const options = {
			method: 'POST',

			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
				'Access-Control-Allow-Methods': '*',
				'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers',
			},
			body: JSON.stringify({
				user_name: user_name.value,
				password: password.value,
			}),
		}

		const response = await fetch('http://127.0.0.1:5000/api/auth/login', options)
		if (response.ok) { 
			const data = await response.json();
			console.log(data);

			// Get the JWT access token
			// Store it in the local storage
			// Note: Storing as a cookie is perhaps better than local storage
			// Note: It may be better in the future to store it using a state management tool like Pinia
			localStorage.setItem('access_token', data.access_token);

			// A not very secure way to do it
			if (data.user_type == 'EMPLOYEE') {
				router.push('/adminDashboard');
			} else {
				router.push('/customerDashboard');
			}
		}
	}
	loginButton.addEventListener('click', login);
})

</script>

<template>
	<div class="item">
		<div class="details">
			<h3>Login</h3>
			<form>
				<label for="username">Username</label>
				<input 
					v-model="user_name"
					type="text" 
					placeholder="Username" />
				<label for="password">Password</label>
				<input 
					v-model="password"
					type="password" 
					placeholder="password" />
				<button id="login" type="submit">Login</button>
				
				<p>Don't have an account? <router-link to="/register">Register</router-link></p>
				
			</form>			
		</div>	
	</div>	
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

