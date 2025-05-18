<script setup>
import { ref, onMounted, computed } from "vue";
import AccountsList from "./AccountsList.vue";
import { useRouter } from 'vue-router';

const props = defineProps({
  userProfile: {
    type: Object,
    required: true,
  },
});
console.log(props.userProfile.user.user_name);

// Data will be loaded into object that includes the list of transactions, response message and response code
const transactionsLoading = ref(true); // Loading state for transactions
const transactions = ref(null); // Placeholder for the fetched transactions

// Data will be loaded into object that includes the list of accounts, response message and response code
const accountsLoading = ref(true); // Loading state for accounts
const accounts = ref(null); // Placeholder for the fetched accounts

const router = useRouter();

const options = {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers":
      "Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers",
    Authorization: "Bearer " + localStorage.getItem("access_token"),
  },
};

const fetchTransactions = async () => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/transactions?user_name=${props.userProfile.user.user_name}`,
      options
    );
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
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/accounts?user_id=${user_id}`,
      options
    );
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

const handleNewAccount = () => {
  router.push({ 
    path: '/new-account',
    query: { 
      user_name: props.userProfile.user.user_name,
      user_id: props.userProfile.user.user_id
    }
  });
};


onMounted(async () => {
  await fetchTransactions(); // Fetch transactions
  await fetchAccounts(props.userProfile.user.user_id);
  const newAccountButton = document.querySelector('.action-button[data-action="new-account"]');
  if (newAccountButton) {
    newAccountButton.addEventListener('click', handleNewAccount);
  }
});

// Add new computed properties for summary data
const totalBalance = computed(() => {
  if (!accounts.value?.accounts) return 0;
  return accounts.value.accounts.reduce(
    (sum, account) => sum + parseFloat(account.account_balance),
    0
  );
});

const recentTransactions = computed(() => {
  if (!transactions.value?.transactions) return [];
  return transactions.value.transactions.slice(0, 5); // Get last 5 transactions
});
</script>

<template>
  <div class="dashboard-wrapper">
    <nav class="side-nav">
      <div class="nav-profile">
        <div class="profile-icon">
          {{ props.userProfile.user.first_name[0]
          }}{{ props.userProfile.user.last_name[0] }}
        </div>
        <div class="profile-info">
          <h3>
            {{ props.userProfile.user.first_name }}
            {{ props.userProfile.user.last_name }}
          </h3>
          <p>{{ props.userProfile.user.user_type }}</p>
        </div>
      </div>
      <div class="nav-links">
        <a href="#" class="nav-link active"
          ><i class="fas fa-home"></i> Dashboard</a
        >
        <a href="#" class="nav-link"
          ><i class="fas fa-exchange-alt"></i> Transfers</a
        >
        <a href="#" class="nav-link"
          ><i class="fas fa-file-invoice-dollar"></i> Bills</a
        >
        <a href="#" class="nav-link"
          ><i class="fas fa-piggy-bank"></i> Savings</a
        >
        <a href="#" class="nav-link"
          ><i class="fas fa-chart-line"></i> Investments</a
        >
      </div>
    </nav>

    <main class="main-content">
      <header class="dashboard-header">
        <div class="welcome-card">
          <div class="welcome-text">
            <h1>Welcome back, {{ props.userProfile.user.first_name }}!</h1>
            <p class="subtitle">Here's your financial overview</p>
          </div>
          <div class="total-balance">
            <span class="balance-label">Total Balance</span>
            <span class="balance-amount"
              >${{ totalBalance.toLocaleString() }}</span
            >
          </div>
        </div>

        <div class="quick-actions">
          <button class="action-button">
            <i class="fas fa-exchange-alt"></i> Transfer
          </button>
          <button class="action-button">
            <i class="fas fa-paper-plane"></i> Pay Bills
          </button>
          <button class="action-button" data-action="new-account" @click="handleNewAccount">
            <i class="fas fa-plus"></i> New Account
          </button>
          <button class="action-button">
            <i class="fas fa-history"></i> History
          </button>
        </div>
      </header>

      <div class="dashboard-grid">
        <div class="dashboard-card accounts-summary">
          <div class="card-header">
            <h2>Accounts</h2>
            <button class="text-button">View All</button>
          </div>
          <div class="card-content">
            <AccountsList
              v-if="!accountsLoading && accounts"
              :data="accounts.accounts"
            />
            <div v-else class="loading-state">Loading accounts...</div>
          </div>
        </div>

        <div class="dashboard-card recent-transactions">
          <div class="card-header">
            <h2>Recent Transactions</h2>
            <button class="text-button">View All</button>
          </div>
          <div class="card-content">
            <div
              v-if="!transactionsLoading && transactions"
              class="transaction-list"
            >
              <div
                v-for="tx in recentTransactions"
                :key="tx.transaction_id"
                class="transaction-item"
              >
                <div class="transaction-icon">
                  <i
                    :class="
                      tx.amount > 0 ? 'fas fa-arrow-down' : 'fas fa-arrow-up'
                    "
                  ></i>
                </div>
                <div class="transaction-info">
                  <span class="transaction-type">{{
                    tx.transaction_type
                  }}</span>
                  <span class="transaction-date">{{
                    new Date(tx.transaction_date).toLocaleDateString()
                  }}</span>
                </div>
                <span
                  class="transaction-amount"
                  :class="{ 'amount-negative': tx.amount < 0 }"
                >
                  ${{ Math.abs(tx.amount).toLocaleString() }}
                </span>
              </div>
            </div>
            <div v-else class="loading-state">Loading transactions...</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background: var(--bank-blue-dark);
  padding-top: 60px;
}

