<template>
  <v-footer class="text-center d-flex flex-column ga-2 py-4" color="#cacbbb">
    <div class="d-flex ga-3">
      <img :src="redot_sem_fundo" alt="logo" class="logo_footer"></img>
    </div>

    <div class="font-weight-regular text-black">
        <a>Redot</a>
    </div>

    <div>
      <strong>by power Mavip</strong>
    </div>
  </v-footer>
</template>

<script setup>
import redot_sem_fundo from '@/assets/redot_sem_fundo.png'

const openSocialLink = (url) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
.logo_footer {
  max-width: 100px;
}

</style>