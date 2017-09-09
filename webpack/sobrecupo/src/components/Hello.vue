<template>
  <div class="hello">
    <SidebarContainer  ></SidebarContainer>
    <Drawer></Drawer>
  </div>
</template>

<style>
.hello{
  display: flex;
  margin-right: 30rem;
  width: 100%;
  margin: auto;
}
</style>



<script>
import SidebarContainer from './SidebarContainer'
import Drawer from './Drawer'

export default {
  name: 'hello',
  components: { SidebarContainer, Drawer },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
