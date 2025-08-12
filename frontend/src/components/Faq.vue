
<template>
<v-app class="bg-white">
    <v-container class="text-center my-16">
    <h2 class="text-h5 font-weight-bold mb-6 text-grey-darken-2">
      Perguntas frequentes (FAQ)
    </h2>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <p class="text-red mb-8 text-grey-darken-2">
          Aqui você encontra respostas para as dúvidas mais comuns sobre o funcionamento da plataforma.
        </p>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-text-field
          label="Email"
          variant="outlined"
          placeholder="Digite seu email"
          color="#753842"
          class="mb-4"
        />
        <v-text-field
          label="Sua pergunta"
          variant="outlined"
          placeholder="Digite sua pergunta"
          color="#753842"
          class="mb-4"
        />
        <div class="d-flex justify-center">
          <v-btn
            color="#ea860e"
            class="rounded-pill"
            dark
            @click="enviar"
          >
            Enviar
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</v-app>
</template>

<script setup>
const enviar = () => {
    console.log("Pergunta enviada")
}

</script>