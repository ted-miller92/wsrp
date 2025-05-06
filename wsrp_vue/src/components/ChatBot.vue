<template>
  <div>
    <!-- Floating Chat Icon -->
    <button
      v-if="!open"
      class="chat-fab"
      @click="open = true"
      aria-label="Open Chat"
    >
      💬
    </button>

    <!-- Chat Pane -->
    <transition name="fade">
      <div v-if="open" class="chat-pane">
        <div class="chat-header">
          <span>ChatBot</span>
          <button class="close-btn" @click="open = false">×</button>
        </div>
        <div class="chat-model-select">
          <label for="model">Model:</label>
          <select v-model="selectedModel" id="model">
            <option v-for="model in models" :key="model.value" :value="model.value">
              {{ model.label }}
            </option>
          </select>
        </div>
        <div class="chat-messages">
          <div v-for="(msg, i) in messages" :key="i" :class="msg.role">
            <span>{{ msg.role === 'user' ? 'You' : 'Bot' }}:</span> {{ msg.text }}
          </div>
        </div>
        <form class="chat-input" @submit.prevent="sendMessage">
          <input v-model="input" type="text" placeholder="Type a message..." />
          <button type="submit">Send</button>
        </form>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useChatStore } from '@/stores/chatStore';

const chatStore = useChatStore();
const open = computed({
  get: () => chatStore.open,
  set: (val) => { if (val) chatStore.openChat(); else chatStore.closeChat(); }
});
const input = ref("");
const messages = ref([]);
const selectedModel = ref("meta-llama/llama-4-maverick:free");
const models = [
  { value: "meta-llama/llama-4-maverick:free", label: "Meta-Llama: Llama 4 Maverick (Free)" },
  { value: "qwen/qwen3-235b-a22b:free", label: "Qwen 3 235B A22B (Free)" },
  { value: "google/gemini-2.0-flash-exp:free", label: "Google: Gemini 2.0 Flash Exp (Free)" },
  { value: "nvidia/llama-3.3-nemotron-super-49b-v1:free", label: "NVIDIA: Llama 3.3 Nemotron Super 49B V1 (Free)" },
  { value: "opengvlab/internvl3-14b:free", label: "OpenGVLab: InternVL3 14B (Free, 128K ctx)" },
  { value: "qwen/qwen3-30b-a3b:free", label: "Qwen 3 30B A3B (Free)" },
  { value: "deepseek/deepseek-prover-v2:free", label: "DeepSeek: DeepSeek Prover V2 (Free, 164K ctx)" },
  { value: "deepseek/deepseek-r1:free", label: "DeepSeek: DeepSeek R1 (Free)" },
  { value: "deepseek/deepseek-chat-v3-0324:free", label: "DeepSeek: DeepSeek Chat V3 0324 (Free)" },
  { value: "deepseek/deepseek-v3-base:free", label: "DeepSeek: DeepSeek V3 Base (Free)" },
  { value: "opengvlab/internvl3-2b:free", label: "OpenGVLab: InternVL3 2B (Free, 32K ctx)" },
  { value: "thudm/glm-4-9b:free", label: "THUDM: GLM-4 9B (Free)" },
  { value: "thudm/glm-z1-9b:free", label: "THUDM: GLM-Z1 9B (Free)" },
  { value: "google/gemma-3-27b-it:free", label: "Google: Gemma 3 27B IT (Free)" },
  { value: "microsoft/mai-ds-r1:free", label: "Microsoft: MAI-DS-R1 (Free)" },
  { value: "cognitivecomputations/dolphin3.0-r1-mistral-24b:free", label: "CognitiveComputations: Dolphin 3.0 R1 Mistral 24B (Free)" },
  { value: "nousresearch/deephermes-3-llama-3-8b-preview:free", label: "NousResearch: DeepHermes 3 Llama 3 8B Preview (Free)" },
  { value: "mistralai/mistral-7b-instruct", label: "Mistral 7B Instruct" },
  { value: "qwen/qwen3-0.6b-04-28:free", label: "Qwen 3 0.6B (Free)" }
];

