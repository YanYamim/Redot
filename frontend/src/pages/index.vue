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

      <v-lazy class="bg-white">
        <v-container fluid class="py-16">
          <v-row align="center" justify="center"> 
            <v-col cols="12" md="6" class="text-left pa-6"> 
              <div>
                <img :src="redot_sem_texto" alt="Logo" class="w-40 mb-4"><br></br>
                <a style="color: #213880;" class="text-h3">
                  Comece agora a<br>
                  identificar quem<br>
                  está te copiando
                </a>
              </div>
            </v-col>

            <v-col cols="12" md="4" class="pa-6"> 
              <v-card class="pa-4 text-center rounded-xl bg-white text-black" style="border: 2px solid #213880;">
                <v-sheet
                  color="indigo darken-1"
                  height="32"
                  class="d-flex align-center justify-center rounded-t-lg ma-n5"
                >
                  <span class="white--text font-weight-bold text-caption">Recomendado</span>
                </v-sheet>

                <div class="mt-6 text-h4 font-weight-bold fonte-personalizada">Redot</div>
                <div class="text-caption text-grey">plano anual</div>

                <div class="d-flex align-center mt-6">
                  <div class="text-h8 text-decoration-line-through font-weight-bold text-left mr-2">R$2.500,00</div>
                  <v-chip color="green" text-color="white" small class="mt-1">40% OFF</v-chip>
                </div>

                <div class="text-h4 font-weight-bold color-padrao">R$49,79 <span class="text-caption">/ mês</span></div>
                
                <v-divider class="my-3"></v-divider>

                <v-btn color="green" class="mt-4 rounded-pill" @click="comecar">Identificar agora</v-btn>

                <v-list dense class="bg-white">
                  <v-list-item>
                    <v-list-item-content class="d-flex align-center">
                      <v-icon color="success" class="mr-2">mdi-check</v-icon>
                      <span>Identificador de concorrentes.</span>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content class="d-flex align-center">
                      <v-icon color="success" class="mr-2">mdi-check</v-icon>
                      <span>Identificador de perfil.</span>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content class="d-flex align-center">
                      <v-icon color="success" class="mr-2">mdi-check</v-icon>
                      <span>Identificador de perfil de anúncio.</span>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content class="d-flex align-center">
                      <v-icon color="success" class="mr-2">mdi-check</v-icon>
                      <span>Identificador de contas.</span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-lazy>

      <v-lazy>
        <v-container fluid class="py-16 d-flex flex-column align-center justify-center text-center" style="background-color: #213880">
            <h1 class="mb-6 text-white">
              Vai deixar seu concorrente reinar ou identificar?
            </h1>
          </v-container>
        </v-lazy>

      <v-lazy class="bg-grey">
        <v-container fluid class="py-16 d-flex flex-column align-center justify-center text-center">
          <h1 class="mb-6 text-white text-center">Veja quem usou nossa solução</h1>
          <v-row class="d-flex justify-space-around"> 

            <v-col cols="12" md="5" class="px-4"> 
              <v-card class="bg-white rounded-lg pa-6" height="100%"> 
                <h1 class="my-4 text-red">CHARME KIDS - Moda infatil</h1> 
                <h3 class="text-grey">Os resultados foram bastantes satisfatórios, descobri várias<br></br>
                empresas usando o nome da minha marca sem minha devida permissão</h3>
              </v-card>
            </v-col>

            <v-col cols="12" md="5" class="px-4">
              <v-card class="bg-white rounded-lg pa-6" height="100%">
                <h1 class="my-4 text-red">Tomás Menezes</h1>
                <h3 class="text-grey">A experiência foi imediata e<br></br>incrível, com o Redot consegui descobrir vários<br></br>
                  concorrentes que estavam usando minha marca</h3>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-lazy>

      <v-lazy>
        <v-container fluid class="py-16 d-flex flex-column align-center justify-center text-center">
          <h1 class="mb-8" style="color: #213880">Saia na frente e com vantagem</h1> 
          
          <div class="d-flex flex-column align-center" style="width: 100%; max-width: 800px;">
            <div class="d-flex justify-space-between w-100 mb-4">
              <h2 class="text-left" style="width: 45%; color: #213880;">Identifique<br></br>Anúncios</h2>
              <h2 class="text-right" style="width: 45%; color: #213880">Identifique<br></br> Contas</h2> 
            </div>
            
            <img :src="redot_sem_fundo" alt="logo" class="logo_sem_fundo my-6">
            
              <div class="d-flex justify-space-between w-100 mt-4">
              <h2 class="text-left" style="width: 45%; color: #213880">Identifique<br></br> Concorrentes</h2> 
              <h2 class="text-right" style="width: 45%; color: #213880">Combate a<br></br> falsificações</h2> 
            </div>
          </div>
        </v-container>
      </v-lazy>

      <v-lazy>
      <v-container fluid class="py-16 d-flex flex-column align-center justify-center text-center" style="background-color: #213880">
        <h1 class="mb-6 text-white text-center">Para quem é o Redot?</h1>
        <v-row class="d-flex justify-space-around"> 

          <v-col cols="12" md="3" class="px-4"> 
            <v-card class="bg-white rounded-lg pa-6" height="100%"> 
              <v-icon size="48" color="black" class="mt-4">mdi-account-supervisor</v-icon>
              <h1 class="my-4 text-red">Influenciadores</h1> 
              <h3>Ajuda na busca de quem pode estar te copiando</h3>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" class="px-4">
            <v-card class="bg-white rounded-lg pa-6" height="100%">
              <v-icon size="48" color="black" class="mt-4">mdi-factory</v-icon>
              <h1 class="my-4 text-red">Indústria</h1>
              <h3>Identifica informações falsas ou perfis piratas</h3>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" class="px-4">
            <v-card class="bg-white rounded-lg pa-6" height="100%">
              <v-icon size="48" color="black" class="mt-4">mdi-store</v-icon>
              <h1 class="my-4 text-red">Comércio</h1>
              <h3>Localize concorrentes utilizando seu nome</h3>
            </v-card>
          </v-col>
        </v-row>
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
import redot_sem_texto from '@/assets/redot_sem_texto.png'
import redot_sem_fundo from '@/assets/redot_sem_fundo.png'
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

.logo_sem_fundo {
  max-width: 150px;
}
</style>