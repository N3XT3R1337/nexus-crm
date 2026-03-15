<template>
  <div v-if="deal">
    <div class="flex items-center gap-4 mb-6">
      <button @click="$router.back()" class="btn-ghost">&larr; Back</button>
      <div class="flex-1">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ deal.title }}</h1>
        <div class="flex items-center gap-3 mt-1">
          <span v-if="deal.stage" class="text-xs px-2 py-0.5 rounded-full text-white" :style="{ backgroundColor: deal.stage.color }">
            {{ deal.stage.name }}
          </span>
          <span :class="['badge', deal.status === 'won' ? 'bg-green-100 text-green-800' : deal.status === 'lost' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800']">
            {{ deal.status }}
          </span>
        </div>
      </div>
      <div v-if="deal.status === 'open'" class="flex gap-2">
        <button @click="handleWin" class="btn-primary bg-green-600 hover:bg-green-700">Mark Won</button>
        <button @click="showLoseModal = true" class="btn-danger">Mark Lost</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Deal Info</h2>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div><span class="text-gray-500">Value</span><p class="text-2xl font-bold">${{ deal.value.toLocaleString() }}</p></div>
            <div><span class="text-gray-500">Probability</span><p class="text-2xl font-bold">{{ deal.probability }}%</p></div>
            <div><span class="text-gray-500">Priority</span><p class="font-medium capitalize">{{ deal.priority }}</p></div>
            <div><span class="text-gray-500">Currency</span><p class="font-medium">{{ deal.currency }}</p></div>
            <div><span class="text-gray-500">Expected Close</span><p class="font-medium">{{ deal.expected_close_date ? new Date(deal.expected_close_date).toLocaleDateString() : '-' }}</p></div>
            <div><span class="text-gray-500">Created</span><p class="font-medium">{{ new Date(deal.created_at).toLocaleDateString() }}</p></div>
          </div>
          <div v-if="deal.description" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p class="text-sm text-gray-700 dark:text-gray-300">{{ deal.description }}</p>
          </div>
          <div v-if="deal.lost_reason" class="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
            <p class="text-sm text-red-700 dark:text-red-300"><strong>Lost reason:</strong> {{ deal.lost_reason }}</p>
          </div>
        </div>

        <div v-if="deal.status === 'open'" class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Stage Progression</h2>
          <div class="flex items-center gap-2">
            <div v-for="stage in stages" :key="stage.id"
              :class="['flex-1 h-2 rounded-full cursor-pointer transition-all', deal.stage_id === stage.id ? 'ring-2 ring-offset-2 ring-primary-500' : '']"
              :style="{ backgroundColor: deal.stage_id === stage.id || getStageOrder(stage.id) <= getStageOrder(deal.stage_id || '') ? stage.color : '#E5E7EB' }"
              @click="handleTransition(stage.id)">
            </div>
          </div>
          <div class="flex justify-between mt-2">
            <span v-for="stage in stages" :key="stage.id" class="text-xs text-gray-500 flex-1 text-center">{{ stage.name }}</span>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Activities</h2>
          <ActivityTimeline :activities="activities" />
        </div>
      </div>
    </div>

    <Modal v-model="showLoseModal" title="Mark Deal as Lost" size="sm">
      <div class="space-y-4">
        <textarea v-model="lostReason" class="input-field" rows="3" placeholder="Why was this deal lost?"></textarea>
        <div class="flex justify-end gap-3">
          <button @click="showLoseModal = false" class="btn-secondary">Cancel</button>
          <button @click="handleLose" class="btn-danger">Confirm Lost</button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useDealsStore } from '@/stores/deals'
import apiClient from '@/api/client'
import Modal from '@/components/common/Modal.vue'
import ActivityTimeline from '@/components/activities/ActivityTimeline.vue'
import type { Activity } from '@/types'

const route = useRoute()
const store = useDealsStore()
const activities = ref<Activity[]>([])
const showLoseModal = ref(false)
const lostReason = ref('')

const deal = computed(() => store.currentDeal)
const stages = computed(() => store.stages.filter(s => !['Closed Won', 'Closed Lost'].includes(s.name)))

function getStageOrder(stageId: string): number {
  return store.stages.find(s => s.id === stageId)?.order || 0
}

onMounted(async () => {
  const id = route.params.id as string
  await Promise.all([store.fetchDeal(id), store.fetchStages()])
  try {
    const res = await apiClient.get(`/activities?deal_id=${id}`)
    activities.value = res.data.items
  } catch { /* no activities */ }
})

async function handleTransition(stageId: string) {
  if (deal.value) await store.transitionStage(deal.value.id, stageId)
}

async function handleWin() {
  if (deal.value) await store.winDeal(deal.value.id)
}

async function handleLose() {
  if (deal.value && lostReason.value) {
    await store.loseDeal(deal.value.id, lostReason.value)
    showLoseModal.value = false
  }
}
</script>
