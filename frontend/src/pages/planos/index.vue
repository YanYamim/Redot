<template>
  <div class="bg-white h-100">
    <v-responsive
      class="align-centerfill-height mx-auto "
      max-width="900"
    >
      <PlanosPagamentos />
    </v-responsive>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import PlanosPagamentos from '@/components/PlanosPagamentos.vue'
const store = useAppStore()
onMounted(async () => {
    await store.verify()
})
</script>