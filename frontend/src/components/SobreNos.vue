<template>
  <v-container
    fluid
    class="py-16 d-flex flex-column align-center justify-center text-center" style="background-color: #213880"
  >
    <div style="width: 600px;" class="text-left">
      <h2 class="mb-6 text-white">
        Quem é Redot?
      </h2>
      <h3 class="mb-6 text-white">
        Somos uma aplicação que visa proteger você que quer ter domínio sobre sua marca<br></br>
        E garantir que nenhuma outra pessoa plagie suas ideias.
      </h3>
      
    </div>
  </v-container>

  <v-lazy class="bg-grey">
    <v-container class="py-12">
      <v-row justify="center" align="center">
        <v-col cols="12" md="12">
            <h2 class="text-h4 font-weight-bold mb-4 text-center">
              Nosso objetivo é te ajudar a ter total domínio sobre sua marca!
            </h2>
        </v-col>
      </v-row>
    </v-container>
  </v-lazy>
  
<h1 style="color: #753842;" align="center">Como funciona?</h1>
<v-lazy>
  <v-container class="py-12">
    <v-row justify="center" align="center" dense>
      <v-col cols="12" class="text-center d-flex flex-column align-center">
          <img :src="redot_sem_texto" alt="Logo" class="logo_sem_texto">
          <p>Primeiramente será feito a criação do seu perfil Redot, os planos podem ser mensair ou anuais<br></br>
             Para assim sua empresa poder usufruir da aplicação</p>
      </v-col>
      
      <v-divider class="my-4" thickness="3"></v-divider>
      <v-col cols="12" class="text-center d-flex flex-column align-center">
          <img :src="redot_sem_texto" alt="Logo" class="logo_sem_texto">
          <p>Você digitará o nome do perfil ou marca o qual queira rastrear<br></br>
            Então o Redot procurará por tais nomes em diversas plataformas para te notificar<br></br>
            Caso outra empresa esteja usando o mesmo nome que o seu</p>
      </v-col>
      <v-divider class="my-4" thickness="3"></v-divider>
      <v-col cols="12" class="text-center d-flex flex-column align-center">
          <img :src="redot_sem_texto" alt="Logo" class="logo_sem_texto">
          <p>As pesquisas são feitas de forma periódica<br></br>
             Ou seja, após um determinado tempo mais pesquisas são feitas</p>
      </v-col>
    </v-row>
  </v-container>
</v-lazy>
<v-lazy>
  <v-container
      fluid
      class="py-16 d-flex flex-column align-center justify-center text-center" style="background-color: #213880"
    >
      <h1 class="mb-6 text-white">
        Pronto pra começar?
      </h1>
      <h3 class="mb-6 text-white">
        Redot é a forma mais simples de encontrar<br></br>Concorrentes, aproveitadores e criminosos
      </h3>
        <v-btn
          color="#ea860e"
          class="ml-5 rounded-pill"
          dark
          @click="comecar"
        >
          Encontrar agora
        </v-btn>
    </v-container>
  </v-lazy>
</template>

<script setup>
import router from '@/router'
import redot_sem_texto from '@/assets/redot_sem_texto.png'

const comecar = async () => {
  router.push('/planos')
}
</script>

<style scoped>
.logo_sem_texto {
  max-width: 60px;
}

</style>