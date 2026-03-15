<template>
  <div class="card p-4 hover:shadow-md transition-shadow cursor-pointer" @click="$emit('click', deal)"
    draggable="true" @dragstart="$emit('dragstart', $event, deal)">
    <div class="flex items-start justify-between">
      <h3 class="text-sm font-medium text-gray-900 dark:text-white truncate flex-1">{{ deal.title }}</h3>
      <span :class="['badge ml-2', priorityClass]">{{ deal.priority }}</span>
    </div>
    <p class="text-lg font-bold text-gray-900 dark:text-white mt-2">
      ${{ deal.value.toLocaleString() }}
    </p>
    <div class="mt-3 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
      <span>{{ deal.probability }}% probability</span>
      <span v-if="deal.expected_close_date">{{ formatDate(deal.expected_close_date) }}</span>
    </div>
    <div v-if="deal.stage" class="mt-2">
      <span class="text-xs px-2 py-0.5 rounded-full text-white" :style="{ backgroundColor: deal.stage.color }">
        {{ deal.stage.name }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Deal } from '@/types'

const props = defineProps<{ deal: Deal }>()
defineEmits<{
  click: [deal: Deal]
  dragstart: [event: DragEvent, deal: Deal]
}>()

const priorityClass = computed(() => {
  const classes: Record<string, string> = {
    low: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    medium: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
    critical: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  }
  return classes[props.deal.priority] || 'bg-gray-100 text-gray-800'
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>
