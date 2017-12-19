import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Completion from '@/components/Completion'
import Profile from '@/components/Profile'
import Lobby from '@/components/Lobby'
import Game from '@/components/Game'
import GameFinal from '@/components/GameFinal'
import Admin from '@/components/Admin'

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
            path: '/completion',
            name: 'Completion',
            component: Completion
        },
        {
            path: '/profile',
            name: 'Profile',
            component: Profile
        },
        {
            path: '/lobby',
            name: 'Lobby',
            component: Lobby
        },
        // {
        //     path: '/game',
        //     name: 'Game',
        //     component: Game,
        //     props: { default: true }
        //
        // },
        {
            path: '/game',
            name: 'GameFinal',
            component: GameFinal,
            props: { default: true }

        },
        {
            path: '/admin',
            name: 'Admin',
            component: Admin,
        }
    ]
})
