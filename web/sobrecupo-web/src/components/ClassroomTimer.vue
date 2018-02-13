<template>
    <div v-bind:style='[outerCircleDefault, outerCircleStyle(time)]'>
        <div v-bind:style='innerCircleStyle'>
            <p>{{data.id}}</p>
        </div>
    </div>
</template>

<script>
export default {
  name: "ClassroomTimer",
  data() {
    return {
      innerCircleStyle: {
        width: "110px",
        height: "110px",
        backgroundColor: "black",
        borderRadius: "50%",
        justifyContent: "center",
        alignItems: "center",
        margin: "0 auto",
        color: "whitesmoke"
      },
      outerCircleDefault: {
        width: "120px",
        height: "120px",
        borderRadius: "50%",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "whitesmoke",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      },
      time: -1,
      maxTime: 500*60
    };
  },
  mounted () {
      this.time = this.data.TUO*60;
      setInterval(this.updateDatetime, 1000);
  },
  props: [
      'data'
  ],
  methods: {
    outerCircleStyle: function(a) {
      let angle = -(this.time / this.maxTime) * 360;
      if (this.time >= this.maxTime / 2) {
        angle -= 90;
        //console.log(angle);
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
