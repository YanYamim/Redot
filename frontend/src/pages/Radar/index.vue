<template>
  <div class="bg-white h-100">
    <v-responsive
      class="align-centerfill-height mx-auto "
      max-width="900"
    >
      <Radar />
    </v-responsive>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import Radar from '@/components/Radar.vue'
const store = useAppStore()
onMounted(async () => {
    await store.verify()
})
</script>