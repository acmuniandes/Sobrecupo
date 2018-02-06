<template>
  <div>
    <div v-for="classroom in info">
      <classroom-timer/>
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
      error: ''
    };
  },
  mounted() {
    //Using a pointer to this due to the context change on axios function
    const _this = this;
    axios.get("/salones")
      .then(response => {
        _this.info = response.data;
      })
      .catch(error => {
        console.log(error);
        _this.error = error.data;
      });
    
    this.classroomNow(new Date());
    console.log(this.info);
  },
  methods:{
    classroomNow: function(date){
      //First part of the method generates day schedule from base json
      classrooms = this.info
      exceptions = []
      localClassrooms = {}
      today = this.generateDate(date)
      for(classroom in classrooms)
      {
        //If the classroom does not belong to the known invalid classrooms list, compute it
        if(this.invalidClassrooms.indexOf(classroom) == -1)
        {
          schedule = []
          exceptions = classrooms[classroom]["exceptions"][today]

          /*
          console.log("Exceptions " + classroom + " // " + today + ":")
          console.log(exceptions)
          */

          if(exceptions != undefined)
          {
            //The 'today' field contains a string with the format "SCH$$SCH$$ (...)"
            //TODO error may be on month/day format (AGO = 08 and not 8, etc.)
            schedule = schedule.concat(exceptions.split("$$"))

            //console.log("after exp: " + schedule)
          }
          //This line converts to a JS object but the string is not optimally formed, so it has to replace
          // ' ocurrences with " to be a valid json to parse
          base = JSON.parse(classrooms[classroom][(date.getDay()-1).toString()].replace(/\'/g, '\"'))

          for(sch in base)
            schedule.push(base[sch])
          
          localClassrooms[classroom] = schedule
        }
      }

      //Second part, finds free classrooms from previous data structure formed

      console.log("Local classrooms: ")
      console.log(localClassrooms)

      hour = date.getHours()*100 + date.getMinutes()

      for(classroom in localClassrooms)
      {
          //Warden variable, modeling that the hour belongs to the tuple
          warden = true

          //Variable that saves the shortest (but positive) difference betweeen
          //the first element of all cointinuity tuples
          timeUntilOccupation = 9000

          //Variables that store information to fix base 10 aritmethic offset (later explained)
          hourI = 0
          hourF = 0

          for(continuityTuple in localClassrooms[classroom])
          {
            continuity_tuple = localClassrooms[classroom][continuityTuple].split(/ - /g)

            //console.log("Non split: " + localClassrooms[classroom][continuityTuple])
            //console.log("Splitted: " + continuity_tuple)

            //Checks if given hour is within continuityTuple
            if(this.isInCountinuityTuple(hour, continuity_tuple))
            {
              //If so, it means that the classroom is occupied, thus, there's no need to check
              //if it's within another tuple (and continue with the next classroom)
              warden = false
              break
            }

            //Compares actual continuity tuple difference with the actual best aproximation
            tupleHour = parseInt(continuity_tuple[0])
            difference = tupleHour - hour

            if(difference > 0 && difference<timeUntilOccupation)
            {
              //Due to implementation, base 10 aritmethic will result in unconsistent behaviour
              //when time comparisons are made between different hours (ie. 09:45 vs 10:10)

              //This will be fixed later using hourI/F
              timeUntilOccupation = difference

              hourI = Math.floor(hour/100)
              hourF = Math.floor(tupleHour/100)
            }
          }

          //If the warden remains true, the hour is not in any tuple of the classrooms
          //schedules, meaning it's free! (eureka!)
          if (warden)
          {
            //Printing state for testing 
            /*
            console.log("----Start----")
            console.log("hI: " + hourI)
            console.log("hF: " + hourF)
            */            

            //Creates an object with classroom id as a key and time until occupation as value
            if(timeUntilOccupation == 9000)
            {
              timeUntilOccupation = "Hasta el final del día"
              //--
              classroomObject = {}
              classroomObject["id"] = classroom
              classroomObject["TUO"] = timeUntilOccupation
              //--
              this.freeClassrooms.push(classroomObject)
            }
            
            //Due to implementation, base 10 aritmethic will result in unconsistent behaviour
            //when a classroom is free for longer than 60 minutes

            //Formula obtained by experimental trial and error
            else if(hourF-hourI >= 0)
            {
              //console.log("TUO before: " + timeUntilOccupation)
              timeUntilOccupation = timeUntilOccupation - (40*(hourF - hourI))
              //console.log("TUO after: " + timeUntilOccupation)
              if (timeUntilOccupation >10)
              {
                //--
                classroomObject = {}
                classroomObject["id"] = classroom
                classroomObject["TUO"] = timeUntilOccupation
                //--
                this.freeClassrooms.push(classroomObject)
              }
            }   
          }

          //Note that if the class is not free, timeUntilOcupation's value is irrelevant
          //(for now) [as well with hourI/hourF]

          //----------Creating unique building list---------
          if(!this.arrContains(this.allBuildings, this.extractBuilding(classroom)))
              this.allBuildings.push(this.extractBuilding(classroom))
          //-------------------
      }
    }
  }
};
</script>
