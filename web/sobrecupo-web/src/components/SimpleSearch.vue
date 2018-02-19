<template>
  <div>
    <div :style="styles.container">
      <img src="@/assets/icons/search.png"/>
      <input v-on:input="toSearch" v-model="input" :style="styles.input" placeholder="Buscar..." />
    </div>
  </div>
</template>

<script>
export default {
  name: "SimpleSearch",
  data: function() {
    return {
      input: "",
      styles: {
        container:{
          backgroundColor: "whitesmoke",
          border: "4px solid #ffc600",
          borderRadius: "4px",
          display: "flex",
          width: "130px",
          alignItems: "center",
          justifyContent: "center",
          marginLeft: "25px",
          marginBottom: "25px"
        },
        input: {
          backgroundColor: "whitesmoke",
          padding: "8px",
          width: "80px",
          borderRadius: "15px",
          border: "none"
        }
      }
    }
  },
  props: [
    "search"
  ],
  methods: {
    toSearch: function() {
      this.$emit('input', this.input);
    }
  }
}
</script>
