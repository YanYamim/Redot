<template>
  <div class="bg-white h-100">
    <v-responsive
      class="align-centerfill-height mx-auto ">
      <DemonstracaoRadar />
    </v-responsive>
  </div>
</template>

<script setup lang="ts">
import DemonstracaoRadar from '@/components/DemonstracaoRadar.vue'
import { useAppStore } from '@/stores/app'
const store = useAppStore()
onMounted(async () => {
    await store.verify()
})
</script>