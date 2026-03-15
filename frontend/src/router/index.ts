import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/views/AppLayout.vue'),
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
        { path: 'contacts', name: 'Contacts', component: () => import('@/views/ContactsView.vue') },
        { path: 'contacts/:id', name: 'ContactDetail', component: () => import('@/views/ContactDetailView.vue') },
        { path: 'companies', name: 'Companies', component: () => import('@/views/CompaniesView.vue') },
        { path: 'companies/:id', name: 'CompanyDetail', component: () => import('@/views/CompanyDetailView.vue') },
        { path: 'deals', name: 'Deals', component: () => import('@/views/DealsView.vue') },
        { path: 'deals/:id', name: 'DealDetail', component: () => import('@/views/DealDetailView.vue') },
        { path: 'pipeline', name: 'Pipeline', component: () => import('@/views/PipelineView.vue') },
        { path: 'activities', name: 'Activities', component: () => import('@/views/ActivitiesView.vue') },
        { path: 'reports', name: 'Reports', component: () => import('@/views/ReportsView.vue') },
        { path: 'settings', name: 'Settings', component: () => import('@/views/SettingsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  if (to.meta.public || authStore.isAuthenticated) {
    next()
  } else {
    next('/login')
  }
})

export default router
