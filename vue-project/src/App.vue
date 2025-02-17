<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/">Accueil</RouterLink>
      </nav>
  </header>

  <RouterView />
</template>


<style scoped>
</style>