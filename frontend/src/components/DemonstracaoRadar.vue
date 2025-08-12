<template>
  <v-container fluid class="fill-height ma-0 pa-0">
    <v-row no-gutters class="fill-height">
      <v-col cols="12" md="6" class="fill-height d-flex">
        <v-card class="pa-6 flex-grow-1" elevation="0" color="white">
          <div class="text-h2 font-weight-black mb-6" style="text-align: center; color:#753842">Mavip</div>

          <v-form @submit.prevent="mockResultado" class="search-form">
            <v-text-field 
              v-model="palavraPesquisa"
              :rules="rules" 
              variant="outlined" 
              label="Digite a empresa a ser rastreada"
              required
              clearable
              color="black"
            ></v-text-field>

            <div class="button-group">
              <v-btn 
                type="submit"
                :disabled="!palavraPesquisa"
                :loading="loading" 
                color="#213880"
                class="mr-2 "
              >
                Pesquisar 
              </v-btn>
            </div>
          </v-form>
          <v-divider class="my-6" thickness="3"></v-divider>
          <div class="text-h6 font-weight-black mb-6 color-padrao">Crie uma conta para ver seus concorrentes</div>

          <div class="mb-4" v-if="mostrarResultados">
            <!-- Google -->
            <div class="mb-4">
              <div class="d-flex align-center mb-2">
                <v-icon color="red" class="mr-2">mdi-check-circle</v-icon>
                <span class="font-weight-medium text-black">
                  Google: <span class="red--text">14 Ocorrências</span>
                </span>
              </div>
              <div class="blur-text">
                Fingerspitzengefühl – sensibilidade intuitiva<br>
                Kummerspeck – peso ganho por comer emocionalmente<br>
                Glühbirne – lâmpada<br>
                Staubsauger – aspirador de pó<br>
                Krankenhaus – hospital<br>
                Zugzwang – obrigação de agir (xadrez)<br>
                Lebensfreude – alegria de viver<br>
                Ignis – fogo<br>
                Pax – paz<br>
                Mors – morte<br>
                Caelum – céu<br>
                Flumen – rio<br>
                Vita – vida<br>
                Tempus – tempo<br>
              </div>
            </div>

            <!-- Instagram -->
            <div class="mb-4">
              <div class="d-flex align-center mb-2">
                <v-icon color="red" class="mr-2">mdi-check-circle</v-icon>
                <span class="font-weight-medium text-black">
                  Instagram: <span class="red--text">4 Ocorrências</span>
                </span>
              </div>
              <div class="blur-text">
                Schmetterling – borboleta<br>
                Zeitgeist – espírito da época<br>
                Wanderlust – desejo de viajar<br>
                Fernweh – saudade de lugares que nunca visitou<br>
              </div>
            </div>

            <!-- Facebook -->
            <div class="mb-4">
              <div class="d-flex align-center mb-2">
                <v-icon color="red" class="mr-2">mdi-check-circle</v-icon>
                <span class="font-weight-medium text-black">
                  Facebook: <span class="red--text">4 Ocorrências</span>
                </span>
              </div>
              <div class="blur-text">
                Staubsauger – aspirador de pó<br>
                Krankenhaus – hospital<br>
                Zugzwang – obrigação de agir (xadrez)<br>
                Lebensfreude – alegria de viver<br>
              </div>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Painel de assinatura -->
      <v-col cols="12" md="6" class="fill-height d-flex">
        <v-card class="pa-6 flex-grow-1" elevation="0" color="white">
          <div class="text-h4 mb-2 font-weight-bold" style="text-align: center; color:#753842">
            INSCREVA-SE PARA RECEBER RELATÓRIO COMPLETO
          </div>
          <div class="text-h6 mb-4 text-grey" style="text-align: center;">
            Depois de criar sua conta, terá acesso às informações relativas à identificação dos perfis encontrados
          </div>

          <!-- Oferta Exclusiva -->
          <v-divider class="my-4" thickness="3"></v-divider>

          <div class="text-center text-overline mb-2 text-black">OFERTA EXCLUSIVA</div>

          <!-- Assinatura Mensal -->
          <div class="d-flex justify-space-between align-center mb-4">
            <div class="text-h5 font-weight-bold color-padrao">
              Assinatura mensal
            </div>
            <div class="text-right">
              <div class="text-caption text-decoration-line-through text-grey">
                R$292,90
              </div>
              <div class="text-h4 font-weight-bold color-padrao">
                R$86,93
              </div>
            </div>
          </div>

          <!-- Assinatura Anual -->
          <div class="d-flex justify-space-between align-center mb-4">
            <div class="text-h5 font-weight-bold color-padrao">
              Assinatura anual
            </div>
            <div class="text-right">
              <div class="text-caption text-decoration-line-through text-grey">
                R$292,90
              </div>
              <div class="text-h4 font-weight-bold color-padrao">
                R$43,93
              </div>
            </div>
          </div>

          <v-divider class="my-4" thickness="3"></v-divider>

          <v-text-field
            label="Endereço de e-mail*"
            variant="outlined"
            dense
            v-model="email"
            :rules="emailRules"
            color="black"
          ></v-text-field>

          <v-btn color="green" class="mt-4" block @click="prosseguir" :disabled="!emailValido">
            PRÓXIMO
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import router from '@/router';
import { ref, computed } from 'vue';

  const email = ref('');
  const palavraPesquisa = ref('');
  const loading = ref(false);
  const mostrarResultados = ref(false);
  const termoPesquisado = ref('');

  const now = new Date();
  const dataAtual = now.toLocaleDateString('pt-BR');
  const horaAtual = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  const rules = [
    value => !!value || 'Campo obrigatório',
    value => (value && value.length >= 3) || 'Mínimo 3 caracteres'
  ];

  const emailRules = [
    v => !!v || 'E-mail é obrigatório',
    v => /.+@.+\..+/.test(v) || 'E-mail deve ser válido'
  ];

  const emailValido = computed(() => {
    return /.+@.+\..+/.test(email.value);
  });

  const mockResultado = () => {
    if (!palavraPesquisa.value) return;
    
    loading.value = true;
    termoPesquisado.value = palavraPesquisa.value;
    
    setTimeout(() => {
      loading.value = false;
      mostrarResultados.value = true;
    }, 1000);
  };

  const prosseguir = async () => {
    if (!emailValido.value) {
      alert('Digite um e-mail válido!');
      return;
    }
    router.push('/Planos')
  }
</script>

<style scoped>
.blur-text {
  color: transparent;
  text-shadow: 0 0 8px rgba(0,0,0,0.5);
  user-select: none;
  font-size: 0.9rem;
  line-height: 1.4;
  padding: 8px;
  background-color: #f5f5f5;
  border-radius: 4px;
  white-space: pre-line;
}

.color-padrao {
  color: #213880;
}
</style>