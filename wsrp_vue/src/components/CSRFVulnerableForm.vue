<template>
  <div class="container">
    <div class="item">
      <h2 class="csrf-title">Vulnerable CSRF Form</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="account">Account ID</label>
          <input v-model="account_id" type="text" placeholder="Account ID" />
        </div>
        <div>
          <label for="amount">Amount</label>
          <input v-model="amount" type="number" placeholder="Amount" />
        </div>
        <button type="submit">Transfer</button>
      </form>
    </div>

    <!-- Dropdown Section for Instructions -->
    <div class="instructions">
      <button @click="toggleInstructions" class="toggle-button">
        {{ showInstructions ? "Hide Instructions" : "How to use this version" }}
      </button>
      <div v-if="showInstructions" class="instructions-content">
        <h3>How to Use the CSRF Vulnerable Version</h3>
        <p>
          This version of the form is intentionally vulnerable to CSRF attacks.
          To demonstrate this vulnerability, follow these steps:
        </p>
        <ol>
          <li>Open the developer console in your browser.</li>
          <li>Copy the following code snippet:</li>
          <pre><code>fetch('http://127.0.0.1:5000/api/csrf_vuln/transfer', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    from_account: 'attacker_account',
    to_account: 'victim_account',
    amount: 100,
  }),
});</code></pre>
          <li>
            Modify the `from_account`, `to_account`, and `amount` as needed.
          </li>
          <li>Paste the code into the console and hit Enter.</li>
          <li>
            If successful, the transfer will be executed without the victim's
            consent.
          </li>
        </ol>
        <p>
          Please use this version responsibly and only in a controlled
          environment. For more information, please view the project's README.md
          file.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const account_id = ref("");
const amount = ref("");
const showInstructions = ref(false); // Reactive variable to control dropdown visibility

const submitForm = async () => {
  const endpoint = "/api/csrf_vuln/transfer"; // Use the CSRF vulnerable endpoint directly
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from_account: account_id.value, // Assuming this is the account to transfer from
      to_account: "victim_account", // Hardcoded for demonstration
      amount: amount.value,
    }),
  };

  const response = await fetch(`http://127.0.0.1:5000${endpoint}`, options);
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    // Handle successful transfer (e.g., notify user)
  } else {
    // Handle transfer error
  }
};

const toggleInstructions = () => {
  showInstructions.value = !showInstructions.value; // Toggle the visibility of instructions
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
  margin-top: 2rem;
}

.item {
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(255, 255, 255, 0.1); /* Match the login form background */
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
  width: 100%; /* Ensure it takes full width */
}

.csrf-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--bank-gold);
  text-align: center;
}

.instructions {
  margin-top: 1.5rem;
  width: 100%; /* Ensure it takes full width */
  background: rgba(255, 255, 255, 0.1); /* Light background for contrast */
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem; /* Add padding for better spacing */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.toggle-button {
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.toggle-button:hover {
  background: var(--bank-gold-dark);
}

.instructions-content {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  font-size: 0.7rem; /* Set a smaller font size for the dropdown text */
}

/* Add styles for the code block */
.instructions-content pre {
  white-space: pre-wrap; /* Allows the text to wrap */
  word-wrap: break-word; /* Breaks long words */
  overflow: auto; /* Adds a scrollbar if necessary */
}

form div {
  margin-bottom: 1rem; /* Add space between each title and entry box */
}

label {
  margin-bottom: 0.5rem; /* Add space between the label and the input field */
  margin-right: 1rem; /* Add space to the right of each label */
}
</style>
