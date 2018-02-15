<template>
  <div :style='BannerStyle'>
      <img src="@/assets/logo.png"/>
      texto
  </div>
</template>

<script>
export default {
  name: 'Banner',
  data : () => {
      return {
      BannerStyle: {
          position: "fixed",
          top: 0,
          bottom: 0,
          left: 0,
          right: 0,
          height: "200px",
          backgroundColor: "#222222"
      }
    }
  }
}
</script>