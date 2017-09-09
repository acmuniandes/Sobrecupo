<template>

<h1>{{msg}}</h1>

</template>


<script>
import Salon from './Salon'

export default {
  name: 'salon',
  components: {
    Salon
  },
  data () {
    return {
      msg: 'HOLA'
    }
  }
}
</script>
