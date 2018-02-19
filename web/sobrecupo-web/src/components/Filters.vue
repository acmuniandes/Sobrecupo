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
        <div :style="styles.filterContainer" v-show="filtering">
          <simple-search v-on:input="searchUpdate" v-model="textSearch"/>
          <div :style="styles.sliderContainer">
            <vue-slider v-on:input="timeRangeUpdate" ref="slider" v-model="timeRange" v-bind="options" :show="filtering"/>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import vueSlider from "vue-slider-component";
import SimpleSearch from "./SimpleSearch";

export default {
  name: "Filters",
  data: () => {
    return {
      filtering: false,
      textSearch: "",
      timeRange: [0, 120],
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
        },
        filterContainer: {
          display: "flex",
          alignItems: "center",
          justifyContent: "center"
        },
        sliderContainer: {
          margin: "15px",
          width: "40%"
        }
      },
      options: {
        value: [0, 120],
        width: "100%",
        height: 8,
        dotSize: 16,
        min: 0,
        max: 120,
        disabled: false,
        show: false,
        tooltip: "always",
        formatter: "{value}m",
        bgStyle: {
          backgroundColor: "#fff",
          boxShadow: "inset 0.5px 0.5px 3px 1px rgba(0,0,0,.36)"
        },
        tooltipStyle: {
          backgroundColor: "#ffc600",
          borderColor: "#ffc600"
        },
        processStyle: {
          backgroundColor: "#ffc600"
        }
      }
    };
  },
  components: {
    SimpleSearch,
    vueSlider
  },
  props: [
    'timeRange',
    'search'
  ],
  computed: {
    displayStatus: function() {
      if (this.search === "" && this.timeRange[0] === 0 && this.timeRange[1] === 120) {
        return "Mostrando todos los salones disponibles";          
      }
      return "Mostrando salones disponibles filtrados";
    },
    filterStatus: function() {
      if (this.filtering) {
        return "Cerrar filtros";
      }
      return "Filtrar";
    }
  },
  methods: {
    searchUpdate: function() {
      this.$emit('search', this.textSearch);
    },
    timeRangeUpdate: function() {
      this.$emit('timeRange', this.timeRange);
    }
  }
};
</script>
