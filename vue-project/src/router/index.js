import { createRouter, createWebHistory } from 'vue-router'
import RechercheView from '../views/RechercheView.vue'
import ChatBotView from '../views/ChatBotView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/recherche',
      name: 'recherche',
      component: RechercheView,
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatBotView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
  ],
})

export default router