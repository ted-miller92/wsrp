<template>
  <div class="container">
    <div class="item">
      <h2 class="login-title">XSS Vulnerable Login</h2>
      <form @submit.prevent="login">
        <label for="username">Username</label>
        <input v-model="user_name" type="text" placeholder="Username" />
        <label for="password">Password</label>
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
        <p>
          Don't have an account?
          <router-link to="/register">Register</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const user_name = ref("");
const password = ref("");
const showInstructions = ref(false);

const login = async () => {
  // Console log to make sure the function is being executed
  console.log("Login function called with username:", user_name.value);

  const endpoint = "/api/xss_vuln/auth/login";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_name: user_name.value,
      password: password.value,
    }),
  };

  try {
    console.log("Sending request with payload:", user_name.value);
    const response = await fetch(`http://127.0.0.1:5000${endpoint}`, options);
    const data = await response.json();
    console.log("Server response:", data);

    // Remove any existing XSS containers first
    const existingContainers = document.querySelectorAll("#xss-container");
    existingContainers.forEach((container) => container.remove());

    // Log the user input from the response
    if (data.user_input) {
      console.log("User input from response:", data.user_input);
    }

    // Create a demonstration popup regardless of what's in the payload
    // This ensures something is shown to the user
    if (data.user_input) {
      console.log("Found user_input in response:", data.user_input);

      // Create a container for the XSS payload
      const container = document.createElement("div");
      container.id = "xss-container";
      container.style.position = "fixed";
      container.style.top = "0";
      container.style.left = "0";
      container.style.width = "100%";
      container.style.height = "100%";
      container.style.zIndex = "10000";
      container.style.display = "flex";
      container.style.justifyContent = "center";
      container.style.alignItems = "center";
      container.style.backgroundColor = "rgba(0,0,0,0.5)";
      document.body.appendChild(container);

      // Create a custom alert box
      const alertBox = document.createElement("div");
      alertBox.style.background = "white";
      alertBox.style.padding = "30px";
      alertBox.style.borderRadius = "8px";
      alertBox.style.textAlign = "center";
      alertBox.style.maxWidth = "400px";
      alertBox.style.width = "90%";
      alertBox.style.boxShadow = "0 5px 15px rgba(0,0,0,0.3)";

      // Add a title
      const title = document.createElement("h2");
      title.textContent = "XSS Vulnerability Demonstration";
      title.style.color = "red";
      title.style.marginTop = "0";
      title.style.marginBottom = "15px";
      alertBox.appendChild(title);

      // Add the message
      const message = document.createElement("p");
      message.innerHTML =
        "This is a demonstration of an XSS attack.<br><br>" +
        "In a real attack, this popup could:<br>" +
        "• Steal your cookies<br>" +
        "• Request your credentials<br>" +
        "• Redirect you to a malicious site<br><br>";
      message.style.margin = "0 0 20px 0";
      message.style.fontSize = "16px";
      message.style.textAlign = "left";
      message.style.color = "#333333";
      alertBox.appendChild(message);

      // Display the user input HTML directly
      const userInputDisplay = document.createElement("div");
      userInputDisplay.style.border = "1px solid #ddd";
      userInputDisplay.style.padding = "15px";
      userInputDisplay.style.backgroundColor = "#f9f9f9";
      userInputDisplay.style.marginBottom = "20px";
      userInputDisplay.style.borderRadius = "4px";
      userInputDisplay.style.color = "#333333";
      userInputDisplay.innerHTML = data.user_input || "No input detected";
      alertBox.appendChild(userInputDisplay);

      // Add OK button
      const okButton = document.createElement("button");
      okButton.textContent = "Close Demo";
      okButton.style.marginTop = "15px";
      okButton.style.padding = "10px 30px";
      okButton.style.background = "#007bff";
      okButton.style.color = "white";
      okButton.style.border = "none";
      okButton.style.borderRadius = "4px";
      okButton.style.cursor = "pointer";
      okButton.style.fontSize = "16px";
      okButton.style.fontWeight = "bold";
      okButton.onclick = () => {
        container.remove();
      };
      alertBox.appendChild(okButton);

      container.appendChild(alertBox);
    } else {
      console.log("No user_input found in response");
    }
  } catch (error) {
    console.error("Login failed:", error);
  }
};

const toggleInstructions = () => {
  showInstructions.value = !showInstructions.value;
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 2rem;
}

.item {
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
}

.login-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--bank-gold);
  text-align: center;
}

.instructions {
  margin-top: 1.5rem;
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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

.instructions-content code {
  display: block;
  margin: 0.5rem 0;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

input {
  display: block;
  width: 100%;
  margin: 1rem 0;
  padding: 1rem;
  font-size: 1.1rem;
  border: 1px solid var(--bank-gold);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--bank-white);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--bank-gold);
}

button {
  margin: 1.5rem 0;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(
    135deg,
    var(--bank-gold) 0%,
    var(--bank-gold-dark) 100%
  );
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 100%;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(207, 181, 59, 0.4);
  background: linear-gradient(
    135deg,
    var(--bank-gold-light) 0%,
    var(--bank-gold) 100%
  );
}
</style>
