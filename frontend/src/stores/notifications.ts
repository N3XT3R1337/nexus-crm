import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'
import type { Notification } from '@/types'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref<Notification[]>([])
  const total = ref(0)
  const unreadCount = ref(0)

  const hasUnread = computed(() => unreadCount.value > 0)

  async function fetchNotifications(page = 1) {
    const { data } = await apiClient.get('/notifications', { params: { page, per_page: 20 } })
    notifications.value = data.items
    total.value = data.total
    unreadCount.value = data.unread_count
  }

  async function markAsRead(id: string) {
    await apiClient.put(`/notifications/${id}/read`)
    const notification = notifications.value.find(n => n.id === id)
    if (notification && !notification.read) {
      notification.read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    }
  }

  async function markAllAsRead() {
    await apiClient.put('/notifications/read-all')
    notifications.value.forEach(n => n.read = true)
    unreadCount.value = 0
  }

  return { notifications, total, unreadCount, hasUnread, fetchNotifications, markAsRead, markAllAsRead }
})
