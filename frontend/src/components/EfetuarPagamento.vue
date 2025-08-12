<template>
  <v-form v-model="valid" ref="form">
    <v-container>
      <v-row>
        <v-col cols="12" md="8">
          <v-select
            v-model="state.formaPagamento"
            :items="opcoesPagamento"
            :rules="rules.formaPagamento"
            label="Forma de Pagamento"
            required
          ></v-select>
        </v-col>

        <template v-if="state.formaPagamento.includes('Cartão')">
          <v-col cols="12" md="8">
            <v-text-field
              v-model="state.numeroCartao"
              :rules="rules.numeroCartao"
              label="Número do Cartão"
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="8">
            <v-text-field
              v-model="state.validadeCartao"
              :rules="rules.validadeCartao"
              label="Validade (MM/AA)"
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="8">
            <v-text-field
              v-model="state.cvc"
              :rules="rules.cvc"
              label="CVC"
              required
            ></v-text-field>
          </v-col>
        </template>
      </v-row>

      <v-btn :disabled="!valid" color="green" @click="efetuarCompra">
        Efetuar Pagamento
      </v-btn>
    </v-container>
  </v-form>

  <v-overlay
    :model-value="pagamentoRealizado"
    opacity="0.7"
    class="d-flex align-center justify-center"
  >
    <v-card class="pa-6 text-center rounded-xl" color="#cacbbb">
      <v-icon
        color="green"
        size="64"
        class="mb-4"
      >
        mdi-check-circle
      </v-icon>
      <h1>Pagamento realizado com sucesso</h1>
    </v-card>
  </v-overlay>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form = ref(null)
const valid = ref(null)
const pagamentoRealizado = ref(false)
const planoSelecionado = ref('')

const planosIds = {
  'Redot Test': 1,   
  'Redot': 2,        
  'Redot Note': 3    
}

const initialState = { formaPagamento: '', numeroCartao: '', validadeCartao: '', cvc: ''}
const state = reactive({ ...initialState })

const opcoesPagamento = [
    'Pix',
    'Cartão de crédito(Visa)',
    'Cartão de crédito(Mastercard)',
    'Boleto bancário'
];

const rules = {
  formaPagamento: [(v) => !!v || 'Selecionar uma forma de pagamento é obrigatória'],
  numeroCartao: [(v) => !!v || 'Número do cartão é obrigatório'],
  validadeCartao: [(v) => !!v || 'Validade do cartão é obrigatória'],
  cvc: [(v) => !!v || 'CVC do cartão é obrigatório']
}

onMounted(() => {
  planoSelecionado.value = decodeURIComponent(router.currentRoute.value.query.plano || '')
  
  if(!planoSelecionado.value) {
    console.error('Nenhum plano recebido! Query:', router.currentRoute.value.query)
    router.push('/planos')
  }
})

const efetuarCompra = async () => {
    try {
      const idTipoPlano = planosIds[planoSelecionado.value]
      const body = {
        id_tipo_plano: idTipoPlano,
        id_conta: 1
      }

      const response = await axios.post(`http://127.0.0.1:5000/planos/pagamento`, body, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      pagamentoRealizado.value = true
      setTimeout(() => {
        pagamentoRealizado.value = false
      }, 3000)

    } catch (error) {
        console.error('Erro ao finalizar compra:', error)
        alert(error.message || 'Erro ao processar pagamento')
    }
}
</script>