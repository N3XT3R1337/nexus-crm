<template>
  <div class="card p-6">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Pipeline Overview</h3>
    <div class="space-y-3">
      <div v-for="stage in stages" :key="stage.id" class="flex items-center gap-3">
        <span class="w-3 h-3 rounded-full flex-shrink-0" :style="{ backgroundColor: stage.color }"></span>
        <span class="text-sm text-gray-700 dark:text-gray-300 w-24 flex-shrink-0">{{ stage.name }}</span>
        <div class="flex-1 h-6 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
          <div class="h-full rounded-full transition-all duration-500"
            :style="{ width: barWidth(stage.total_value) + '%', backgroundColor: stage.color }"></div>
        </div>
        <span class="text-sm font-medium text-gray-900 dark:text-white w-28 text-right">
          ${{ stage.total_value.toLocaleString() }}
        </span>
        <span class="text-xs text-gray-500 w-16 text-right">{{ stage.deal_count }} deals</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PipelineStage } from '@/types'

const props = defineProps<{ stages: PipelineStage[] }>()

const maxValue = computed(() => Math.max(...props.stages.map(s => s.total_value), 1))

function barWidth(value: number): number {
  return (value / maxValue.value) * 100
}
</script>
