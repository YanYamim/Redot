<template>
  <v-app-bar class="px-4 d-flex justify-space-between align-center" color="white" :elevation="2">
    <div class="d-flex align-center">
      <img :src="redot_sem_fundo" alt="Logo" class="logo_sem_fundo" />
    </div>

    <div class="d-flex justify-center align-center flex-grow-1">
      <v-btn text href="/">Home</v-btn>
      <v-btn text href="/sobre">Sobre nós</v-btn>
      <v-btn text href="/faq">FAQ</v-btn>
      <v-btn text href="/demonstracao">Demonstração</v-btn>
      <v-btn text href="/Radar">Radar</v-btn>
    </div>

    <v-btn text href="/login">Login</v-btn>

    <div style="width: 100px;"></div>
  </v-app-bar>
</template>

<script lang="ts" setup>
import redot_sem_fundo from '@/assets/redot_sem_fundo.png'
</script>

<style scoped>
.logo_sem_fundo {
  max-width: 100px;
}
</style>
