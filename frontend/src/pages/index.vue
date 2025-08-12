<template>
    <v-app class="bg-white">
      <v-container
        fluid
        class="py-16 d-flex flex-column align-center justify-center text-center" style="background-color: #213880"
      >
        <div style="width: 600px;" class="text-left">
          <h2 class="mb-6 text-white">
            Descubra se alguém está usando <br />seu perfil ou marca
          </h2>

          <h3 class="mb-6 text-white">
            Cansado de encontrar pessoas te copiando?!
          </h3>

          <h3 class="mb-6 text-white">
            Descubra se alguém está usando <br />seu perfil ou marca
          </h3>

          <div class="d-flex align-center">
            <v-text-field
              label="Insira um nome de perfil ou marca"
              variant="outlined"
              class="flex-grow-1 text-white"
            />
            <v-btn
              color="#ea860e"
              class="ml-5 rounded-pill"
              dark
              @click="comecar"
            >
              Descobrir
            </v-btn>
          </div>

          <v-row justify="start" align="center" class="gap-4 mt-6">
            <v-col cols="auto">
              <v-card class="pa-2 d-flex align-center justify-center" elevation="2">
                <v-icon size="24" color="white" class="mr-2">mdi-lock</v-icon>
                <div class="text-subtitle-2 font-weight-medium">
                  SECURE<br />Totalmente seguro
                </div>
              </v-card>
            </v-col>

            <v-col cols="auto">
              <v-card class="pa-2 d-flex align-center justify-center" elevation="2">
                <v-icon size="24" color="white" class="mr-2">mdi-shield</v-icon>
                <div class="text-subtitle-2 font-weight-medium">
                  100%<br />Confiável
                </div>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-container>


      <v-lazy class="bg-grey">
        <v-container class="py-12">
          <v-row justify="center" align="center">
            <v-col cols="12" md="12">
                <h2 class="text-h4 font-weight-bold mb-4 text-center">
                  "Perfis e marcas de sucesso são sempre copiadas e, portanto, precisam de proteção completa"
                </h2>
            </v-col>
          </v-row>
        </v-container>
      </v-lazy>

    <h1 style="color: #753842;" align="center">Como descobrir quem está usando seu perfil?</h1>

    <v-lazy>
      <v-container class="py-12">
        <v-row justify="center" align="center" dense>
          <v-col cols="12" class="text-center d-flex flex-column align-center">
              <img :src="redot_sem_texto" alt="Logo" class="logo_sem_texto">
              <h3 style="color: #4b484b;" class="text-h6 mt-2">Crie uma conta</h3>
              <p>Somente o número de telefone, e-mail e senha são necessários.</p>
          </v-col>
          
          <v-divider class="my-4" thickness="3"></v-divider>

          <v-col cols="12" class="text-center d-flex flex-column align-center">
              <img :src="redot_sem_texto" alt="Logo" class="logo_sem_texto">
              <h3 style="color: #4b484b;" class="text-h6 mt-2">Envie um nome de perfil ou marca</h3>
              <p>Redot enviará lista de perfis ou marcas associadas a sua.</p>
          </v-col>

          <v-divider class="my-4" thickness="3"></v-divider>

          <v-col cols="12" class="text-center d-flex flex-column align-center">
              <img :src="redot_sem_texto" alt="Logo" class="logo_sem_texto">
              <h3 style="color: #4b484b;" class="text-h6 mt-2">Você será notificado</h3>
              <p>Receba atualizações permanentes ou selecione 30 dias.</p>
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
      <div class="d-flex ga-3">
        <img :src="planos" alt="logo" class="logo_footer"></img>
      </div>
      <v-lazy>
        <v-container
          fluid
          class="py-16 d-flex flex-column align-center justify-center text-center" style="background-color: #213880"
        >
          <h1 class="mb-6 text-white">
            Ficou com alguma dúvida?
          </h1>

          <h3 class="mb-6 text-white">
            Visite nossa central de dúvidas, lá você encontra respostas para dúvidas<br></br>frequentes ou entre em contato direto com nosso time de especialistas
          </h3>
            <v-btn
              color="#ea860e"
              class="ml-5 rounded-pill"
              dark
              @click="duvidas"
            >
              Fale conosco agora 
            </v-btn>
        </v-container>
      </v-lazy>
  </v-app>
</template>

<script setup>
import router from '@/router'
import { shallowRef } from 'vue'
import redot_sem_texto from '@/assets/redot_sem_texto.png'
import planos from '@/assets/planos.png'

const comecar = async () => {
  router.push('/planos')
}

const duvidas = async () => {
  router.push('/faq')
}
</script>

<style scoped>
.logo_sem_texto {
  max-width: 60px;
}

</style>