<script setup>
import { ref, onMounted } from 'vue';
import {jwtDecode} from 'jwt-decode'
import Menu from './Menu.vue'
import TransactionList from './TransactionList.vue';

// parse the user_name from the current jwt token
const decodedToken = jwtDecode(localStorage.getItem('access_token'));
const user_name = decodedToken.sub;

const isLoading = ref(true); // Loading state
const data = ref(null); // Placeholder for the fetched data

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

const fetchData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/transactions?user_name=\'' + user_name + '\'', options)
        if (response.ok) {
            
            data.value = await response.json();
            isLoading.value = false;
        }
    } catch (error) {
        console.error(error);
    } finally {
		isLoading.value = false; // Set loading to false after data is fetched
	}
};

onMounted(() => {
    setTimeout(() => fetchData(), 1000);    
});

onMounted(fetchData);

</script>

<template>
	<Menu />
	<div class="greetings">
		<h3>Admin Dashboard</h3>
		<p>Hello {{ user_name }}</p>
	</div>

	<div class="item">
		<p>Here are your transactions:</p>
		<TransactionList v-if="!isLoading && data" :data="data" />
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
