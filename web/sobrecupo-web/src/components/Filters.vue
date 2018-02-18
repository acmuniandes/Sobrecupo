<template>
  <div>      
    <div :style='[styles.border]'>
      <div :style="[styles.filterMessage]">
        <h2>{{displayStatus}}</h2> 
        <div :style="[styles.filterMessage]" v-on:click="filtering = !filtering">
          <div :style="[styles.filterBullet, filtering ? styles.rotate : {}]"/><h2>{{filterStatus}}</h2>
        </div>
      </div>
      <transition name="move-down">
        <div v-show="filtering">
          <simple-search v-model="search"/>

          {{search}}
        </div>
      </transition>
    </div>
  </div>
</template>

<script>

import SimpleSearch from "./SimpleSearch"

export default {
  name: "Filters",
  data: () => {
    return {
      filtering: false,
      search: "",
      tags: [],
      styles: {
        filterBullet: {
          height: "0px",
          width: "0px",
          borderTop: "10px solid #ffc600",
          borderLeft: "7px solid transparent",
          borderRight: "7px solid transparent",
          marginLeft: "10px"
        },
        border: {
          width: "100%",
          borderBottom: "5px solid #ffc600",
          borderTop: "5px solid #ffc600"
        },
        filterMessage: {
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "center",
          color: "#afafaf"
        },
        rotate: {
          animationName: "bulletRotation",
          animationDuration: "1s",
          animationTimingFunction: "ease"
        }
      }
    }
  },
  components:{
    SimpleSearch
  },
  computed: {
    displayStatus: function() {
      if(this.tags.length > 0 || this.search !== ""){
        return "Mostrando salones disponibles filtrados";
      }
      return "Mostrando todos los salones disponibles";
    },
    filterStatus: function() {
      if(this.filtering){
        return "Cerrar filtros";
      }
      return "Filtrar"
    }
  },
  methods: {
    search: function() {

    }
  }
}
</script>
