<template>
  <div style="margin-top: 10%" id="app">
    <banner/>
    <!-- Current view display -->
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
