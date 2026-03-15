<template>
  <div class="card p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ label }}</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">
          {{ prefix }}{{ typeof value === 'number' ? value.toLocaleString() : value }}{{ suffix }}
        </p>
        <p v-if="change !== undefined" :class="['text-sm mt-1', change >= 0 ? 'text-green-600' : 'text-red-600']">
          {{ change >= 0 ? '+' : '' }}{{ change }}% from last period
        </p>
      </div>
      <div :class="['w-12 h-12 rounded-xl flex items-center justify-center text-xl', iconBg]">
        {{ icon }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  label: string
  value: number | string
  icon: string
  iconBg?: string
  prefix?: string
  suffix?: string
  change?: number
}>(), {
  iconBg: 'bg-primary-100 dark:bg-primary-900/30',
  prefix: '',
  suffix: '',
})
</script>
