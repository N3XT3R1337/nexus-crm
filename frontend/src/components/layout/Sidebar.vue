<template>
  <aside class="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-primary-600 flex items-center justify-center">
          <span class="text-lg font-bold text-white">N</span>
        </div>
        <div>
          <h1 class="text-lg font-bold text-gray-900 dark:text-white">Nexus CRM</h1>
          <p class="text-xs text-gray-500 dark:text-gray-400">Sales Management</p>
        </div>
      </div>
    </div>

    <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
      <router-link v-for="item in navItems" :key="item.path" :to="item.path"
        :class="['sidebar-link', { active: $route.path === item.path || $route.path.startsWith(item.path + '/') }]">
        <span class="text-lg">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="p-3 border-t border-gray-200 dark:border-gray-700">
      <div class="flex items-center gap-3 px-3 py-2">
        <div class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
          <span class="text-sm font-medium text-primary-600 dark:text-primary-400">
            {{ authStore.user?.first_name?.[0] }}{{ authStore.user?.last_name?.[0] }}
          </span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ authStore.fullName }}</p>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ authStore.user?.email }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: '\u{1F4CA}' },
  { path: '/contacts', label: 'Contacts', icon: '\u{1F465}' },
  { path: '/companies', label: 'Companies', icon: '\u{1F3E2}' },
  { path: '/deals', label: 'Deals', icon: '\u{1F4B0}' },
  { path: '/pipeline', label: 'Pipeline', icon: '\u{1F504}' },
  { path: '/activities', label: 'Activities', icon: '\u{1F4CB}' },
  { path: '/reports', label: 'Reports', icon: '\u{1F4C8}' },
  { path: '/settings', label: 'Settings', icon: '\u{2699}\u{FE0F}' },
]
</script>
