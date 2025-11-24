/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'

import Documents from '@/pages/Documents.vue'
import Random from '@/pages/Random.vue'
import General from '@/pages/General.vue'
import Tickets from '@/pages/Tickets.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Landing page

router.addRoute({ path: '/upload', component: General })
router.addRoute({ path: '/tickets', component: Tickets})
router.addRoute({ path: '/docs', component: Documents })
router.addRoute({ path: '/rand', component: Random })


// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (localStorage.getItem('vuetify:dynamic-reload')) {
      console.error('Dynamic import error, reloading page did not fix it', err)
    } else {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
