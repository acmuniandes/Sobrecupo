<template>
    <div v-bind:style='[outerCircleDefault, outerCircleStyle(time)]'>
        <div v-bind:style='innerCircleStyle'>
            <p>{{classroomName}}</p>
            <p>{{data.TUO}}</p>
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
        backgroundColor: "#111111",
        borderRadius: "50%",
        display: 'flex',
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        color: "#ffc600"
      },
      outerCircleDefault: {
        width: "120px",
        height: "120px",
        borderRadius: "50%",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#afafaf",
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
  computed: {
    classroomName: function () {
      if(typeof(this.data.id) === "string")
        return this.data.id.slice(1).replace('_', ' ');
      else
        console.log("??: " + this.data.id);
    }
  },
  methods: {
    outerCircleStyle: function(a) {
      
      if(this.time > 120*60){
        return {
          backgroundImage:
            "linear-gradient(0 deg, #ff6c00 50%, #ff6c00 50%), " +
            "linear-gradient(90deg, #ff6c00 50%, #ff6c00 50%)"
        };
      }
      else if(this.time<= 120*60 && this.time > 90*60){
        let angle = -( (this.time/60-60) / 60) * 360;
        angle -= 90;
        return {
          backgroundImage:
            "linear-gradient(-90deg, transparent 50%, #ff6c00 50%), " +
            "linear-gradient(" +
            angle +
            "deg, #ff6c00 48%, #ffc600 50%), " +
            "linear-gradient(90deg, #ff6c00 50%, transparent 50%)"
        };
      }
      else if(this.time <= 90*60 && this.time > 60*60){
        let angle = -( (this.time/60-60) / 60) * 360;
        angle -= 90;
        return {
          backgroundImage:
            "linear-gradient(90deg, transparent 50%, #ffc600 50%), " +
            "linear-gradient(" + angle + "deg, #ff6c00 48%, #ffc600 50%), " +
            "linear-gradient(90deg, #ffc600 50%, transparent 50%)"
        };
      }
      else if (this.time <= 60*60 && this.time > 30*60) {
        let angle = -(this.time/60 / 60) * 360;
        angle -= 90;
        return {
          backgroundImage:
            "linear-gradient(" +
            angle +
            "deg, #ffc600 48%, transparent 50%), " +
            "linear-gradient(90deg, #ffc600 50%, transparent 50%)"
        };
      } else {
        let angle = -(this.time/60 / 60) * 360;
        angle -= 90;
        return {
          backgroundImage:
            "linear-gradient(-90deg, #afafaf 50%, transparent 60%)," +
            "linear-gradient(" +
            angle +
            "deg, #ffc600 48%, transparent 50%)"
        };
      }
    },
    updateDatetime: function(){

        if (this.time <= 0)
          this.data.TUO = "¡Se ocupó!";

        if(typeof(this.data.TUO) !== "string")
        {
          this.time -= 1;
          if(this.time % 60 == 0)
            this.data.TUO -= 1;
        }
        
    }
  }
};
</script>
