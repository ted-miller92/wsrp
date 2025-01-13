<script setup>
import { ref, watch, onMounted } from 'vue'
import {useRouter } from 'vue-router'
// import GenericList from './GenericList.vue'

// const components = {
//     GenericList
// }

const isLoading = ref(true);
const data = ref(null);
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
        const response = await fetch('http://127.0.0.1:5000/api/transactions', options)
        if (response.ok) {
            
            data.value = await response.json();
            isLoading.value = false;
        }
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
    setTimeout(() => fetchData(), 1000);    
});

</script>

<template>
    <div class="item">
        <div class="details">
            <h3>Transactions</h3>
            <p v-if="isLoading">Loading...</p>
            <p v-else-if="!isLoading && data.length === 0">No transactions found.</p>
            <p v-else-if="!isLoading && data.length > 0">{{ data.length }} transactions found:</p>
            <ul v-if="!isLoading && data.length > 0">
                <li v-for="transaction in data" :key="transaction.transaction_id">
                    <p>Transaction ID: {{ transaction.transaction_id }}</p>
                    <p>Amount: {{ transaction.transaction_amount }}</p>
                </li>
            </ul>       
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

