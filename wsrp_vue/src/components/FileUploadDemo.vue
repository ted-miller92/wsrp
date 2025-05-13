<script setup>
import { ref, computed } from 'vue';
import { useVulnerabilityStore } from '@/stores/vulnerabilityStore';

const vulnerabilityStore = useVulnerabilityStore();
const selectedFile = ref(null);
const uploadResult = ref('');
const uploading = ref(false);

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  uploadResult.value = '';
};

const uploadFile = async () => {
  if (!selectedFile.value) {
    uploadResult.value = 'Please select a file.';
    return;
  }
  uploading.value = true;
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  const endpoint = vulnerabilityStore.fileUploadVulnerable
    ? '/api/vuln/upload'
    : '/api/upload';
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}${endpoint}`, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    uploadResult.value = data.message || 'Upload complete.';
  } catch (err) {
    uploadResult.value = 'Error uploading file.';
  } finally {
    uploading.value = false;
  }
};

const isVulnerable = computed(() => vulnerabilityStore.fileUploadVulnerable);
const modeLabel = computed(() => isVulnerable.value ? 'VULNERABLE' : 'SECURE');
const modeColor = computed(() => isVulnerable.value ? '#ff4d4f' : '#4caf50');
const allowedFiles = computed(() =>
  isVulnerable.value
    ? 'Any file type (including .exe, .php, .js, etc.)'
    : 'Only images (.png, .jpg, .jpeg, .gif)'
);
const instructions = computed(() =>
  isVulnerable.value
    ? 'In VULNERABLE mode, you can upload any file type. This simulates an insecure file upload vulnerability.'
    : 'In SECURE mode, only safe image files are allowed. This simulates a secure file upload implementation.'
);

const phpSample = '<?php\necho \'This is a test PHP file.\';\n?>';
function copyPhpSample() {
  navigator.clipboard.writeText(phpSample);
}
</script>

<template>
  <div class="upload-demo-container">
    <h2>File Upload</h2>
    <div class="mode-indicator" :style="{ background: modeColor }">
      <strong>{{ modeLabel }}</strong>
    </div>
    <p class="instructions">{{ instructions }}</p>
    <p class="allowed-files"><strong>Allowed files:</strong> {{ allowedFiles }}</p>

    <div class="demo-files">
      <h3>Demo Files</h3>
      <div v-if="!isVulnerable">
        <p>
          Download and upload this sample image:<br>
          <img src="/sample-image.jpg" alt="Sample" class="demo-image" />
          <br>
          <span class="demo-note">Right-click the image and choose "Save As" to download.</span>
        </p>
      </div>
      <div v-else>
        <p>
          To test the vulnerable upload, try uploading a file with a dangerous extension, like <code>.php</code> or <code>.exe</code>.<br>
          <strong>Option 1:</strong> <a href="/sample-vuln.php" download class="demo-link">Download sample-vuln.php</a> and upload it.<br>
          <strong>Option 2:</strong> Create your own <code>sample-vuln.php</code> file with the following content:
        </p>
        <pre class="demo-file-content"><code>{{ phpSample }}</code></pre>
        <button @click="copyPhpSample">Copy to Clipboard</button>
        <p class="demo-note">To create the file: Open a text editor, paste the above code, save it as <code>sample-vuln.php</code>, and upload it using the form below.</p>
      </div>
    </div>

    <input type="file" @change="handleFileChange" />
    <button @click="uploadFile" :disabled="uploading">Upload</button>
    <div v-if="uploadResult" class="upload-result">{{ uploadResult }}</div>
  </div>
</template>

<style scoped>
.upload-demo-container {
  margin: 6rem auto 2rem auto;
  padding: 2.5rem 2rem;
  max-width: 540px;
  background: rgba(26, 35, 126, 0.13);
  border: 1.5px solid var(--bank-gold);
  border-radius: 18px;
  color: var(--bank-white);
  box-shadow: 0 6px 18px rgba(0,0,0,0.10);
  font-size: 1.18rem;
  font-family: 'Segoe UI', 'Arial', sans-serif;
}

h2 {
  font-size: 2.1rem;
  color: var(--bank-gold);
  margin-bottom: 1.2rem;
  text-align: center;
}

.mode-indicator {
  display: inline-block;
  padding: 0.6rem 2.2rem;
  border-radius: 22px;
  color: #fff;
  font-weight: bold;
  font-size: 1.18rem;
  margin-bottom: 1.2rem;
  letter-spacing: 1px;
  text-align: center;
}

.instructions {
  margin-bottom: 0.7rem;
  color: var(--bank-gold);
  font-size: 1.08rem;
  text-align: center;
}

.allowed-files {
  margin-bottom: 1.7rem;
  color: #ffe066;
  font-size: 1.08rem;
  text-align: center;
}

.demo-files {
  margin-bottom: 2rem;
  background: rgba(0,0,0,0.13);
  border-radius: 12px;
  padding: 1.2rem 1rem 1.2rem 1rem;
  border: 1px solid var(--bank-gold);
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.demo-files h3 {
  font-size: 1.18rem;
  color: var(--bank-gold);
  margin-bottom: 0.7rem;
  text-align: left;
}
.demo-image {
  margin: 0.7rem 0 0.3rem 0;
  border: 1.5px solid #ffe066;
  border-radius: 6px;
  max-width: 100%;
  display: block;
}
.demo-note {
  color: #ffe066;
  font-size: 1.01rem;
  margin-top: 0.2rem;
  display: block;
}
.demo-link {
  color: #ffe066;
  text-decoration: underline;
  margin-right: 1rem;
  font-size: 1.05rem;
}
.demo-file-content {
  background: #222;
  color: #ffe066;
  padding: 0.7rem 0.8rem;
  border-radius: 6px;
  margin-bottom: 0.7rem;
  font-size: 1.08rem;
  overflow-x: auto;
}
input[type="file"] {
  margin: 1.2rem 0 0.7rem 0;
  font-size: 1.08rem;
}
button {
  background: var(--bank-gold);
  color: #1a237e;
  border: none;
  border-radius: 6px;
  padding: 0.7rem 1.5rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 0.5rem;
  margin-right: 0.5rem;
  transition: background 0.2s, color 0.2s;
}
button:hover {
  background: #ffe066;
  color: #1a237e;
}
.upload-result {
  margin-top: 1.2rem;
  color: var(--bank-gold);
  font-size: 1.13rem;
  text-align: center;
  font-weight: 600;
}
</style> 