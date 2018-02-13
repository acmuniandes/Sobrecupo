<template>
  <div :style='gridStyle' >
    <div v-for='(classroom, index) of freeClassrooms' :key='index'>
      <classroom-timer classroom='classroom'/>
    </div>
  </div>
</template>

<script>
import ClassroomTimer from "./ClassroomTimer";
import axios from "axios";

export default {
  name: "ClassroomList",
  data() {
    return {
      info: null,
      error: "",
      freeClassrooms: [],
      invalidClassrooms: [],
      allBuildings: [],
      gridStyle: {
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gridGap: "20px"
      }
    };
  },
  components:{
    ClassroomTimer
  },
  mounted() {
    //Using a pointer to this due to the context change on axios function
    const _this = this;
    axios
      .get("/salones")
      .then(response => {
        _this.info = response.data;
        _this.classroomNow(new Date("February 13, 2018 11:13:00"));
        console.log(this.info);
      })
      .catch(error => {
        console.log(error);
        _this.error = error.data;
      });
  },
  methods: {
    generateDate: function(date) {
      const day = date.getDate();
      let month = date.getMonth() + 1;

      //Month format for json: if month beofre october: 0X, others XX
      if (month < 10) month = "0" + month;

      return day + "/" + month + "/18";
    },

    //@TODO Correct empty interval-emptiness
    //(technically all classrooms are free between classes)
    isInCountinuityTuple: function(hour, tuple) {
      //A continuity tuple is defined as a continous time interval in which the classroom is occupied.
      //The method just checks if the given hour is between the boundaries of the given tuple

      //tuple[0] is the lower boundary
      //tuple[1] is the uppper boundary

      //If the hour is bigger than the lower boundary
      if (
        hour >= parseInt(tuple[0]) /*plus/minus the dead time interval*/ - 10
      ) {
        //and is lower than the upper boundary
        if (hour < parseInt(tuple[1])) {
          //Then, it means that it is within the boundaries
          return true;
        }
      }
      return false;
    },

    formatFreeClassroom: function(classroom) {
      let msg = "";
      msg += classroom.id.slice(1);

      if (typeof classroom.TUO == "string")
        msg += ": Está libre hasta el final del dia";
      else if (classroom.TUO > 60)
        msg +=
          ": Está libre durante " +
          Math.floor(classroom.TUO / 60) +
          "h " +
          classroom.TUO % 60 +
          "m  [" +
          classroom.TUO +
          "m]";
      else msg += ": Está libre durante " + classroom.TUO + " minutos";

      return msg;
    },

    randomClassroom: function() {
      if (this.freeClassrooms.length == 0) {
        this.freeClassroom = "Paila";
        return this.freeClassroom;
      } else {
        let number = Math.random() * (this.freeClassrooms.length - 1);
        number = Math.round(number);
        const chosen = this.freeClassrooms[number];

        this.freeClassroom = this.formatFreeClassroom(chosen);
        return this.freeClassroom;
      }
    },

    arrContains: function(array, element) {
      for (var i of array) if (array[i] == element) return true;
      return false;
    },

    extractBuilding: function(classroomm) {
      let str = classroomm.split("_")[0];
      return str.slice(1);
    },

    generateIterator: function(classrooms) {
      return Object.keys(classrooms);
    },
    classroomNow: function(date) {
      //First part of the method generates day schedule from base json
      const classroomsRaw = this.info;
      let exceptions = [];
      let localClassrooms = {};
      let todayyy = this.generateDate(date);
      //due to ES6 for in loops do not work with objects - FUCK
      const classrooms = this.generateIterator(classroomsRaw);
      for(var classroomi in classrooms){
        //If the classroom does not belong to the known invalid classrooms list, compute it
        if (this.invalidClassrooms.indexOf(classrooms[classroomi]) == -1) {
          let schedule = [];
          exceptions = classroomsRaw[classrooms[classroomi]]["exceptions"][todayyy];

          /* console.log("Exceptions " + classrooms[classroomi] + " // " + todayyy + ":");
          console.log(exceptions); */
          

          if (exceptions){
            //The 'todayyy' field contains a string with the format "SCH$$SCH$$ (...)"
            //TODO error may be on month/day format (AGO = 08 and not 8, etc.)
            schedule = schedule.concat(exceptions.split("$$"));

            //console.log("after exp: " + schedule)
          }
          //This line converts to a JS object but the string is not optimally formed, so it has to replace
          // ' ocurrences with " to be a valid json to parse
          const base = JSON.parse(
            classroomsRaw[classrooms[classroomi]][(date.getDay() - 1).toString()].replace(
              /\'/g,
              '"'
            )
          );
          for (var sch in base) schedule.push(base[sch]);

          /* console.log(schedule);
          console.log("local classrooms: " , localClassrooms); */

          localClassrooms[classrooms[classroomi]] = schedule;
        }
      }

      //Second part, finds free classrooms from previous data structure formed

      console.log("Local classrooms: ");
      console.log(localClassrooms);

      let hour = date.getHours() * 100 + date.getMinutes();
      
      const _localClassrooms = this.generateIterator(localClassrooms);

      for (var classroom1 in _localClassrooms) {
        //Warden variable, modeling that the hour belongs to the tuple
        let warden = true;

        //Variable that saves the shortest (but positive) difference betweeen
        //the first element of all cointinuity tuples
        let timeUntilOccupation = 9000;

        //Variables that store information to fix base 10 aritmethic offset (later explained)
        let hourI = 0;
        let hourF = 0;

        for (var continuityTuple of localClassrooms[_localClassrooms[classroom1]]) {
          //console.log(_localClassrooms[classroom1] + " // " + continuityTuple);
          //const continuity_tuple = localClassrooms[_localClassrooms[classroom1]][continuityTuple].split(/ - /g);

          const continuity_tuple = continuityTuple.split(/ - /g);

          //console.log("Non split: " + localClassrooms[classroom][continuityTuple])
          //console.log("Splitted: " + continuity_tuple)

          //Checks if given hour is within continuityTuple
          if (this.isInCountinuityTuple(hour, continuity_tuple)) {
            //If so, it means that the classroom is occupied, thus, there's no need to check
            //if it's within another tuple (and continue with the next classroom)
            warden = false;
            break;
          }

          //Compares actual continuity tuple difference with the actual best aproximation
          const tupleHour = parseInt(continuity_tuple[0]);
          const difference = tupleHour - hour;

          if (difference > 0 && difference < timeUntilOccupation) {
            //Due to implementation, base 10 aritmethic will result in unconsistent behaviour
            //when time comparisons are made between different hours (ie. 09:45 vs 10:10)

            //This will be fixed later using hourI/F
            timeUntilOccupation = difference;

            hourI = Math.floor(hour / 100);
            hourF = Math.floor(tupleHour / 100);
          }
        }

        //If the warden remains true, the hour is not in any tuple of the classrooms
        //schedules, meaning it's free! (eureka!)
        if (warden) {
          //Printing state for testing
          /*
            console.log("----Start----")
            console.log("hI: " + hourI)
            console.log("hF: " + hourF)
            */

          //Creates an object with classroom id as a key and time until occupation as value
          if (timeUntilOccupation == 9000) {
            timeUntilOccupation = "Hasta el final del día";
            //--
            let classroomObject = {};
            classroomObject["id"] = _localClassrooms[classroom1];
            classroomObject["TUO"] = timeUntilOccupation;
            //--
            this.freeClassrooms.push(classroomObject);
          } else if (hourF - hourI >= 0) {
            //Due to implementation, base 10 aritmethic will result in unconsistent behaviour
            //when a classroom is free for longer than 60 minutes

            //Formula obtained by experimental trial and error
            //console.log("TUO before: " + timeUntilOccupation)
            timeUntilOccupation = timeUntilOccupation - 40 * (hourF - hourI);
            //console.log("TUO after: " + timeUntilOccupation)
            if (timeUntilOccupation > 10) {
              //--
              let classroomObject = {};
              classroomObject["id"] = _localClassrooms[classroom1];
              classroomObject["TUO"] = timeUntilOccupation;
              //--
              this.freeClassrooms.push(classroomObject);
            }
          }
        }

        //Note that if the class is not free, timeUntilOcupation's value is irrelevant
        //(for now) [as well with hourI/hourF]

        //----------Creating unique building list---------
        if (!this.arrContains(this.allBuildings, this.extractBuilding(classroom1)))
          this.allBuildings.push(this.extractBuilding(classroom1));
        //-------------------
      }
    }
  }
};
</script>
