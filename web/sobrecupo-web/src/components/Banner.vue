<template>
  <nav :style='BannerStyle'>
      <img :style='ImageStyle' src="@/assets/SobrecupoTransparente.png"/>
  </nav>
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
          height: "5em",
          backgroundColor: "rgba(34, 34, 34, 0.4)"
      },
      ImageStyle: {
        height: "100%"
      }
    }
  }
}
</script>