// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  actions: {
    // Adicione este método se for necessário
    verify() {
      // Implementação da verificação
      return Promise.resolve();
    }
  }
});
