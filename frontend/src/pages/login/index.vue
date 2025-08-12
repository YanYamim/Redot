<template>
  <div class="bg-white h-100">
    <v-responsive
      class="align-centerfill-height mx-auto "
      max-width="900"
    >
      <TelaLogin />
    </v-responsive>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const store = useAppStore()

onMounted(async () => {
  await store.verify()
})
</script>