.side-nav {
  width: 200px;
  background: rgba(26, 35, 126, 0.6);
  backdrop-filter: blur(10px);
  padding: 2rem 1rem;
  border-right: 1px solid var(--bank-gold);
  flex-shrink: 0;
}

.nav-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(207, 181, 59, 0.2);
  width: 100%;
}

.profile-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(
    135deg,
    var(--bank-gold) 0%,
    var(--bank-gold-dark) 100%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.4rem;
  color: var(--bank-blue-dark);
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.profile-info {
  text-align: center;
  width: 100%;
}

.profile-info h3 {
  color: var(--bank-gold);
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  white-space: normal;
  overflow: visible;
  word-break: break-word;
  line-height: 1.3;
}

.profile-info p {
  color: var(--bank-white);
  opacity: 0.7;
  font-size: 1rem;
  white-space: normal;
  overflow: visible;
  word-break: break-word;
  line-height: 1.3;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--bank-white);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(207, 181, 59, 0.1);
  color: var(--bank-gold);
}

.main-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  width: calc(100% - 200px);
}

.dashboard-header {
  margin-bottom: 2rem;
}

.welcome-card {
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  width: 100%;
}

.welcome-text h1 {
  color: var(--bank-gold);
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.balance-amount {
  font-size: 2rem;
  color: var(--bank-gold);
  font-weight: 600;
}

.quick-actions {
  display: flex;
  gap: 1rem;
}

.action-button {
  flex: 1;
  padding: 1rem;
  background: rgba(26, 35, 126, 0.4);
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  color: var(--bank-white);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-button:hover {
  background: rgba(207, 181, 59, 0.1);
  transform: translateY(-2px);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(400px, 1fr) minmax(400px, 1fr);
  gap: 2rem;
  width: 100%;
}

.dashboard-card {
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h2 {
  color: var(--bank-gold);
  font-size: 1.2rem;
}

.text-button {
  background: none;
  border: none;
  color: var(--bank-gold);
  cursor: pointer;
  font-size: 0.9rem;
}

.transaction-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.transaction-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.transaction-icon {
  width: 40px;
  height: 40px;
  background: rgba(207, 181, 59, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bank-gold);
}

.loading-state {
  text-align: center;
  color: var(--bank-white);
  opacity: 0.7;
  padding: 2rem;
}

@media (max-width: 1024px) {
  .main-content {
    width: 100%;
    padding: 1rem;
  }

  .side-nav {
    width: 100%;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    flex-wrap: wrap;
  }

  .action-button {
    flex: 1 1 calc(50% - 0.5rem);
  }
}
</style>
