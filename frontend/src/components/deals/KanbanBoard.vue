<template>
  <div class="flex gap-4 overflow-x-auto pb-4">
    <div v-for="stage in stages" :key="stage.id"
      class="flex-shrink-0 w-72 bg-gray-100 dark:bg-gray-800 rounded-xl p-3"
      @dragover.prevent @drop="handleDrop($event, stage.id)">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full" :style="{ backgroundColor: stage.color }"></span>
          <h3 class="font-medium text-gray-900 dark:text-white text-sm">{{ stage.name }}</h3>
          <span class="badge bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
            {{ getStageDeals(stage.id).length }}
          </span>
        </div>
        <span class="text-xs text-gray-500 dark:text-gray-400">
          ${{ getStageValue(stage.id).toLocaleString() }}
        </span>
      </div>
      <div class="space-y-2 min-h-[100px]">
        <DealCard v-for="deal in getStageDeals(stage.id)" :key="deal.id" :deal="deal"
          @click="$emit('deal-click', deal)" @dragstart="handleDragStart" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Deal, DealStage } from '@/types'
import DealCard from './DealCard.vue'

const props = defineProps<{
  stages: DealStage[]
  deals: Deal[]
}>()

const emit = defineEmits<{
  'deal-click': [deal: Deal]
  'stage-change': [dealId: string, stageId: string]
}>()

let draggedDealId = ''

function getStageDeals(stageId: string): Deal[] {
  return props.deals.filter(d => d.stage_id === stageId && d.status === 'open')
}

function getStageValue(stageId: string): number {
  return getStageDeals(stageId).reduce((sum, d) => sum + d.value, 0)
}

function handleDragStart(event: DragEvent, deal: Deal) {
  draggedDealId = deal.id
  event.dataTransfer?.setData('text/plain', deal.id)
}

function handleDrop(_event: DragEvent, stageId: string) {
  if (draggedDealId) {
    emit('stage-change', draggedDealId, stageId)
    draggedDealId = ''
  }
}
</script>
