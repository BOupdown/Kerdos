<template>

  <div class="center-image">
    <img src="../assets/planet-4398004_1280-removebg-preview.png" alt="Image Description">
  </div>
</template>

<script setup>
</script>

<style scoped>

.center-image {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 450px; /* Ajuste la hauteur selon tes besoins */
}

.center-image img {
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}



</style>

