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
          @click="buscarResultado()" 
          :loading="loading" 
          color="blue"
        >
          Pesquisar
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
        class="radar-table elevation-5"
      >
        <template v-slot:item.fonte="{ item }">
          <v-chip :color="getCorFonte(item.fonte)" label>
            {{ formatarFonte(item.fonte) }}
          </v-chip>
        </template>

        <template v-slot:item.url="{ item }">
          <a :href="item.url" target="_blank" rel="noopener noreferrer" v-if="item.url">
            <v-icon>mdi-open-in-new</v-icon>
          </a>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            {{ resultadosCarregados ? 'Nada encontrado sobre essa empresa' : 'Aguardando resultados...' }}
          </div>
        </template>
      </v-data-table-server>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { API_ENDPOINTS } from '@/config/api';

const palavraPesquisa = ref('');
const resultados = ref([]);
const itensPorPagina = ref(10);
const totalResultados = ref(0);
const loading = ref(false);
const mensagemBackend = ref('');
const resultadosCarregados = ref(false);

const rules = [
  value => !!value || 'Campo obrigatório',
  value => (value && value.length >= 3) || 'Mínimo 3 caracteres'
];

const headers = [
  { title: 'Resultado', value: 'resultado' },
  { title: 'Fonte', value: 'fonte' },
  { title: 'Link', value: 'url' }
];

const formatarFonte = (fonte) => {
  const fontes = { instagram: 'Instagram', facebook: 'Facebook', google: 'Google' };
  return fontes[fonte] || fonte;
};

const getCorFonte = (fonte) => {
  const cores = { instagram: 'purple', facebook: 'blue', google: 'green' };
  return cores[fonte] || 'grey';
};

const buscarResultado = async () => {
  if (!palavraPesquisa.value) return;

  loading.value = true;
  mensagemBackend.value = '';
  resultadosCarregados.value = false;
  resultados.value = [];

  try {
    const postResp = await fetch(API_ENDPOINTS.RADAR, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome_perfil: palavraPesquisa.value })
    });
    const postData = await postResp.json();

    if (!postResp.ok) {
      mensagemBackend.value = postData.erro || 'Erro ao iniciar pesquisa';
      resultadosCarregados.value = true;
      return;
    }

    mensagemBackend.value = postData.mensagem || 'Pesquisa iniciada...';

    const url = `${API_ENDPOINTS.RADAR_RESULTADOS}?nome_perfil=${encodeURIComponent(palavraPesquisa.value)}`;
    const getResp = await fetch(url);
    const getData = await getResp.json();

    if (getData.erro) throw new Error(getData.erro);

    if (Array.isArray(getData.resultados)) {
      resultados.value = getData.resultados.map((r, idx) => ({
        id: idx,
        resultado: r.resultado || r.nome_pesquisa || r.nome_perfil || '',
        fonte: r.fonte,
        url: r.url,
      }));
      totalResultados.value = resultados.value.length;
    } else {
      resultados.value = [];
      totalResultados.value = 0;
    }

    resultadosCarregados.value = true;
    mensagemBackend.value = `Consultado. ${resultados.value.length} resultado(s) encontrado(s)`;

  } catch (e) {
    mensagemBackend.value = `Erro: ${e.message}`;
    resultadosCarregados.value = true;
  } finally {
    loading.value = false;
  }
};
</script>