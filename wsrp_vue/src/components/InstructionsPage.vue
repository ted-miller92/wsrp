<template>
  <NavBar />
  <div class="instructions-page">
    <h1>Instructions: Using the Vulnerabilities Demo</h1>
    <p>
      This page will guide you through each vulnerability demo in this application. Use the <strong>Vulnerabilities</strong> toggle in the top navigation bar to enable or disable each vulnerability. When a toggle is set to <span style="color: red; font-weight: bold;">Vulnerable</span>, the corresponding feature is intentionally insecure for demonstration purposes.
    </p>

    <section>
      <button class="expand-btn" @click="open.sqli = !open.sqli">
        <span>{{ open.sqli ? '▼' : '►' }}</span> 1. SQL Injection (SQLi)
      </button>
      <div v-if="open.sqli" class="section-content">
        <p><strong>What is it?</strong> SQL Injection allows attackers to manipulate database queries by injecting malicious SQL code into input fields.</p>
        <ol>
          <li>In the navbar, open <strong>Vulnerabilities</strong> and toggle <strong>SQL Injection</strong> to <span style="color: red;">Vulnerable</span>.</li>
          <li>Go to the <strong>Login</strong> page.</li>
          <li>In the username field, enter a payload such as <code>' OR '1'='1</code> or <code>admin' --</code>.</li>
          <li>Enter any password and click <strong>Login</strong>.</li>
          <li>If the app is vulnerable, you will be logged in or see data you shouldn't have access to.</li>
        </ol>
        <p><strong>Why is this dangerous?</strong> Attackers can bypass authentication, steal data, or even destroy the database.</p>
      </div>
    </section>

    <section>
      <button class="expand-btn" @click="open.xss = !open.xss">
        <span>{{ open.xss ? '▼' : '►' }}</span> 2. Cross-Site Scripting (XSS)
      </button>
      <div v-if="open.xss" class="section-content">
        <p><strong>What is it?</strong> XSS lets attackers inject malicious scripts into web pages viewed by others.</p>
        <ol>
          <li>Toggle <strong>XSS</strong> to <span style="color: red;">Vulnerable</span> in the navbar.</li>
          <li>Go to the <strong>Login</strong> page.</li>
          <li>In the username field, enter a payload like <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code> or <code>&lt;img src="x" onerror="alert('XSS')"&gt;</code>.</li>
          <li>Enter any password and click <strong>Login</strong>.</li>
          <li>If the app is vulnerable, a popup or alert will appear, showing the script executed.</li>
        </ol>
        <p><strong>Why is this dangerous?</strong> Attackers can steal cookies, impersonate users, or deface the site.</p>
      </div>
    </section>

    <section>
      <button class="expand-btn" @click="open.csrf = !open.csrf">
        <span>{{ open.csrf ? '▼' : '►' }}</span> 3. Cross-Site Request Forgery (CSRF)
      </button>
      <div v-if="open.csrf" class="section-content">
        <p><strong>What is it?</strong> CSRF tricks a logged-in user into submitting unwanted actions on their behalf.</p>
        <ol>
          <li>Toggle <strong>CSRF</strong> to <span style="color: red;">Vulnerable</span> in the navbar.</li>
          <li>Log in as a user and go to a form that performs an action (like transferring money).</li>
          <li>Open your browser's developer console.</li>
          <li>Paste and run a fetch request (see below) to simulate a CSRF attack:</li>
        </ol>
        <pre><code>fetch(`${import.meta.env.VITE_API_URL}/api/csrf_vuln/transfer`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ from_account: 'attacker', to_account: 'victim', amount: 100 })
});</code></pre>
        <p>If the app is vulnerable, the transfer will succeed without proper authorization.</p>
        <p><strong>Why is this dangerous?</strong> Attackers can trick users into transferring money or changing account details without their consent.</p>
      </div>
    </section>

    <section>
      <button class="expand-btn" @click="open.brute = !open.brute">
        <span>{{ open.brute ? '▼' : '►' }}</span> 4. Brute Force
      </button>
      <div v-if="open.brute" class="section-content">
        <p><strong>What is it?</strong> Brute force attacks try many username/password combinations to guess credentials.</p>
        <ol>
          <li>Toggle <strong>Brute Force</strong> to <span style="color: red;">Vulnerable</span> in the navbar (if available).</li>
          <li>Go to the <strong>Login</strong> page.</li>
          <li>Try logging in repeatedly with different passwords for the same user.</li>
          <li>If the app is vulnerable, there will be no rate limiting or lockout, and you can try unlimited attempts.</li>
        </ol>
        <p><strong>Why is this dangerous?</strong> Attackers can eventually guess weak passwords and gain unauthorized access.</p>
      </div>
    </section>

    <section>
      <button class="expand-btn" @click="open.file = !open.file">
        <span>{{ open.file ? '▼' : '►' }}</span> 5. Insecure File Upload
      </button>
      <div v-if="open.file" class="section-content">
        <p><strong>What is it?</strong> Insecure file upload allows attackers to upload malicious files to the server.</p>
        <ol>
          <li>Toggle <strong>File Upload</strong> to <span style="color: red;">Vulnerable</span> in the navbar.</li>
          <li>Go to the file upload form (if available).</li>
          <li>Try uploading a file type that should not be allowed (e.g., <code>.exe</code>, <code>.php</code>, or a script file).</li>
          <li>If the app is vulnerable, the upload will succeed without validation.</li>
        </ol>
        <p><strong>Why is this dangerous?</strong> Attackers can upload malware or scripts that compromise the server or other users.</p>
      </div>
    </section>

    <section>
      <button class="expand-btn" @click="open.idor = !open.idor">
        <span>{{ open.idor ? '▼' : '►' }}</span> 6. Insecure Direct Object Reference (IDOR)
      </button>
      <div v-if="open.idor" class="section-content">
        <p><strong>What is it?</strong> IDOR lets attackers access or modify data belonging to other users by manipulating references (like IDs) in requests.</p>
        <ol>
          <li>Toggle <strong>IDOR</strong> to <span style="color: red;">Vulnerable</span> in the navbar.</li>
          <li>Log in as a user and note your account/user ID (visible in the dashboard or profile).</li>
          <li>Use browser dev tools to modify a request (e.g., change the <code>user_id</code> or <code>account_id</code> in a URL or request body) to another user's ID.</li>
          <li>If the app is vulnerable, you will see or modify data that does not belong to you.</li>
        </ol>
        <p><strong>Why is this dangerous?</strong> Attackers can steal or change other users' data by guessing or changing IDs in requests.</p>
      </div>
    </section>

    <section>
      <button class="expand-btn" @click="open.tips = !open.tips">
        <span>{{ open.tips ? '▼' : '►' }}</span> Tips for Safe Testing
      </button>
      <div v-if="open.tips" class="section-content">
        <ul>
          <li>Only test vulnerabilities in a safe, controlled environment.</li>
          <li>Never use real or sensitive data for testing.</li>
          <li>Reset toggles to <span style="color: green; font-weight: bold;">Secure</span> when done.</li>
          <li>For more details, see the README or documentation linked in the footer.</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';
