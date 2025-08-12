<template>
  <div class="radar-container">
    <div class="radar-titulo text-h2 ma-2 pa-2">Radar</div>
    
    <v-form @submit.prevent class="search-form">
      <v-text-field 
        v-model="palavraPesquisa"
        :rules="rules" 
        variant="outlined" 
        label="Digite a empresa a ser rastreada"
        required
        clearable
      ></v-text-field>
      
      <div class="button-group">
        <v-btn 
          @click="buscarResultado(true)" 
          :loading="loading" 
          color="blue"
        >
          Pesquisar com identificação
        </v-btn>
      </div>
    </v-form>

    <v-container class="d-flex justify-center align-center">
      <v-data-table-server
        v-model:items-per-page="itensPorPagina"
        :headers="headers"
        :items="resultados"
        :items-length="totalResultados"
        :loading="loading"
        item-value="titulo"
        class="radar-table elevation-5"
      >
        <template v-slot:item.fonte="{ item }">
          <v-chip :color="getCorFonte(item.fonte)" label>
            {{ formatarFonte(item.fonte) }}
          </v-chip>
        </template>

        <template v-slot:item.url="{ item }" v-if="mostrarUrls">
          <a :href="item.url" target="_blank" rel="noopener noreferrer">
            <v-icon>mdi-open-in-new</v-icon>
          </a>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">{{ resultadosCarregados ? 'Nada encontrado sobre essa empresa' : 'Aguardando resultados...' }}</div>
        </template>
      </v-data-table-server>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const palavraPesquisa = ref('');
const resultados = ref([]);
const itensPorPagina = ref(10);
const totalResultados = ref(0);
const loading = ref(false);
const loadingResults = ref(false);
const mensagemBackend = ref('');
const resultadosCarregados = ref(false);

const rules = [
  value => !!value || 'Campo obrigatório',
  value => (value && value.length >= 3) || 'Mínimo 3 caracteres'
];

const headers = [
  { title: 'Título', key: 'titulo' },
  { title: 'Fonte', key: 'fonte' },
  { title: 'Link', key: 'url' }
];

const formatarFonte = (fonte) => {
  const fontes = {
    'instagram': 'Instagram',
    'facebook': 'Facebook',
    'google': 'Google'
  };
  return fontes[fonte] || fonte;
};

const getCorFonte = (fonte) => {
  const cores = {
    'instagram': 'purple',
    'facebook': 'blue',
    'google': 'green'
  };
  return cores[fonte] || 'grey';
};

const buscarResultado = async () => {
  if (!palavraPesquisa.value) return;
  
  loading.value = true;
  resultados.value = [];
  mensagemBackend.value = '';
  resultadosCarregados.value = false;

  try {
    const response = await fetch('/radar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome_perfil: palavraPesquisa.value })
    });

    const data = await response.json();
    mensagemBackend.value = data.mensagem;
    
    await buscarResultadosPeriodicamente();

  } catch (error) {
    console.error("Erro na pesquisa:", error);
    mensagemBackend.value = "Erro ao iniciar a pesquisa";
  } finally {
    loading.value = false;
  }
};

const buscarResultadosPeriodicamente = async () => {
  loadingResults.value = true;
  const maxTentativas = 15;
  let tentativas = 0;

  const verificarResultados = async () => {
    tentativas++;
    
    try {
      const response = await fetch('/radar/resultados', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome_perfil: palavraPesquisa.value })
      });

      const data = await response.json();
      
      if (data.erro) throw new Error(data.erro);
      
      resultados.value = data.resultados;
      totalResultados.value = data.total;
      
      const deveParar = data.resultados.length > 0 || 
                       data.status === 'completo' || 
                       tentativas >= maxTentativas;
      
      if (deveParar) {
        resultadosCarregados.value = true;
        if (tentativas >= maxTentativas) {
          mensagemBackend.value += "\nMáximo de tentativas alcançado";
        }
      }
      
      return deveParar;
      
    } catch (error) {
      if (tentativas >= maxTentativas) {
        mensagemBackend.value += `\nErro: ${error.message}`;
        resultadosCarregados.value = true;
        return true;
      }
      return false;
    }
  };

  while (!(await verificarResultados()) && tentativas < maxTentativas) {
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  loadingResults.value = false;
};

</script>