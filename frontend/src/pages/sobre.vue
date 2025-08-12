<template>
  <div class="bg-white h-100">
    <SobreNos />
  </div>
</template>


<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import SobreNos from '@/components/SobreNos.vue'
const store = useAppStore()
onMounted(async () => {
    await store.verify()
})
</script>