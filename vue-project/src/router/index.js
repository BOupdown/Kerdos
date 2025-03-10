import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CalculsView from '../views/CalculsView.vue'
import RechercheView from '../views/RechercheView.vue'
import chatbotView from '../views/chatbotView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/calculs',
      name: 'calculs',
      component: CalculsView,
    },
    {
      path: '/recherche',
      name: 'recherche',
      component: RechercheView,
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: chatbotView,
    },
  ],
  
})

export default router