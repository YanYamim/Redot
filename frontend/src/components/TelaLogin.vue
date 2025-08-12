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
          <v-btn :disabled="!valid" color="green" @click="acessarUsuario">
            Entrar
          </v-btn>
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

const router = useRouter()
const form = ref(null)
const valid = ref(null)

const initialState = { email: '', senha: '' }
const state = reactive({ ...initialState })

const rules = {
  email: [
    (v) => /.+@.+\..+/.test(v) || 'E-mail inválido',
  ],
  senha: [(v) => !!v || 'Senha é obrigatória'],
}

const acessarUsuario = async () => {
  const result = await form.value.validate()
  if(!result.valid) return

  try {
    await axios.post(`http://127.0.0.1:5000/usuario/cadastro`, body)
    router.push('/login/')
  } catch (error) {
    console.error('Erro ao cadastrar:', error)
  }
}
</script>