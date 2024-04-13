<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main class="main">
    <TheWelcome />
  </main>
</template>

<style scoped>
@media (min-width: 1024px) {
  .main {
    display: flex;
    place-items: center;
    min-height: 80vh;
  }
}
</style>