const open = ref({
  sqli: true,
  xss: false,
  csrf: false,
  brute: false,
  file: false,
  idor: false,
  tips: false,
});
</script>

<style scoped>
.instructions-page {
  max-width: 1200px;
  margin: 60px auto 0 auto;
  padding: 2.5rem 3rem;
  background: rgba(26, 35, 126, 0.4);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  color: var(--bank-white);
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
h1 {
  color: var(--bank-gold);
  margin-bottom: 1.5rem;
}
h2 {
  color: var(--bank-gold);
  margin-top: 2rem;
  margin-bottom: 1rem;
}
section {
  margin-bottom: 2rem;
}
.expand-btn {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  color: var(--bank-gold);
  font-size: 1.2rem;
  font-weight: 600;
  padding: 0.75rem 0;
  cursor: pointer;
  outline: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s;
}
.expand-btn:hover {
  color: var(--bank-gold-light);
}
.section-content {
  margin-top: 0.5rem;
  padding: 1rem 1.5rem;
  background: rgba(0,0,0,0.08);
  border-radius: 8px;
  border: 1px solid var(--bank-gold);
  color: var(--bank-white);
  animation: fadeIn 0.2s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
code, pre {
  background: rgba(0,0,0,0.2);
  border-radius: 4px;
  padding: 2px 6px;
  font-family: monospace;
  color: #ffe066;
}
pre {
  padding: 1rem;
  overflow-x: auto;
}
strong {
  color: var(--bank-gold);
}
</style> 