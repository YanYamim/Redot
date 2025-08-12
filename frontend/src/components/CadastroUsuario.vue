<template>
  <div class="text-h2">
    Crie sua conta
  </div>
  <v-form v-model="valid" ref="form">
    <v-container>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.identificacao"
            :counter="14"
            type="number"
            :rules="rules.identificacao"
            label="CPF/CNPJ"
            required
          ></v-text-field>
        </v-col>
        
        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.nomeUsuario"
            :counter="30"
            :rules="rules.nomeUsuario"
            :label="nomeLabel"
          ></v-text-field>
        </v-col>


        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.email"
            :rules="rules.email"
            label="E-mail"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.rg"
            :counter="10"
            type="number"
            :rules="rules.rg"
            label="RG"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.senha"
            :rules="rules.senha"
            type="password"
            label="Senha"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.cep"
            :rules="rules.cep"
            type="number"
            label="CEP"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.numero"
            type="number"
            :rules="rules.numero"
            label="Número"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.complemento"
            :rules="rules.complemento"
            label="Complemento"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.telefone"
            type="number"
            :rules="rules.telefone"
            label="Telefone"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="state.celular"
            type="number"
            :rules="rules.celular"
            label="Celular"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row justify="center" class="mt-4">
        <v-btn :disabled="!valid" color="green" @click="salvarUsuario">
          Cadastrar
        </v-btn>
      </v-row>
    </v-container>
  </v-form>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form = ref(null)
const valid = ref(null)

const initialState = { nomeUsuario: '', identificacao: '', email: '', rg: '', senha: '', cep: '', numero: '', complemento: '', telefone: '', celular: '' }
const state = reactive({ ...initialState })

const rules = {
  identificacao: [(v) => !!v || 'CPF/CNPJ é obrigatório'],
  email: [
    (v) => /.+@.+\..+/.test(v) || 'E-mail inválido',
  ],
  senha: [(v) => !!v || 'Senha é obrigatória'],
  rg: [(v) => !!v || 'RG é obrigatório'],
  cep: [(v) => !!v || 'CEP é obrigatório']
}

const nomeLabel = computed(() => {
  const length = state.identificacao?.toString().replace(/\D/g, '').length || 0
  if (length > 14) return 'Razão Social'
  if (length === 11) return 'Nome'
  return 'Nome/Razão Social'
})

const salvarUsuario = async () => {
  const result = await form.value.validate()
  if(!result.valid) return

  const identificacao = state.identificacao.replace(/\D/g, '')
  let tipo = ''
  const body = {
    email: state.email,
    rg: state.rg,
    senha: state.senha,
    cep: state.cep,
    numero: state.numero,
    complemento: state.complemento,
    telefone: state.telefone,
    celular: state.celular
  }

  if(identificacao.length === 11) {
    tipo = 'F'
    body.tipo = tipo
    body.cpf = identificacao
    body.nome_usuario = state.nomeUsuario
  } else if(identificacao.length === 14) {
    tipo = 'J'
    body.tipo = tipo
    body.cnpj = identificacao
    body.razao_social = state.nomeUsuario
  }

  try {
    await axios.post(`http://127.0.0.1:5000/usuario/cadastro`, body)
    router.push('/login/')
  } catch (error) {
    console.error('Erro ao cadastrar:', error)
  }
}
</script>