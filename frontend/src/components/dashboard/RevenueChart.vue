<template>
  <div class="card p-6">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">{{ title }}</h3>
    <div class="h-64">
      <Bar v-if="type === 'bar'" :data="chartData" :options="chartOptions" />
      <Doughnut v-else-if="type === 'doughnut'" :data="chartData" :options="chartOptions" />
      <Line v-else :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Bar, Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement,
  ArcElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler)

const props = withDefaults(defineProps<{
  title: string
  labels: string[]
  datasets: Array<{ label: string; data: number[]; backgroundColor?: string | string[]; borderColor?: string }>
  type?: 'bar' | 'line' | 'doughnut'
}>(), { type: 'bar' })

const chartData = computed(() => ({
  labels: props.labels,
  datasets: props.datasets.map(ds => ({
    ...ds,
    backgroundColor: ds.backgroundColor || '#6366F1',
    borderColor: ds.borderColor || '#6366F1',
    borderWidth: props.type === 'line' ? 2 : 0,
    fill: props.type === 'line',
    tension: 0.4,
  })),
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: props.datasets.length > 1 || props.type === 'doughnut' },
  },
  scales: props.type === 'doughnut' ? {} : {
    y: { beginAtZero: true, grid: { color: 'rgba(156, 163, 175, 0.1)' } },
    x: { grid: { display: false } },
  },
}))
</script>