// Show hello message when chat is opened
watch(open, (newVal) => {
  if (newVal) {
    // Only add hello if it's the first message or if chat was just opened
    if (messages.value.length === 0) {
      messages.value.push({ role: 'bot', text: 'Hello! How can I help you? Ask me about web security vulnerabilities or this demo app.' });
    }
  } else {
    // Optionally clear messages when chat is closed
    // messages.value = [];
  }
});

function sendMessage() {
  if (!input.value.trim()) return;
  const userMessage = { role: 'user', text: input.value };
  messages.value.push(userMessage);
  const userInput = input.value;
  input.value = "";

  // Show loading message
  messages.value.push({ role: 'bot', text: 'Thinking...' });

  fetchOpenRouterResponse(userInput, selectedModel.value)
    .then(botReply => {
      // Replace the loading message with the actual response
      messages.value.pop();
      messages.value.push({ role: 'bot', text: botReply });
    })
    .catch(() => {
      messages.value.pop();
      messages.value.push({ role: 'bot', text: 'Sorry, there was an error.' });
    });
}

async function fetchOpenRouterResponse(prompt, model) {
  const apiKey = import.meta.env.VITE_OPENROUTER_API_KEY;
  // Short, concise system prompt
  const systemPrompt = `You are an expert assistant for a secure banking demo app that teaches about common web security vulnerabilities and their mitigations, including SQL Injection, CSRF, XSS, File Upload, and IDOR. Answer user questions clearly and concisely in 2 sentences maximum and focused on these topics.`;
  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: prompt }
      ]
    })
  });
  if (!response.ok) throw new Error('API error');
  const data = await response.json();
  // Clean up the bot's response before returning
  let content = data.choices?.[0]?.message?.content || 'No response.';
  // Remove asterisks, excessive whitespace, and strange characters
  content = content.replace(/[\*]+/g, '') // Remove asterisks
                 .replace(/[\u200B-\u200D\uFEFF]/g, '') // Remove zero-width chars
                 .replace(/\s{2,}/g, ' ') // Collapse multiple spaces
                 .replace(/\n{2,}/g, '\n') // Collapse multiple newlines
                 .trim();
  return content;
}
</script>

<style scoped>
.chat-fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  font-size: 2rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  border: none;
  cursor: pointer;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.chat-fab:hover {
  background: var(--bank-gold-light);
}

.chat-pane {
  position: fixed;
  bottom: 2.5rem;
  right: 2.5rem;
  width: 350px;
  max-width: 95vw;
  height: 480px;
  background: rgba(26, 35, 126, 0.98);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  display: flex;
  flex-direction: column;
  z-index: 1001;
  overflow: hidden;
  border: 1.5px solid var(--bank-gold);
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  font-weight: 700;
  padding: 0.75rem 1.25rem;
  font-size: 1.1rem;
}
.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--bank-blue-dark);
  cursor: pointer;
  font-weight: bold;
}

.chat-model-select {
  padding: 0.5rem 1.25rem;
  background: rgba(255,255,255,0.05);
  border-bottom: 1px solid var(--bank-gold-light);
}
.chat-model-select label {
  font-size: 0.95rem;
  color: var(--bank-gold);
  margin-right: 0.5rem;
}
.chat-model-select select {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  border: 1px solid var(--bank-gold);
  background: var(--bank-white);
  color: var(--bank-blue-dark);
  font-size: 1rem;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background: rgba(255,255,255,0.03);
  font-size: 1rem;
  color: var(--bank-white);
}
.chat-messages .user {
  text-align: right;
  color: var(--bank-gold);
  margin-bottom: 0.5rem;
}
.chat-messages .bot {
  text-align: left;
  color: var(--bank-white);
  margin-bottom: 0.5rem;
}

.chat-input {
  display: flex;
  padding: 0.75rem 1rem;
  background: rgba(255,255,255,0.05);
  border-top: 1px solid var(--bank-gold-light);
}
.chat-input input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--bank-gold);
  font-size: 1rem;
  margin-right: 0.5rem;
  background: var(--bank-white);
  color: var(--bank-blue-dark);
}
.chat-input button {
  background: var(--bank-gold);
  color: var(--bank-blue-dark);
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.25rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.chat-input button:hover {
  background: var(--bank-gold-light);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 