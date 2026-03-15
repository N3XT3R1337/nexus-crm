<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Reports</h1>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <RevenueChart title="Revenue Forecast" :labels="forecastLabels" :datasets="forecastDatasets" type="line" />
      <RevenueChart title="Pipeline Velocity" :labels="velocityLabels" :datasets="velocityDatasets" type="bar" />
    </div>

    <div class="card p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Sales by Owner</h3>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-900/50">
            <tr>
              <th class="table-header">Name</th>
              <th class="table-header">Total Deals</th>
              <th class="table-header">Won Deals</th>
              <th class="table-header">Total Value</th>
              <th class="table-header">Win Rate</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="owner in salesByOwner" :key="owner.user_id">
              <td class="table-cell font-medium">{{ owner.name }}</td>
              <td class="table-cell">{{ owner.total_deals }}</td>
              <td class="table-cell">{{ owner.won_deals }}</td>
              <td class="table-cell">${{ owner.total_value.toLocaleString() }}</td>
              <td class="table-cell">{{ owner.total_deals > 0 ? Math.round(owner.won_deals / owner.total_deals * 100) : 0 }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'
import RevenueChart from '@/components/dashboard/RevenueChart.vue'

const forecastLabels = ref<string[]>([])
const forecastDatasets = ref<any[]>([])
const velocityLabels = ref<string[]>([])
const velocityDatasets = ref<any[]>([])
const salesByOwner = ref<any[]>([])

onMounted(async () => {
  const [forecastRes, velocityRes, salesRes] = await Promise.all([
    apiClient.get('/reports/revenue-forecast?months=6'),
    apiClient.get('/reports/pipeline-velocity'),
    apiClient.get('/reports/sales-by-owner'),
  ])

  forecastLabels.value = forecastRes.data.map((d: any) => d.month)
  forecastDatasets.value = [
    { label: 'Predicted', data: forecastRes.data.map((d: any) => d.predicted), borderColor: '#6366F1', backgroundColor: 'rgba(99,102,241,0.1)' },
    { label: 'Weighted', data: forecastRes.data.map((d: any) => d.weighted), borderColor: '#F59E0B', backgroundColor: 'rgba(245,158,11,0.1)' },
    { label: 'Actual', data: forecastRes.data.map((d: any) => d.actual), borderColor: '#10B981', backgroundColor: 'rgba(16,185,129,0.1)' },
  ]

  velocityLabels.value = velocityRes.data.map((d: any) => d.stage_name)
  velocityDatasets.value = [{
    label: 'Deals in Stage',
    data: velocityRes.data.map((d: any) => d.deal_count),
    backgroundColor: '#8B5CF6',
  }]

  salesByOwner.value = salesRes.data
})
</script>
