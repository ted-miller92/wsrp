<script setup>
import { ref, onMounted } from 'vue';
import {jwtDecode} from 'jwt-decode'
import TransactionList from './TransactionList.vue';
import AccountsList from './AccountsList.vue';

const props = defineProps(
	{
		userProfile: {
			type: Object,
			required: true
		}
	}
)
console.log(props.userProfile.user.user_name)

// parse the user_name from the current jwt token
const decodedToken = jwtDecode(localStorage.getItem('access_token'));
const user_name = decodedToken.sub;

// Data will be loaded into object that includes the list of transactions, response message and response code
const transactionsLoading = ref(true); // Loading state for transactions
const transactions = ref(null); // Placeholder for the fetched transactions

// Data will be loaded into object that includes the list of accounts, response message and response code
const accountsLoading = ref(true); // Loading state for accounts
const accounts = ref(null); // Placeholder for the fetched accounts

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

const fetchTransactions = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/transactions?user_name=\'' + user_name + '\'', options)
        if (response.ok) {
            transactions.value = await response.json();
            transactionsLoading.value = false;
        }
    } catch (error) {
        console.error(error);
    } finally {
		transactionsLoading.value = false; // Set loading to false after data is fetched
	}
};

const fetchAccounts = async (user_id) => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/accounts?user_id=\'' + user_id + '\'', options)
        if (response.ok) {
            accounts.value = await response.json();
            accountsLoading.value = false;
        }
    } catch (error) {
        console.error(error);
    } finally {
		accountsLoading.value = false; // Set loading to false after data is fetched
	}
};

onMounted(async () => {
	await fetchTransactions(); // Fetch transactions
	await fetchAccounts(props.userProfile.user.user_id);
});

</script>

<template>
	<div class="item">
		<p>Here are your transactions:</p>
		<TransactionList v-if="!transactionsLoading && transactions" :data="transactions.transactions" />
	</div>
	<div class="item">
		<p>Here are your accounts:</p>
		<AccountsList v-if="!accountsLoading && accounts" :data="accounts.accounts" />
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
