import { defineStore } from 'pinia';

export const useChatStore = defineStore('chat', {
  state: () => ({
    open: false,
  }),
  actions: {
    openChat() {
      this.open = true;
    },
    closeChat() {
      this.open = false;
    },
    toggleChat() {
      this.open = !this.open;
    }
  }
}); 