<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useVulnerabilityStore } from "@/stores/vulnerabilityStore";

const router = useRouter();
const user_name = ref("");
const password = ref("");
const showInstructions = ref(false); // Reactive variable to control dropdown visibility

// load the pinia store so we can access state variables
const vulnerabilityStore = useVulnerabilityStore();

// This component loads a set of hints/instructions based on what vulnerability is selected
const toggleInstructions = () => {
  showInstructions.value = !showInstructions.value; // Toggle the visibility of instructions
};
</script>

<template>
  <!-- Dropdown Section for Instructions -->
  <div v-if="vulnerabilityStore.getSqliVulnerable()" class="instructions">
      <button @click="toggleInstructions" class="toggle-button">
        {{ showInstructions ? "Hide Instructions" : "Instructions" }}
      </button>
      <div v-if="showInstructions" class="instructions-content">
        <h3>How to Use the SQL Vulnerable Version</h3>
        <p>
          This version of the login form is intentionally vulnerable to SQL
          injection attacks. To demonstrate this vulnerability, follow these
          steps:
        </p>
        <ol>
          <li>Enter a valid username.</li>
          <li>
            In the password field, enter a SQL injection payload, such as:
            <pre>' OR '1'='1</pre>
          </li>
          <li>Click the "Login" button.</li>
          <li>If successful, you will see a list of users in the console.</li>
        </ol>
        <p>
          Please use this version responsibly and only in a controlled
          environment. For more information, please view the project's README.md
          file.
        </p>
      </div>
  </div>
  <div v-else-if="vulnerabilityStore.getXssVulnerable()" class="instructions">
    <button @click="toggleInstructions" class="toggle-button">
        {{ showInstructions ? "Hide Instructions" : "Instructions" }}
      </button>
      <div v-if="showInstructions" class="instructions-content">
        <h3>XSS Attack Examples</h3>
        <p>
          Below are examples of XSS payloads that can be used to exploit
          vulnerabilities in web applications:
        </p>
        <ol>
          <li>
            <strong>Malicious Phishing Alert:</strong>
            <code
              >&lt;div style="padding:15px;background:#fee;border:2px solid
              #c00;border-radius:5px;font-family:Arial;"&gt;&lt;h3
              style="color:#c00;margin-top:0;"&gt;URGENT: Security
              Notice&lt;/h3&gt;&lt;p&gt;We've detected unusual activity in your
              account. Please &lt;a href="https://www.google.com"
              style="color:#c00;font-weight:bold;"&gt;click here to verify your
              identity&lt;/a&gt; and prevent your account from being
              locked.&lt;/p&gt;&lt;/div&gt;</code
            >
          </li>
        </ol>
      </div>
  </div>
</template>


<style scoped>
.instructions {
  margin-top: 1.5rem;
  width: 100%; /* Ensure it takes full width */
  background: rgba(255, 255, 255, 0.1); /* Light background for contrast */
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem; /* Add padding for better spacing */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.instructions-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--bank-gold);
  margin-bottom: 1rem;
}

.instructions-description {
  font-size: 1.1rem;
  color: var(--bank-white);
  margin-bottom: 1rem;
}

.instructions-steps {
  margin-left: 1.5rem; /* Indent the list */
  color: var(--bank-white);
}

.instructions-warning {
  margin-top: 1rem;
  font-weight: 600;
  color: var(--bank-red); /* Use a contrasting color for warnings */
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
}
</style>