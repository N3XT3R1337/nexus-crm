<template>
  <div class="relative">
    <button @click="togglePanel" class="btn-ghost p-2 rounded-lg relative">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      <span v-if="store.hasUnread"
        class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
        {{ store.unreadCount > 9 ? '9+' : store.unreadCount }}
      </span>
    </button>

    <div v-if="showPanel"
      class="absolute right-0 top-full mt-2 w-80 card shadow-xl z-50 max-h-96 overflow-hidden">
      <div class="p-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <h3 class="font-medium text-gray-900 dark:text-white">Notifications</h3>
        <button v-if="store.hasUnread" @click="store.markAllAsRead()" class="text-xs text-primary-600 hover:text-primary-500">
          Mark all read
        </button>
      </div>
      <div class="overflow-y-auto max-h-72">
        <div v-for="n in store.notifications" :key="n.id"
          :class="['px-3 py-3 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750 cursor-pointer',
            { 'bg-primary-50 dark:bg-primary-900/10': !n.read }]"
          @click="handleClick(n)">
          <p class="text-sm font-medium text-gray-900 dark:text-white">{{ n.title }}</p>
          <p v-if="n.message" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">{{ n.message }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ formatTime(n.created_at) }}</p>
        </div>
        <p v-if="store.notifications.length === 0" class="p-6 text-center text-gray-500 text-sm">No notifications</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationsStore } from '@/stores/notifications'
import type { Notification } from '@/types'

const router = useRouter()
const store = useNotificationsStore()
const showPanel = ref(false)

onMounted(() => store.fetchNotifications())

function togglePanel() {
  showPanel.value = !showPanel.value
  if (showPanel.value) store.fetchNotifications()
}

function handleClick(n: Notification) {
  store.markAsRead(n.id)
  if (n.link) router.push(n.link)
  showPanel.value = false
}

function formatTime(date: string): string {
  const diff = Date.now() - new Date(date).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}
</script>
