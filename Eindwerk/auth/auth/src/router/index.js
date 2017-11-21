import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Profile from '@/components/Profile'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
      {
      path: '/register',
      name: 'Register',
      component: Register
    },
      {
      path: '/profile',
      name: 'Profile',
      component: Profile
    }
  ]
})
