<template>
  <div class='sidebarcontainer'>
    <h1>Salones</h1>

    <div class=listElement v-for='block, index in blocks' >
        <form action="#" >
          <div class='checkboxIcon'>
            <input type="checkbox" :name='block' @change='addBlock()' @  :id="'test' + index " />
            <label :for="'test' + index "> </label>
          </div>
          <h4 >{{block}}</h4>
        </form>
    </div>

  </div>
</template>

<style>
.sidebarcontainer{
  width: 17rem;
  background-color: #b2dfdb;
  height: 100%;
  margin-left: 1rem;
  border-radius: 1rem
}
.listElement{
  background-color: #80cbc4;
  margin:auto;
  margin-bottom: 1rem;
  font-size: 2rem;
  display: block;
  width: 10rem;
  border-radius: 0.6rem;
}
form{
  display: flex;
  flex-direction: row
}

.checkboxIcon{
  display: flex;
  flex-direction: row;
  margin: auto 1rem;
  margin-left: 1.5rem
}

</style>


<script>

export default {
  name: 'sidebarcontainer',
  data () {
    return {
      filter: []
    }
  },
  props: {
    blocks: {
      type: Array,
      default: function () {
        return [ 'ML', 'AU', 'W', 'LL', 'O', 'B', 'SD', 'Q', 'TX', 'Z' ]
      }
    }
  },
  methods: {
    addBlock: function () {
      var newArray = []
      Array.from(document.getElementsByTagName('input')).forEach(function (aBlock) {
        if (aBlock.checked) {
          newArray.push(aBlock.name)
        }
      })
      this.$store.state.filter = newArray
    }
  }
}
</script>
