<script setup>
import { onMounted } from 'vue';
import {jwtDecode} from 'jwt-decode'
import Menu from './Menu.vue'
import TransactionList from './TransactionList.vue';

// parse the user_name from the current jwt token
const decodedToken = jwtDecode(localStorage.getItem('access_token'));
const user_name = decodedToken.sub;
</script>

<template>
	<Menu />
	<div class="greetings">
		<h1 class="green">{{ msg }}</h1>
		<h3>Admin Dashboard</h3>
		<p>Hello {{ user_name }}</p>
	</div>

	<div class="item">
		<TransactionList />
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
