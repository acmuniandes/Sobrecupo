<template>
    <div v-bind:style='[outerCircleDefault, outerCircleStyle(time)]'>
        <div v-bind:style='innerCircleStyle'>
            {{classroom}}
        </div>
    </div>
</template>

<script>
export default {
  name: "ClassroomTimer",
  data() {
    return {
      classroom: "ML 603",
      innerCircleStyle: {
        width: "110px",
        height: "110px",
        backgroundColor: "black",
        borderRadius: "50%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      },
      outerCircleDefault: {
        width: "120px",
        height: "120px",
        borderRadius: "50%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "whitesmoke"
      },
      time: -100
    };
  },
  mounted () {
      this.time = this.releasedIn;
      setInterval(this.updateDatetime, 1000);
  },
  props: [
      'released-in',
      'max-time'
  ],
  methods: {
    outerCircleStyle: function(a) {
      let angle = -(this.time / this.maxTime) * 360;
      if (this.time >= this.maxTime / 2) {
        angle -= 90;
        console.log(angle);
        return {
          backgroundImage:
            "linear-gradient(" +
            angle +
            "deg, #ffc500 48%, transparent 50%), " +
            "linear-gradient(90deg, #ffc500 50%, transparent 50%)"
        };
      } else {
        angle -= 90;
        return {
          backgroundImage:
            "linear-gradient(-90deg, whitesmoke 50%, transparent 60%)," +
            "linear-gradient(" +
            angle +
            "deg, #ffc500 48%, transparent 50%)"
        }
      }
    },
    updateDatetime: function(){
        this.time -= 1
    }
  }
};
</script>
