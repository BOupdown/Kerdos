<script setup>
import { reactive } from 'vue';
</script>

<template>
  <div  class="container">
    <RouterView />
    <div class="bottom-nav">
      <RouterLink to="/" class="nav-button">Accueil</RouterLink>
      <RouterLink to="/recherche" class="nav-button">Recherche</RouterLink>
      <RouterLink to="/chatbot" class="nav-button">Chatbot</RouterLink>
    </div>
  </div>
</template>

<style scoped>

/* Vos styles existants */
.center-image {
  position: fixed;
  bottom: 315px;
  left: 615px;
}

.container {
  position: relative;
  padding-bottom: 60px; /* Espace pour ne pas masquer le contenu par le bottom-nav */
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #fff; /* Couleur de fond */
  border-top: 1px solid #ccc; /* Séparation avec le contenu */
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* Effet d'ombre */
  z-index: 10;
}

.nav-button {
  text-decoration: none;
  color: #333;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-button:hover {
  color: #007BFF;
}

</style>
