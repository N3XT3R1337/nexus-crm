<template>
  <div class="space-y-4">
    <div v-for="activity in activities" :key="activity.id" class="flex gap-3">
      <div class="flex-shrink-0">
        <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm', iconClass(activity.type)]">
          {{ typeIcon(activity.type) }}
        </div>
      </div>
      <div class="flex-1 min-w-0">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">{{ activity.subject }}</p>
            <p v-if="activity.description" class="text-sm text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">
              {{ activity.description }}
            </p>
          </div>
          <div class="flex items-center gap-2 ml-4">
            <span v-if="activity.completed" class="badge bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">Done</span>
            <span v-else-if="isOverdue(activity)" class="badge bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">Overdue</span>
          </div>
        </div>
        <div class="flex items-center gap-3 mt-1 text-xs text-gray-400">
          <span>{{ formatDate(activity.created_at) }}</span>
          <span v-if="activity.due_date">Due: {{ formatDate(activity.due_date) }}</span>
          <span v-if="activity.duration_minutes">{{ activity.duration_minutes }}min</span>
        </div>
      </div>
    </div>
    <p v-if="activities.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-8">No activities yet</p>
  </div>
</template>

<script setup lang="ts">
import type { Activity } from '@/types'

defineProps<{ activities: Activity[] }>()

function typeIcon(type: string): string {
  const icons: Record<string, string> = {
    call: '\u{1F4DE}', email: '\u{1F4E7}', meeting: '\u{1F91D}', task: '\u{2705}',
    note: '\u{1F4DD}', follow_up: '\u{1F504}', demo: '\u{1F4BB}', proposal: '\u{1F4C4}',
  }
  return icons[type] || '\u{1F4CB}'
}

function iconClass(type: string): string {
  const classes: Record<string, string> = {
    call: 'bg-blue-100 dark:bg-blue-900',
    email: 'bg-green-100 dark:bg-green-900',
    meeting: 'bg-purple-100 dark:bg-purple-900',
    task: 'bg-yellow-100 dark:bg-yellow-900',
    note: 'bg-gray-100 dark:bg-gray-700',
    follow_up: 'bg-orange-100 dark:bg-orange-900',
    demo: 'bg-indigo-100 dark:bg-indigo-900',
    proposal: 'bg-pink-100 dark:bg-pink-900',
  }
  return classes[type] || 'bg-gray-100 dark:bg-gray-700'
}

function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function isOverdue(activity: Activity): boolean {
  return !activity.completed && !!activity.due_date && new Date(activity.due_date) < new Date()
}
</script>
