<template>
  <v-footer class="d-flex flex-column ga-2 py-4" color="#cacbbb">
    <div class="footer-left-content">
      <img 
        :src="redot_sem_fundo" 
        alt="logo" 
        class="logo_footer w-25"
      >
      <a class="logo-caption">Este site é de propriedade e operado por<br>Todos os direitos reservados a Redot by power Mavip</a>
    </div>

    <div class="footer-links text-black">
      <strong>Política de Privacidade</strong>
      <br><br>
      <strong>Termos de Uso</strong>
      <br><br>
      <strong>Contate-nos</strong>
    </div>
  </v-footer>
</template>

<script setup>
import redot_sem_fundo from '@/assets/redot_sem_fundo.png'
</script>

<style scoped>
.footer-left-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-right: auto;
  padding-left: 16px;
}

.logo_footer {
  width: 200px !important;
  height: auto !important;
}

.logo-caption {
  text-align: left;
  margin-top: 8px;
}

.footer-links {
  text-align: center;
  width: 100%;
}
</style>