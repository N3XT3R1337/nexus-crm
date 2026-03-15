<template>
  <header class="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6">
    <div class="flex-1 max-w-lg">
      <SearchBar />
    </div>

    <div class="flex items-center gap-4">
      <button @click="toggleTheme" class="btn-ghost p-2 rounded-lg">
        <span v-if="isDark" class="text-lg">\u{2600}\u{FE0F}</span>
        <span v-else class="text-lg">\u{1F319}</span>
      </button>

      <NotificationBell />

      <button @click="handleLogout" class="btn-ghost text-sm">Logout</button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import SearchBar from '@/components/common/SearchBar.vue'
import NotificationBell from '@/components/notifications/NotificationBell.vue'

const router = useRouter()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
