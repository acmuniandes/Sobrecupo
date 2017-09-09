<template>
  <div class='Drawer'>

    <salon v-for='classroom in $store.state.classrooms' :classroomname="classroom._id" :remainingtime="classroom[0]"></salon>

  </div>
</template>

<style>
.Drawer{
  /*width:40rem;*/
  background-color:#b3e5fc;
  margin-left:1rem;
  margin-right: 1rem;
  width:90%;
  border-radius: 1rem;
  z-index: -999
}


</style>


<script>
import Salon from './Salon'
import $ from 'jquery'
export default {
  name: 'drawer',
  components: {Salon},
  data () {
    return {
      datossalones: []
    }
  },
  props: {
    myfilter: {}
  },
  methods: {
    loadJSON: function (callback) {
      var xobj = new XMLHttpRequest()
      xobj.overrideMimeType('application/json')
      xobj.open('GET', 'src/assets/classrooms.json', true) // Replace 'my_data' with the path to your file
      xobj.onreadystatechange = function () {
        if (xobj.readyState === 4 && xobj.status === '200') {
        // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
          callback(xobj.responseText)
        }
      }
      xobj.send(null)
    }
  },
  ready: function () {
    console.log('inicia2')
    $.getJSON('./classrooms.json', function (obj) {
      console.log(obj)
    })
  }

}
</script>
