<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Pipeline</h1>
      <router-link to="/deals" class="btn-secondary">List View</router-link>
    </div>

    <KanbanBoard v-if="stages.length" :stages="stages" :deals="deals"
      @deal-click="goToDeal" @stage-change="handleStageChange" />
    <div v-else class="text-center py-12 text-gray-500">Loading pipeline...</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDealsStore } from '@/stores/deals'
import KanbanBoard from '@/components/deals/KanbanBoard.vue'
import type { Deal } from '@/types'

const router = useRouter()
const store = useDealsStore()

const stages = computed(() => store.stages)
const deals = computed(() => store.deals)

onMounted(async () => {
  await Promise.all([store.fetchStages(), store.fetchDeals({ per_page: 100 })])
})

function goToDeal(deal: Deal) {
  router.push(`/deals/${deal.id}`)
}

async function handleStageChange(dealId: string, stageId: string) {
  await store.transitionStage(dealId, stageId)
}
</script>
