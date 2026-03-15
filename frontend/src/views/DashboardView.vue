<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Dashboard</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <StatsCard label="Total Revenue" :value="stats.total_revenue" icon="\u{1F4B0}" prefix="$"
        iconBg="bg-green-100 dark:bg-green-900/30" />
      <StatsCard label="Open Deals" :value="stats.open_deals" icon="\u{1F4C8}"
        iconBg="bg-blue-100 dark:bg-blue-900/30" />
      <StatsCard label="Total Contacts" :value="stats.total_contacts" icon="\u{1F465}"
        iconBg="bg-purple-100 dark:bg-purple-900/30" />
      <StatsCard label="Conversion Rate" :value="stats.conversion_rate" icon="\u{1F3AF}" suffix="%"
        iconBg="bg-orange-100 dark:bg-orange-900/30" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <RevenueChart title="Monthly Revenue" :labels="revenueLabels" :datasets="revenueDatasets" type="bar" />
      <PipelineChart :stages="pipeline" />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <StatsCard label="Won Deals" :value="stats.won_deals" icon="\u{1F3C6}"
        iconBg="bg-green-100 dark:bg-green-900/30" />
      <StatsCard label="Lost Deals" :value="stats.lost_deals" icon="\u{274C}"
        iconBg="bg-red-100 dark:bg-red-900/30" />
      <StatsCard label="Avg Deal Value" :value="stats.avg_deal_value" icon="\u{1F4B5}" prefix="$"
        iconBg="bg-indigo-100 dark:bg-indigo-900/30" />
      <StatsCard label="Pipeline Value" :value="stats.pipeline_value" icon="\u{1F4CA}" prefix="$"
        iconBg="bg-cyan-100 dark:bg-cyan-900/30" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <RevenueChart title="Contacts by Source" :labels="sourceLabels" :datasets="sourceDatasets" type="doughnut" />
      <div class="card p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Activities</h3>
        <ActivityTimeline :activities="recentActivities" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'
import StatsCard from '@/components/dashboard/StatsCard.vue'
import RevenueChart from '@/components/dashboard/RevenueChart.vue'
import PipelineChart from '@/components/dashboard/PipelineChart.vue'
import ActivityTimeline from '@/components/activities/ActivityTimeline.vue'
import type { DashboardStats, PipelineStage, Activity } from '@/types'

const stats = ref<DashboardStats>({
  total_contacts: 0, total_companies: 0, total_deals: 0, total_revenue: 0,
  won_deals: 0, lost_deals: 0, open_deals: 0, conversion_rate: 0,
  avg_deal_value: 0, pipeline_value: 0, activities_this_week: 0, new_contacts_this_month: 0,
})
const pipeline = ref<PipelineStage[]>([])
const revenueData = ref<any[]>([])
const sourceData = ref<any[]>([])
const recentActivities = ref<Activity[]>([])
const revenueLabels = ref<string[]>([])
const revenueDatasets = ref<any[]>([])
const sourceLabels = ref<string[]>([])
const sourceDatasets = ref<any[]>([])

onMounted(async () => {
  const [statsRes, pipelineRes, revenueRes, sourceRes, activitiesRes] = await Promise.all([
    apiClient.get('/dashboard/stats'),
    apiClient.get('/dashboard/pipeline-summary'),
    apiClient.get('/dashboard/deal-value-by-month?months=6'),
    apiClient.get('/dashboard/contacts-by-source'),
    apiClient.get('/dashboard/recent-activities?limit=5'),
  ])

  stats.value = statsRes.data
  pipeline.value = pipelineRes.data
  revenueData.value = revenueRes.data
  sourceData.value = sourceRes.data
  recentActivities.value = activitiesRes.data

  revenueLabels.value = revenueData.value.map((d: any) => d.month)
  revenueDatasets.value = [{
    label: 'Revenue',
    data: revenueData.value.map((d: any) => d.revenue),
    backgroundColor: '#6366F1',
  }]

  sourceLabels.value = sourceData.value.map((d: any) => d.source)
  sourceDatasets.value = [{
    label: 'Contacts',
    data: sourceData.value.map((d: any) => d.count),
    backgroundColor: ['#6366F1', '#EC4899', '#F59E0B', '#10B981', '#3B82F6', '#EF4444', '#8B5CF6'],
  }]
})
</script>
