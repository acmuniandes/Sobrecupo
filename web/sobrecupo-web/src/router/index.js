import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ClassroomList from '@/components/ClassroomList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ClassroomList',
      component: ClassroomList
    }
  ]
})
