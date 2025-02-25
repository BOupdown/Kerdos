<script setup>
import { reactive } from 'vue';
</script>

<template>
  <div class="container">
    <div class="top-nav">
      <RouterLink to="/" class="nav-button">Accueil</RouterLink>
      <RouterLink to="/recherche" class="nav-button">Recherche</RouterLink>
      <RouterLink to="/chatbot" class="nav-button">Chatbot</RouterLink>
    </div>

    <div class="eleven">
      <h1>Wiki CO2</h1>
    </div>

    <RouterView />
  </div>
</template>

<style scoped>
.top-nav {
  display: flex;
  justify-content: center;
  background: linear-gradient(135deg, #000000, #514d52);
  padding: 15px 0;
  border-bottom: 2px solid #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.container {
  padding-top: 60px;
}

.eleven {
  text-align: center;
  color: #aca2a2;
  font-family: 'Times New Roman', Times, serif;
  font-size: 30px;
  margin-top: 20px;
}

.nav-button {
  color: white;
  text-decoration: none;
  padding: 12px 25px;
  margin: 0 20px;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 5px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.nav-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.nav-button:focus {
  outline: none;
}

.nav-button:active {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
