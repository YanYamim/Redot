<template>
<v-container>
  <v-row justify="center" align="stretch" class="ma-n3">
    
    <!-- Plano Test -->
    <v-col cols="12" md="3" class="pa-3">
      <v-card class="pa-4 text-center rounded-xl bg-white text-black" style="border: 2px solid #213880;">
        <div class="text-h4 font-weight-bold fonte-personalizada">Redot Test</div>
        <div class="text-caption text-grey">plano por um mês</div>

        <div class="d-flex align-center mt-6">
          <div class="text-h8 text-decoration-line-through font-weight-bold text-left mr-2">R$2.500,00</div>
          <v-chip color="green" text-color="white" small class="mt-1">40% OFF</v-chip>
        </div>

        <div class="text-h4 font-weight-bold color-padrao">R$99,79 <span class="text-caption">por um mês</span></div>
        
        <v-divider class="my-3"></v-divider>

        <v-btn color="#213880" class="mt-4 rounded-pill" @click="() => pagamento('Redot Test')">Identificar agora</v-btn>

        <!-- Lista características -->
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
        
        <v-divider class="my-3"></v-divider>
   
        <!-- Lista Buscas -->
        <div class="text-subtitle-6 font-weight-medium mb-2">Busca ativa</div>
        <v-list dense class="bg-white">
          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Facebook</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Instagram</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Google</span>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-col>

    <!-- Plano Recomendado -->
    <v-col cols="12" md="3" class="pa-3">
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

        <v-btn color="green" class="mt-4 rounded-pill" @click="() => pagamento('Redot')">Identificar agora</v-btn>

        <!-- Lista características  -->
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
      
        <v-divider class="my-3"></v-divider>
        
        <!-- Lista Buscas -->
        <div class="text-subtitle-6 font-weight-medium mb-2">Busca ativa</div>
        <v-list dense class="bg-white">
          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Facebook</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Instagram</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Google</span>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-col>
   
    <!-- Plano Note -->
    <v-col cols="12" md="3" class="pa-3">
      <v-card class="pa-4 text-center rounded-xl bg-white" style="border: 2px solid #213880;">
        <div class="text-h4 font-weight-bold fonte-personalizada">Redot Note</div>
        <div class="text-caption text-grey">plano anual</div>

        <div class="d-flex align-center mt-6">
          <div class="text-h8 text-decoration-line-through font-weight-bold text-left mr-2">R$2.500,00</div>
          <v-chip color="green" text-color="white" small class="mt-1">40% OFF</v-chip>
        </div>
        
        <div class="text-h4 font-weight-bold color-padrao">R$125,00 <span class="text-caption">/ mês</span></div>
        
        <v-divider class="my-3"></v-divider>
        <v-btn color="#213880" class="mt-4 rounded-pill" @click="() => pagamento('Redot Note')">Identificar agora</v-btn>

        <!-- Lista características -->
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

        <v-divider class="my-3"></v-divider>

        <!-- Lista Buscas -->
        <div class="text-subtitle-6 font-weight-medium mb-2">Busca ativa</div>
        <v-list dense class="bg-white">
          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Facebook</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Instagram</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Google</span>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-col>  

     <!-- Plano Advance -->
    <v-col cols="12" md="3" class="pa-3">
      <v-card class="pa-4 text-center rounded-xl bg-white" style="border: 2px solid #213880;">
        <div class="text-h4 font-weight-bold fonte-personalizada">Redot Advance</div>
        <div class="text-caption text-grey">plano anual</div>

        <div class="d-flex align-center mt-6">
          <div class="text-h8 text-decoration-line-through font-weight-bold text-left mr-2">R$6.873,90</div>
          <v-chip color="green" text-color="white" small class="mt-1">15% OFF</v-chip>
        </div>
        
        <div class="text-h4 font-weight-bold color-padrao">R$820,90 <span class="text-caption">/ mês</span></div>
        
        <v-divider class="my-3"></v-divider>
        <v-btn color="#213880" class="mt-4 rounded-pill" @click="() => pagamento('Redot Advance')">Identificar agora</v-btn>

        <!-- Lista características -->
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

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Diagnóstico Proteção.</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Notificação Extrajudicial.</span>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-divider class="my-3"></v-divider>

        <!-- Lista Buscas -->
        <div class="text-subtitle-6 font-weight-medium mb-2">Busca ativa</div>
        <v-list dense class="bg-white">
          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Facebook</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Instagram</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Google</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>INPI</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Marketplace</span>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-icon color="success" class="mr-2">mdi-check</v-icon>
              <span>Ifood</span>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-col>  
   </v-row>
</v-container>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()

const pagamento = (plano) => {
  router.push({ 
  path: '/planos/pagamento',
  query: { plano: encodeURIComponent(plano) },
  state: { planoSelecionado: plano}
  })
}

</script>

<style scoped>
.color-padrao {
  color: #213880;
}

.fonte-personalizada {
  font-family: 'Playfair Display', serif;
}

</style>