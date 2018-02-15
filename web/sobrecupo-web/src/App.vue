<template>
  <div id="app">
    <banner/>
    <!-- Lugar donde se muestra el view actual -->
    <router-view/>
  </div>
</template>

<script>
import Banner from '@/components/Banner';
export default {
  name: 'App',
  components: {
      Banner
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
