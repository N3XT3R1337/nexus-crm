<template>
  <div class="card p-4 hover:shadow-md transition-shadow cursor-pointer" @click="$emit('click', contact)">
    <div class="flex items-start gap-3">
      <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-medium text-sm"
        :style="{ backgroundColor: avatarColor }">
        {{ contact.first_name[0] }}{{ contact.last_name[0] }}
      </div>
      <div class="flex-1 min-w-0">
        <h3 class="text-sm font-medium text-gray-900 dark:text-white truncate">
          {{ contact.first_name }} {{ contact.last_name }}
        </h3>
        <p v-if="contact.job_title" class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ contact.job_title }}</p>
        <p v-if="contact.email" class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ contact.email }}</p>
      </div>
      <span :class="['badge', statusClass]">{{ contact.status }}</span>
    </div>
    <div v-if="contact.tags?.length" class="mt-3 flex flex-wrap gap-1">
      <span v-for="tag in contact.tags" :key="tag.id" class="text-xs px-2 py-0.5 rounded-full text-white"
        :style="{ backgroundColor: tag.color }">{{ tag.name }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Contact } from '@/types'

const props = defineProps<{ contact: Contact }>()
defineEmits<{ click: [contact: Contact] }>()

const statusClass = computed(() => {
  const classes: Record<string, string> = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    lead: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    customer: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    churned: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  }
  return classes[props.contact.status] || 'bg-gray-100 text-gray-800'
})

const avatarColor = computed(() => {
  const colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#EC4899', '#14B8A6']
  const index = (props.contact.first_name.charCodeAt(0) + props.contact.last_name.charCodeAt(0)) % colors.length
  return colors[index]
})
</script>
