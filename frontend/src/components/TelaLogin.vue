<template>
  <v-container
    class="fill-height d-flex flex-column justify-center align-center"
  >
    <div class="text-h2 mb-6 text-center">
      Login
    </div>

    <v-form v-model="valid" ref="form" class="w-100" style="max-width: 500px">
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="state.email"
              :rules="rules.email"
              label="E-mail"
            ></v-text-field>
          </v-col>

          <v-col cols="12">
            <v-text-field
              v-model="state.senha"
              :rules="rules.senha"
              type="password"
              label="Senha"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row justify="center" class="mt-4">
          <v-btn :disabled="!valid || isLoading" :loading="isLoading" color="green" @click="acessarUsuario">
            Entrar
          </v-btn>
        </v-row>

        <v-row v-if="errorMessage" justify="center" class="mt-4">
          <v-alert type="error" dense>
            {{ errorMessage }}
          </v-alert>
        </v-row>

        <v-row justify="center" class="mt-6">
          <h3 class="text-center">
            Não tem uma conta?<br />
            <router-link to="/login/cadastro">Crie uma agora</router-link>
          </h3>
        </v-row>
      </v-container>
    </v-form>
  </v-container>
</template>



<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_ENDPOINTS } from '@/config/api'

const router = useRouter()
const form = ref(null)
const valid = ref(null)
const errorMessage = ref('')
const isLoading = ref(false)
const initialState = { email: '', senha: '' }
const state = reactive({ ...initialState })

const rules = {
  email: [
    (v) => /.+@.+\..+/.test(v) || 'E-mail inválido',
  ],
  senha: [(v) => !!v || 'Senha é obrigatória'],
}

const acessarUsuario = async () => {
  const { valid } = await form.value.validate()
  if(!valid) return

  try {
    isLoading.value = true
    errorMessage.value = ''

    const response = await axios.post(API_ENDPOINTS.LOGIN, {
      email: state.email,
      senha: state.senha
    })

    const data = response.data || {}

    if (!data.token) {
      errorMessage.value = data.erro || data.error || data.message || 'Credenciais inválidas'
      return
    }

    localStorage.setItem('authToken', data.token)
    if (data.usuario) {
      localStorage.setItem('usuario', JSON.stringify(data.usuario))
    }
    if (data.conta_id !== undefined && data.conta_id !== null) {
      localStorage.setItem('conta_id', String(data.conta_id))
    }

    router.push('/Radar')

  } catch (error) {
    if (error.response) {
      const resp = error.response.data || {}
      errorMessage.value = resp.erro || resp.error || resp.message || 'Erro na autenticação'
    } else {
      errorMessage.value = 'Não foi possível conectar ao servidor'
    }
    console.error('Erro na autenticação:', error)
  } finally {
    isLoading.value = false
  }
}
</script>