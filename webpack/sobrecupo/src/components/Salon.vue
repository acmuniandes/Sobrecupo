<template>
    <div class='classroom animated fadeInLeft' v-if='$store.state.filter.includes(block)'>
      <div class="row">
        <div class="col s1 m11">
          <div class="card blue-grey darken-1">
            <div class="card-content white-text">
              <span class="card-title">{{classroomname.replace('.','').replace('_',' ')}}</span>
              <p>50 minutos</p>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<style>
.classroom{
float: left;
margin: 0;
width: 10rem

}

.card-content{
  border-radius: 4rem
}

.classroomNumber{
  font-weight: 800;
  font-size: 30px;
  float: left
}

.remainingTime{
  font-size: 20px;
}


</style>


<script>

export default {
  name: 'salon',
  props: {
    classroomname: {},
    remainingtime: {}
  },
  computed: {
    block: function () {
      return this.classroomname.split('_')[0].substring(1)
    }
  }
}
</script>
